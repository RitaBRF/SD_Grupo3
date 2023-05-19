import socket
import logging
from GameMechanics import GameMech
import CONSTANT


class SkeletonServer:

    def __init__(self, gm_obj: GameMech):
        self.gm = gm_obj
        self.s = socket.socket()
        self.s.bind((CONSTANT.ENDERECO_SERVIDOR, CONSTANT.PORTO))
        self.s.listen()

    def process_x_max(self, s_c):
        # pedir ao gm o tamanho do jogo
        x_max = self.gm.get_x_max()
        # enviar a mensagem com esse valor
        s_c.send(x_max.to_bytes(CONSTANT.N_BYTES, byteorder="big", signed=True))

    def process_y_max(self, s_c):
        # pedir ao gm o tamanho do jogo
        y_max = self.gm.get_y_max()
        # enviar a mensagem com esse valor
        s_c.send(y_max.to_bytes(CONSTANT.N_BYTES, byteorder="big", signed=True))

    def process_direction(self, s_c, direction, nr_player):
        if direction == CONSTANT.MOVE_UP:
            self.gm.execute(1, "player", int(nr_player))
        elif direction == CONSTANT.MOVE_RIGHT:
            self.gm.execute(2, "player", int(nr_player))
        elif direction == CONSTANT.MOVE_DOWN:
            self.gm.execute(3, "player", int(nr_player))
        elif direction == CONSTANT.MOVE_LEFT:
            self.gm.execute(4, "player", int(nr_player))

    def run(self):
        logging.info("a escutar no porto " + str(CONSTANT.PORTO))
        socket_client, address = self.s.accept()
        logging.info("o cliente com endereço " + str(address) + " ligou-se!")

        msg: str = ""
        fim = False
        while fim == False:
            dados_recebidos: bytes = socket_client.recv(CONSTANT.COMMAND_SIZE)
            msg = dados_recebidos.decode(CONSTANT.CODIFICACAO_STR)
            # logging.debug("o cliente enviou: \"" + msg + "\"")

            if msg == CONSTANT.X_MAX:
                self.process_x_max(socket_client)
            elif msg == CONSTANT.Y_MAX:
                self.process_y_max(socket_client)
            elif msg == CONSTANT.CHANGE_DIR:
                dados_recebidos: bytes = socket_client.recv(CONSTANT.COMMAND_SIZE)
                direction = dados_recebidos.decode(CONSTANT.CODIFICACAO_STR)
                dados_recebidos: bytes = socket_client.recv(CONSTANT.COMMAND_SIZE_INT)
                nr_player = dados_recebidos.decode(CONSTANT.CODIFICACAO_STR)
                self.process_direction(socket_client, direction, nr_player)

            # TODO: continuar a partir daqui com as funcionalidades do GM
            elif msg == CONSTANT.END:
                socket_client.send(CONSTANT.END.encode(CONSTANT.CODIFICACAO_STR))
                fim = True

        socket_client.close()
        logging.info("o cliente com endereço o " + str(address) + " desligou-se!")
        self.s.close()


logging.basicConfig(filename=CONSTANT.NOME_FICHEIRO_LOG,
                    level=CONSTANT.NIVEL_LOG,
                    format='%(asctime)s (%(levelname)s): %(message)s')
