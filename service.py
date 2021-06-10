import math
from typing import Tuple

import grpc
import threading
import logging
from data_structure import Data, TableEntry
from utils import NodeType as n
from utils import TossMessageType as t
from utils import DataHandlingType as d

from grpc._channel import _InactiveRpcError

from protos.output import chord_pb2
from protos.output import chord_pb2_grpc

"""
class Service:
    # server : grpc.server
    #
    def __init__(self):
        pass
    def serve(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
"""


def node_health_check(node: Data) -> bool:
    try:
        with grpc.insecure_channel(node.value) as channel:
            stub = chord_pb2_grpc.HealthCheckerStub(channel)
            response = stub.Check(chord_pb2.HealthCheck(ping=0))
        return True
    except _InactiveRpcError:
        return False


def request_node_info(node: Data, which_info: int) -> Tuple[str, str]:
    # which_info는 utils.NodeType 의 명세를 따름
    with grpc.insecure_channel(node.value) as channel:
        stub = chord_pb2_grpc.GetNodeValueStub(channel)
        response = stub.GetNodeVal(chord_pb2.NodeDetail(node_address=node.value, which_node=which_info))
    return response.node_key, response.node_address


def notify_node_info(target_node: Data, node_info: Data, which_node: int) -> int:
    # change_type 는 utils.NodeType 의 명세를 따름
    with grpc.insecure_channel(target_node.value) as channel:
        stub = chord_pb2_grpc.NotifyNodeStub(channel)
        response = stub.NotifyNodeChanged(chord_pb2.NodeType(
            node_key=node_info.key, node_address=node_info.value, which_node=which_node
        ))
    return response.pong


def toss_message(starter_node: Data, receive_node: Data, message_type: int, message: int = 0, node_type: int = 0) -> int:
    # message_type 는 utils.TossMessageType 의 명세를 따름
    try:
        with grpc.insecure_channel(receive_node.value) as channel:
            stub = chord_pb2_grpc.TossMessageStub(channel)
            response = stub.TM(chord_pb2.Message(
                node_key=starter_node.key, node_address=starter_node.value,
                message_type=message_type, message=message, node_type=node_type
            ))
        return response.pong
    except _InactiveRpcError:
        return False


def data_request(starter_node: Data, receive_node: Data, data: Data, data_handling_type: int) -> int:
    """
    chord.proto 의 HandleData 요청을 보내는 메소드
    :param starter_node: 처음 요청을 생성하는 노드, 함수를 호출할 시에는 호출한 노드를 넣는 것이 맞음
    :param receive_node: 요청을 받는 노드, 현재는 모두 chord_node 의 successor 를 할당했으나, 추후에 finger table 이 구현되면 달라질 수 있음
    :param data: 요청하는 데이터. get 이나 remove 시 value 는 비어도 됨
    :param data_handling_type: utils.DataHandlingType 의 명세를 따름 (단, get_result 를 호출해서 사용할 필요는 없으니 사용하지 않아도 됨
            -> 자세한건 186번째 HandleDataService 클래스 참고할 것
    :return: receive_node 가 값을 잘 처리했으면 0이 return 됨
    """
    # data_handling_type 는 utils.DataHandlingType 의 명세를 따름
    with grpc.insecure_channel(receive_node.value) as channel:
        stub = chord_pb2_grpc.HandleDataStub(channel)
        response = stub.GD(chord_pb2.StarterWithData(
            node_key=starter_node.key, node_address=starter_node.value,
            data_key=data.key, data_value=data.value,
            data_handling_type=data_handling_type
        ))
    return response.pong


class HealthCheckService(chord_pb2_grpc.HealthCheckerServicer):
    def __init__(self, node_table):
        self.node_table = node_table

    def Check(self, request, context):
        return chord_pb2.HealthReply(pong=0)


class GetNodeValueService(chord_pb2_grpc.GetNodeValueServicer):
    def __init__(self, node_table):
        self.node_table = node_table

    def GetNodeVal(self, request, context):
        if request.which_node == n.predecessor:
            return chord_pb2.NodeVal(
                node_key=self.node_table.predecessor.key, node_address=self.node_table.predecessor.value
            )
        else:
            node_data = self.node_table.finger_table.entries[request.which_node]
            key = node_data.key
            value = node_data.value
            return chord_pb2.NodeVal(node_key=key, node_address=value)


class NotifyNodeService(chord_pb2_grpc.NotifyNodeServicer):
    def __init__(self, node_table):
        self.node_table = node_table

    def NotifyNodeChanged(self, request, context):
        if request.which_node == n.predecessor:
            self.node_table.predecessor.update_info(request.node_key, request.node_address, -1)
        else:
            self.node_table.finger_table.entries[request.which_node].update_info(
                request.node_key, request.node_address, request.which_node
            )
        return chord_pb2.HealthReply(pong=0)


