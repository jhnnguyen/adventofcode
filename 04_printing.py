from typing import Literal

from utils.data import fetch

ROLL_SYMBOL = "@"
ROLL_THRESHOLD = 4


class Grid:
    def __init__(self, grid: list[str]):
        _grid = [list(row) for row in grid]

        self._starting_grid = [row.copy() for row in _grid]
        self._grid = [row.copy() for row in _grid]

        self.rows = len(_grid)
        self.cols = len(_grid[0])

    def is_accessible(self, x: int, y: int) -> bool:
        surroundings = self._get_surroundings(x, y)

        surrounding_rolls = [
            roll for roll in surroundings.values() if roll == ROLL_SYMBOL
        ]

        return len(surrounding_rolls) < ROLL_THRESHOLD

    def get_accessible_rolls(self) -> list[tuple[int, int]]:
        accessible_rolls = []
        for y in range(self.rows):
            for x in range(self.cols):
                if self.get_value(x, y) == ROLL_SYMBOL and self.is_accessible(x, y):
                    accessible_rolls.append((x, y))
        return accessible_rolls

    def _remove_roll(self, x: int, y: int) -> None:
        if self.get_value(x, y) == ROLL_SYMBOL:
            self._grid[y][x] = "."

    def remove_rolls(self, rolls: list[tuple[int, int]]) -> None:
        for x, y in rolls:
            self._remove_roll(x, y)

    def _get_surroundings(self, x: int, y: int) -> dict[str, str | None]:
        directions = {
            "up": (x, y + 1),
            "down": (x, y - 1),
            "left": (x - 1, y),
            "right": (x + 1, y),
            "up_left": (x - 1, y + 1),
            "up_right": (x + 1, y + 1),
            "down_left": (x - 1, y - 1),
            "down_right": (x + 1, y - 1),
        }
        surroundings = {}
        for direction, (dx, dy) in directions.items():
            surroundings[direction] = self.get_value(dx, dy)
        return surroundings

    def get_value(self, x: int, y: int) -> str | None:
        if y < 0 or y >= self.rows or x < 0 or x >= self.cols:
            return None
        return self._grid[y][x]

    def print_grid(self, type: Literal["starting", "grid"] = "grid") -> None:
        match type:
            case "grid":
                for row in self._grid:
                    print("".join(row))
            case _:
                for row in self._starting_grid:
                    print("".join(row))


data = fetch(day=4)
grid = Grid(data)

max_iteration = 500
removed_rolls = 0
for _ in range(max_iteration):
    accessible_rolls = grid.get_accessible_rolls()
    if not accessible_rolls:
        break
    removed_rolls += len(accessible_rolls)
    grid.remove_rolls(accessible_rolls)

print(f"Total removed rolls: {removed_rolls}")
