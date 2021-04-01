import math
_allowed_directions = ["N", "W", "S", "E"]
_shift_vector_at_direction = {
    "N": (0, +1),
    "W": (-1, 0),
    "S": (0, -1),
    "E": (+1, 0)
}
MIN_X = 0
MIN_Y = 0
MAX_X = 99
MAX_Y = 99


class Explosion(Exception):
    pass


class Rover:
    def __init__(self, x, y, direction):
        if direction not in _allowed_directions:
            raise Explosion
        if (x < MIN_X) or (x > MAX_X) or (y < MIN_Y) or (y > MAX_Y):
            raise Explosion
        self.position = (x, y)
        self.direction = direction

    def execute_commands_stream(self, commands_stream):
        for command in commands_stream:
            self._execute_command(command)

    def _execute_command(self, command):
        _command_to_atomic_move = {
            'f': self._move_forward,
            'b': self._move_backward,
            'l': self._turn_left,
            'r': self._turn_right
        }
        atomic_move = _command_to_atomic_move[command]
        atomic_move()

    def _move_forward(self):
        (x, y) = self.position
        (dx, dy) = _shift_vector_at_direction[self.direction]
        self.position = (x + dx, y + dy)
        self._wrap_position_at_map_edge()

    def _wrap_position_at_map_edge(self):
        if self.position[1] > MAX_Y:
            self.position = (self.position[0], MIN_Y)
        elif self.position[1] < MIN_Y:
            self.position = (self.position[0], MAX_Y)
        elif self.position[0] < MIN_X:
            self.position = (MAX_X, self.position[1])
        elif self.position[0] > MAX_X:
            self.position = (MIN_X, self.position[1])

    def _move_backward(self):
        self._turn_right()
        self._turn_right()
        self._move_forward()
        self._turn_right()
        self._turn_right()

    def _turn_right(self):
        if self.direction == "N":
            self.direction = "E"
        elif self.direction == "W":
            self.direction = "N"
        elif self.direction == "S":
            self.direction = "W"
        elif self.direction == "E":
            self.direction = "S"

    def _turn_left(self):
        self._turn_right()
        self._turn_right()
        self._turn_right()