class TossMessageService(chord_pb2_grpc.TossMessageServicer):
    def __init__(self, node_table):
        self.node_table = node_table

    def notify_new_node_income(self, new_node: Data):
        # 본인이 새로운 노드를 추가해야 할 때 -> 본인의 successor 로 추가해야 할 때 처리방식

        # 1. 현재 본인의 기존 successor 에게, 새로운 노드가 predecessor 라고 알려줌
        notify_node_info(self.node_table.finger_table.entries[n.successor], new_node, n.predecessor)

        # 2. 새 노드의 predecessor 를 본인으로,
        #    새 노드의 successor 를 본인의 기존 successor 로,
        #    새 노드의 double_successor 를 본인의 기존 double_successor 로 설정함
        #    추후에 finger table 을 사용할 때는, 반복문을 돌면서 그냥 finger table 자체를 할당해주면 됨.
        notify_node_info(new_node, self.node_table.cur_node, n.predecessor)
        notify_node_info(new_node, self.node_table.finger_table.entries[n.successor], n.successor)
        notify_node_info(new_node, self.node_table.finger_table.entries[n.d_successor], n.d_successor)

        # 3. 본인의 double successor 를 기존 successor 로, successor 를 새로운 노드로 업데이트
        self.node_table.finger_table.entries[n.d_successor].update_info(
            self.node_table.finger_table.entries[n.succssor].key, self.node_table.finger_table.entries[n.successor].value,
            n.d_successor
        )
        self.node_table.finger_table.entries[n.successor].update_info(new_node, n.successor)

        # 4. 본인의 predecessor 에게, double successor 가 새로운 노드임을 알려줌
        #    추후에 finger table을 사용할 때, 반복문을 돌면서 처리할 수는 있을거같음.
        threading.Thread(target=notify_node_info,
                         args=(
                             self.node_table.predecessor, new_node, n.finger_table(1),)
                         ).start()

    def TM(self, request, context):
        logging.debug(f'Toss Message received from {request.node_address}')
        if request.message_type == t.join_node:
            # 만약 join일 시, finger table 에서의 insert 위치를 찾아본다.

            # 1. 본인의 key값보다 크고, successor (finger_table[0]) 의 key 값보다 작은 경우는, 내가 추가한다.
            if self.node_table.cur_node.key < request.node_key < self.node_table.finger_table.entries[n.successor].key or \
                    self.node_table.finger_table.entries[n.successor].key < self.node_table.cur_node.key < request.node_key:
                logging.info(f'Now Adding {request.node_address}...')
                self.notify_new_node_income(new_node=Data(request.node_key, request.node_address))
            # 2. 아닐 경우에는, 노드 테이블을 순회하면서 적절히 보낼 위치를 찾는다.
            # -> 일단 지금은, 바로 successor 에게 넘긴다. (finger table 의 속성을 변경하는 작업이 필요함)
            else:
                logging.info(
                    f'Passing {request.node_address}`s message to {self.node_table.finger_table.entries[n.successor].value}')
                threading.Thread(target=toss_message,
                                 args=(
                                     Data(request.node_key, request.node_address),
                                     self.node_table.finger_table.entries[n.successor],
                                     request.message_type)
                                 ).start()
                # send_node = False
                # for i in range(len(self.finger_table.entries) - 1):
                #     if self.finger_table.entries[i].key < request.node_key < self.finger_table.entries[i + 1].key:
                #         send_node = self.finger_table.entries[i]
                #         break
                # if not send_node and self.finger_table.entries[-1].key < request.node_key:
                #     send_node = self.finger_table.entries[-1]
                #
                # threading.Thread(target=toss_message,
                #                  args=(Data(request.node_key, request.node_address), send_node,))
            return chord_pb2.HealthReply(pong=0)

        # 만약에 메시지 타입이 finger table을 업데이트하는 메시지라면
        if request.message_type == t.finger_table_setting:
            logging.debug(f'received finger table update message : {request.node_key}. {request.node_address}, {request.message}')

            # 만약 받은 요청의 node key와 자신의 key가 같다면 (순회를 마쳤다면)
            if request.node_key == self.node_table.cur_node.key:
                logging.debug("finished receiving update message")

                # 현재 네트워크의 노드 수를 갱신해준 후 종료
                self.node_table.node_network_num = request.message
                return chord_pb2.HealthReply(pong=0)

            # 만약 받은 요청의 node_type가 join_node 라면 (새로운 node가 join되었으면)
            if request.node_type == t.join_node:

                # 현재 노드의 네트워크에 존재하는 노드개수 변수를 1 증가시킴
                self.node_table.node_network_num += 1

            # 만약 받은 요청의 node_type가 left_node 라면 (노드가 나간다면)
            if request.node_type == t.left_node:

                # 현재 노드의 네트워크에 존재하는 노드개수 변수를 1 감소시킴
                self.node_table.node_network_num -= 1

                logging.debug("sending update message complete, pass to successor")
                threading.Thread(target=toss_message,
                                 args=(
                                     Data(request.node_key, request.node_address),
                                     self.node_table.finger_table.entries[n.successor],
                                     request.message_type,
                                     request.message)
                                 ).start()
                return chord_pb2.HealthReply(pong=0)



            cur_node_num = int(request.message)
            cur_finger_table_num = math.log2(cur_node_num)

            # 만약 현재 메시지 수가 2의 배수라면 (1 포함)
            if cur_finger_table_num - int(cur_finger_table_num) == 0:

                # 원본에게 finger table을 업데이트하도록 설정
                # 이 요청이 끝나야 계속 가도록 설정
                return_val = toss_message(
                    self.node_table.cur_node,
                    Data(request.node_key, request.node_address),
                    t.receive_finger_data,
                    int(cur_finger_table_num)
                )
                logging.debug(f"send res : {return_val}")

                # 만약 원본 노드가 응답이 없으면 (연결이 끊겼으면), 메시지를 끊음
                if return_val is False:
                    logging.debug(f"starter node network error, will end toss message here")
                    return chord_pb2.HealthReply(pong=0)

            # 만약 어떤 사유로 노드 네트워크를 4번 이상 순회했는데도 여전히 돈다면, 네트워크가 끊어짐을 알림
            if cur_node_num > 4 * self.node_table.node_network_num:
                logging.info("CRITICAL! network is corrupted. end this toss message")
                return chord_pb2.HealthReply(pong=0)

            # 자신이 처리할 일이 끝났으면, 이 요청을 그대로 자신의 successor에게 전송
            logging.debug("sending update message complete, pass to successor")
            threading.Thread(target=toss_message,
                             args=(
                                 Data(request.node_key, request.node_address),
                                 self.node_table.finger_table.entries[n.successor],
                                 request.message_type,
                                 request.message + 1)
                             ).start()
            return chord_pb2.HealthReply(pong=0)

        # 만약 자신의 finger table을 업데이트하는 요청이 왔을 때
        if request.message_type == t.receive_finger_data:
            logging.debug(f'received finger data : {request.node_key}. {request.node_address}, {request.message}')

            # 해당 finger table index가 존재하면 쌓게끔 함
            try:
                self.node_table.finger_table.entries[request.message].update_info(
                    request.node_key, request.node_address, request.message
                )

            # 만약 인덱스가 존재하지 않을 경우, 없는 것만큼 넣어준 다음 append
            except IndexError:
                # 실제 들어가야하는 인덱스번호
                index = request.message

                # Finger Table 길이
                fingers = len(self.node_table.finger_table.entries)

                # 괴리율 (몇 개가 들어가야하는지)
                while fingers != index:
                    self.node_table.finger_table.append("Dummy", "Dummy")
                    index += 1
                self.node_table.finger_table.append(request.node_key, request.node_address)
            logging.debug("done processing")
            return chord_pb2.HealthReply(pong=0)

