import socket
from typing import Union

import CONSTANT


class StubClient:

    def __init__(self):
        self.s: socket = socket.socket()
        self.s.connect((CONSTANT.ENDERECO_SERVIDOR, CONSTANT.PORTO))

    def grid_size(self):
        msg = CONSTANT.X_MAX
        self.s.send(msg.encode(CONSTANT.CODIFICACAO_STR))
        valor = self.s.recv(CONSTANT.N_BYTES)
        x_max = int.from_bytes(valor, byteorder="big", signed=True)

        msg = CONSTANT.Y_MAX
        self.s.send(msg.encode(CONSTANT.CODIFICACAO_STR))
        valor = self.s.recv(CONSTANT.N_BYTES)
        y_max = int.from_bytes(valor, byteorder="big", signed=True)
        return x_max, y_max

    def change_direction(self, direction, nr_player):
        msg = CONSTANT.CHANGE_DIR
        self.s.send(msg.encode(CONSTANT.CODIFICACAO_STR))
        self.s.send(direction.encode(CONSTANT.CODIFICACAO_STR))
        self.s.send(nr_player.encode(CONSTANT.CODIFICACAO_STR))

    def end_connection(self):
        msg = CONSTANT.END
        self.s.send(msg.encode(CONSTANT.CODIFICACAO_STR))
        end = self.s.recv(CONSTANT.COMMAND_SIZE)
        if end.decode(CONSTANT.CODIFICACAO_STR) == CONSTANT.END:
            self.s.close()

