# adaptado do ficheiro game_mech disponibilizado nas aulas de laboratório

import time

# definir as constantes para movimento e paço
MOVE_UP = 1
MOVE_RIGHT = 2
MOVE_DOWN = 3
MOVE_LEFT = 4

TYPE_APPLE = "a"
TYPE_BODY = "b"

TIME_STEP = 7


class GameMech:

    def __init__(self, x_max: int = 20, y_max: int = 20):
        """
        Construtor da classe GameMech. Criação dos dicionários e listas que guardam a informação sobre o mundo.
        """

        self.x_max = x_max
        self.y_max = y_max

        self.players = dict()
        self.obstacles = dict()
        self.nr_players = 0
        self.nr_obstacles = 0

        self.world = dict()

        # criar chaves no dicionário "world" para cada casa e listas vazias como valor correspondente
        for x in range(self.x_max):
            for y in range(self.y_max):
                self.world[(x, y)] = []

    def add_obstacle(self, obs_type: str, x_pos: int, y_pos: int) -> bool:
        """
        Adicionar um novo obstáculo ao mundo.
        """
        nr_obstacle = self.nr_obstacles
        self.obstacles[nr_obstacle] = [obs_type, (x_pos, y_pos)]
        self.world[(x_pos, y_pos)].append(['obstacle', obs_type, nr_obstacle, (x_pos, y_pos)])
        self.nr_obstacles += 1
        return True

    def find_obstacle(self, obs_type, x, y):
        """
        Conferir se uma casa possui um elemento obstáculo de um certo tipo e retorná-lo.
        """
        for e in self.world[(x, y)]:
            if e[0] == 'obstacle' and e[1] == obs_type:
                return e
        return None

    def lose_game(self):
        """
        Jogador colide com um obstáculo do tipo 'corpo'. Perde o jogo.
        """
        pass

    def eat_apple(self, apple, nr_player):
        """
        Jogador colide com um obstáculo do tipo 'maçã'.
        """
        # destruir a macã
        posx = apple[3][0]
        posy = apple[3][1]
        nr_obstacle = apple[2]
        self.obstacles[nr_obstacle] = []
        self.world[(posx, posy)].remove(['obstacle', TYPE_APPLE, nr_obstacle, (posx, posy)])
        self.nr_obstacles -= 1
        # dar ponto ao jogador
        self.players[nr_player][4] += 1
        # aumentar tamanho do jogador

    def add_player(self, name, x_pos: int, y_pos: int) -> int:
        """
        Adicionar um novo jogador ao mundo.
        """
        nr_player = self.nr_players

        tick = int(time.time())

        self.players[nr_player] = [name, (x_pos, y_pos), tick, MOVE_RIGHT, 0]
        self.world[(x_pos, y_pos)].append(['player', name, nr_player, (x_pos, y_pos)])
        self.nr_players += 1

        return nr_player

    def remove_player(self, nr_player) -> int:
        """
        Remover um jogador do mundo.
        """
        if nr_player <= self.nr_players:
            name = self.players[nr_player][0]
            x_pos, y_pos = self.players[nr_player][1][0], self.players[nr_player][1][1]
            self.world[(x_pos, y_pos)].remove(['player', name, nr_player, (x_pos, y_pos)])
            self.players[nr_player] = []
        return nr_player

    def move_player(self, nr_player) -> tuple:
        """
        Mover o jogador
        """
        name = self.players[nr_player][0]
        pos_x, pos_y = self.players[nr_player][1][0], self.players[nr_player][1][1]
        tick = self.players[nr_player][2]
        direction = self.players[nr_player][3]
        points = self.players[nr_player][4]
        new_pos_x = pos_x
        new_pos_y = pos_y
        if direction == MOVE_LEFT:
            new_pos_x = pos_x - 1
            new_pos_y = pos_y
        elif direction == MOVE_RIGHT:
            new_pos_x = pos_x + 1
            new_pos_y = pos_y
        elif direction == MOVE_UP:
            new_pos_y = pos_y - 1
            new_pos_x = pos_x
        elif direction == MOVE_DOWN:
            new_pos_y = pos_y + 1
            new_pos_x = pos_x

        self.players[nr_player] = [name, (new_pos_x, new_pos_y), tick, direction, points]
        world_pos = self.world[(pos_x, pos_y)]
        world_pos.remove(['player', name, nr_player, (pos_x, pos_y)])
        self.world[(pos_x, pos_y)] = world_pos
        self.world[(new_pos_x, new_pos_y)].append(['player', name, nr_player, (new_pos_x, new_pos_y)])

        return new_pos_x, new_pos_y

    # ------- Métodos "Getter" ----------------------------------------------------------------------------------

    def get_players(self):
        return self.players

    def get_obstacles(self):
        return self.obstacles

    def get_nr_obstacles(self):
        return self.nr_obstacles

    def get_nr_players(self):
        return self.nr_players

    def get_x_max(self):
        return self.x_max

    def get_y_max(self):
        return self.y_max

    # ------- Métodos "Print" ------------------------------------------------------------------------------------

    def print_players(self):
        for p in self.players:
            print("Nr. ", p)
            print("Value:", self.players[p])

    def print_pos(self, x: int, y: int):
        print("(x= ", x, ", y=", y, ") =", self.world[(x, y)])

    def print_world(self):
        for i in range(self.x_max):
            for j in range(self.y_max):
                print("(", i, ",", j, ") =", self.world[(i, j)])

    # ------------------------------------------------------------------------------------------------------------

    def execute(self, move: int, type: str, nr_player: int) -> str:
        """
        Ações do jogador condicionadas pelos ticks.
        """
        if type == "player":
            name = self.players[nr_player][0]
            pos_x, pos_y = self.players[nr_player][1][0], self.players[nr_player][1][1]
            tick = self.players[nr_player][2]
            points = self.players[nr_player][4]
            new_direction = move

            next_tick = int(time.time() * TIME_STEP)

            if next_tick > tick:
                tick = next_tick
                self.players[nr_player] = [name, (pos_x, pos_y), tick, new_direction, points]
            else:
                return "Tried to change direction on the same tick"

            return f"**Changed Direction to {new_direction}**"


# Testing the class
if __name__ == '__main__':
    gm = GameMech(10, 10)
    nro_player = gm.add_player('rita', 1, 1)
    print(f"Player created: Player {nro_player}")
    print("Posição Inicial: (1, 1)")

    def move_block():
        a = gm.move_player(nro_player)
        time.sleep(0.7)
        print(a)

    move_block()
    move_block()
    b = gm.execute(MOVE_DOWN, "player", 0)  # vai aplicar
    print(b)
    b = gm.execute(MOVE_LEFT, "player", 0)  # vai ignorar
    print(b)
    move_block()
    move_block()
    b = gm.execute(MOVE_LEFT, "player", 0)  # vai aplicar
    print(b)
    time.sleep(1)
    b = gm.execute(MOVE_UP, "player", 0)  # vai aplicar
    print(b)
    move_block()
    move_block()

    print("VERIFICAÇAO: Print da casa onde o player deve estar:")
    gm.print_pos(3, 1)