class HandleDataService(chord_pb2_grpc.HandleDataServicer):
    def __init__(self, node_table, data_table: TableEntry):
        self.node_table = node_table
        self.data_table = data_table

    def get(self, starter_node: Data, req_data: Data):
        try:
            value = self.data_table.get(req_data.key).value
        except ValueError:
            value = ""

        threading.Thread(
            target=data_request,
            args=(
                self.node_table.cur_node,
                starter_node,  # Finger Table 구현되면 수정 필요
                Data(req_data.key, value),
                d.get_result)
        ).start()

    def GD(self, request, context):
        job_type = request.data_handling_type
        starter_node = Data(request.node_key, request.node_address)
        data = Data(request.data_key, request.data_value)

        cur_key = self.node_table.cur_node.key
        successor_key = self.node_table.finger_table.entries[n.successor].key

        if job_type == d.get_result:
            if data.value == "":
                data.value = "not found"
            logging.info(f"request key:{data.key[:10]}'s value is {data.value}, stored in {starter_node.value}")

        elif cur_key <= data.key < successor_key or successor_key < cur_key <= data.key or data.key < successor_key < cur_key:
            if job_type == d.get:
                self.get(starter_node, data)
            if job_type == d.set:
                self.data_table.set(data)
                logging.info(
                    f"request key:{data.key[:10]}'s value is set to {data.value}, stored in {self.node_table.cur_node.value}")
            if job_type == d.delete:
                self.data_table.delete(data.key)
                logging.info(f"request key:{data.key[:10]} is deleted from {self.node_table.cur_node.value}")
        else:
            threading.Thread(
                target=data_request,
                args=(
                    starter_node,
                    self.node_table.finger_table.entries[0],  # Finger Table 구현되면 수정 필요
                    data,
                    job_type)
            ).start()
        return chord_pb2.HealthReply(pong=0)
