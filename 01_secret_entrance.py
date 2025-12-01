from utils.data import fetch

DIAL_SIZE = 100


class Dial:
    def __init__(self, start_position: int = 0):
        self.position = start_position

        self._counter = 0

    def turn(self, input: str):
        steps = int(input[1:])
        direction = input[0]

        step_sign = 1 if direction == "R" else -1

        self._counter += steps // DIAL_SIZE

        new_position = self.position + (steps % DIAL_SIZE) * step_sign
        crossed_boundary = new_position <= 0 or new_position >= DIAL_SIZE
        if self.position != 0 and crossed_boundary:
            self._counter += 1

        self.position = new_position % DIAL_SIZE

        print(f"Moved {direction}{steps} to {self.position}, count: {self._counter}")

    def get_password(self) -> int:
        return self._counter


data = fetch(day=1)

dial = Dial(50)
for line in data:
    dial.turn(line)

print(f"Dial password: {dial.get_password()}")
print(f"Dial final position: {dial.position}")
