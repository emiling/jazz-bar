import grpc
from grpc._channel import _InactiveRpcError
import threading
import logging
from concurrent import futures
from service import HealthCheckService, GetNodeValueService, NotifyNodeService, TossMessageService, node_health_check, notify_node_info, request_node_info, toss_message
from data_structure import Node

from utils import generate_hash

from protos.output import chord_pb2
from protos.output import chord_pb2_grpc

import time




class TableEntry:
    """
    자동정렬된 List를 가지고 있는 class
    구현해야하는 함수
    1. append : 리스트에 자동 정렬해서 값을 넣음
    2. find (or find_nearest) : 요청한 값에 가장 가까운 value를 찾아줌
    3. update (or modify) : Finger Table 하나의 값을 삭제 혹은 변경
    """
    pass

class ChordNode(Node):
    """
    id : int
    host : string
    port : string
    service : Service
    server : grpc.server
    finger table과 data table은 별도의 class로 관리
    해당 class는 자동 정렬 기능이 있는 list를 담고 있음
    predecessor: Node
    """
    def __init__(self, host, port):
        self.id = generate_hash(host, port)
        print(self.id, type(self.id))
        super().__init__(self.id, host, port)
        self.server = None
        # self.predecessor = Node(self.id, self.host, self.port, "predecessor")
        # # self.successor = Node(self.id, self.host, self.port)
        # self.successor = Node(self.id, self.host, "50053", "successor")
        # self.double_successor = Node(self.id, self.host, self.port, "double_successor")
        # for testing
        if port == "50051":
            self.predecessor = Node("0b03a4d8a7d8f8f4c7afae9aeda7d76b431f4cba", self.host, "50054", "predecessor")
            self.successor = Node("0b03a4d8a7d8f8f4c7afae9aeda7d76b431f4cba", self.host, "50054", "successor")
            self.double_successor = Node(self.id, self.host, self.port, "double_successor")
        if port == "50052" or port == "50053":
            self.predecessor = Node(self.id, self.host, self.port, "predecessor")               # for testing join (join localhost:50053)
            self.successor = Node(self.id, self.host, self.port, "successor")
            self.double_successor = Node(self.id, self.host, self.port, "double_successor")
            # self.predecessor = Node(self.id, self.host, "50051", "predecessor")
            # self.successor = Node(self.id, self.host, "50053", "successor")
            # self.double_successor = Node(self.id, self.host, "50054", "double_successor")
        # if port == "50053":
        #     self.predecessor = Node(self.id, self.host, "50051", "predecessor")
        #     self.successor = Node(self.id, self.host, "50054", "successor")
        #     self.double_successor = Node(self.id, self.host, "50051", "double_successor")
        if port == "50054":
            self.predecessor = Node("a09b0ce42948043810a1f2cc7e7079aec7582f29", self.host, "50051", "predecessor")
            self.successor = Node("a09b0ce42948043810a1f2cc7e7079aec7582f29", self.host, "50051", "successor")
            self.double_successor = Node(self.id, self.host, self.port, "double_successor")
        self.node_table = [self.predecessor, self.successor, self.double_successor]
        self.for_log = ["predecessor", "sucessor", "double_successor"]

        self.serve()

    # TODO : join 함수 구현 (우선순위 높음)
    def join_cluster(self, join_address):
        join_address = join_address.split(":")
        new_node = Node("will replaced", join_address[0], join_address[1])
        toss_message(self, new_node, 1)

    def log_nodes(self):
        for node in self.node_table:
            logging.info(f'current {node.name} : {node.id[:10]}:{node.get_address()}')
        print()

    def health_check(self):
        self.log_nodes()
        while True:

            time.sleep(3)

            if node_health_check(self.predecessor):                             # predecessor가 접속되지 않는다면, 변경 요청이 오기 때문에 신경쓰지 않아도 됨
                pass

            if not node_health_check(self.successor):                           # successor가 접속되지 않는다면,
                logging.info(f'successor is out of connection, change to {self.double_successor.get_address()}')
                self.successor.update_info(self.double_successor.id, self.double_successor.host, self.double_successor.port)
                                                                                # double successor를 successor로 교체 후에
                notify_node_info(self, self.successor, 0)                       # successor에게 본인이 successor의 predecessor라고 알려줌

                d_id, d_host, d_port = request_node_info(self.successor, 1)     # 이후, successor에게 successor를 물어보고
                self.double_successor.update_info(d_id, d_host, d_port)         # 그 값을 double_successor에 저장함

                self.log_nodes()

            if not node_health_check(self.double_successor):                    # 만약 double_successor가 접속되지 않는다면
                logging.info("double successor is out of connection")
                s_id, s_host, s_port = request_node_info(self.successor, 2)     # successor의 successor를 물어보고
                self.double_successor.update_info(s_id, s_host, s_port)         # 그 값을 double_successor에 저장

                self.log_nodes()


    # TODO : Get/Set/Remove/Join에 대한 핸들링 추가 및 프로토콜 결정 (우선순위 높음)
    def command_handler(self, command):
        commands = command.split()

        if commands[0] == 'get':
            print("GETGET")
        elif commands[0] == 'set':
            pass
        elif commands[0] == 'remove':
            pass
        elif commands[0] == 'join':
            self.join_cluster(commands[1])

    def listen_command(self):
        try:
            while True:
                command = input("> ")
                self.command_handler(command)
        except KeyboardInterrupt:
            print('Terminated By User')
            self.server.stop(0)



    def serve(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        # 이 부분이 server
        chord_pb2_grpc.add_HealthCheckerServicer_to_server(HealthCheckService(self), self.server)
        chord_pb2_grpc.add_GetNodeValueServicer_to_server(GetNodeValueService(self), self.server)
        chord_pb2_grpc.add_NotifyNodeServicer_to_server(NotifyNodeService(self), self.server)
        chord_pb2_grpc.add_TossMessageServicer_to_server(TossMessageService(self), self.server)

        address = self.host+":"+self.port
        self.server.add_insecure_port(address)
        self.server.start()

        logging.info(f'ChordServer is listening on {self.host}:{self.port}')
        # self.server.wait_for_termination()

        # input thread
        health_checker = threading.Thread(target=self.health_check)
        command_listener = threading.Thread(target=self.listen_command)
        health_checker.start()
        command_listener.start()


