from utils.data import fetch


class IngredientRange:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

        self.range = range(self.start, self.end + 1)

    @property
    def size(self) -> int:
        return self.end - self.start + 1

    def is_fresh(self, ingredient: int) -> bool:
        return self.start <= ingredient <= self.end

    @classmethod
    def from_line(cls, line: str) -> "IngredientRange":
        start_str, end_str = line.split("-")
        return cls(int(start_str), int(end_str))


class Recipe:
    def __init__(self, ingredient_ranges: list[IngredientRange]):
        self.ingredient_ranges = ingredient_ranges

        self._ranges = []

    def is_fresh(self, ingredient: int) -> bool:
        for ingredient_range in self.ingredient_ranges:
            if ingredient_range.is_fresh(ingredient):
                return True
        return False

    def merge_ranges(self) -> list[IngredientRange]:
        if not self.ingredient_ranges:
            return []

        sorted_ranges = sorted(self.ingredient_ranges, key=lambda r: r.start)

        merged = [sorted_ranges[0]]
        for current_range in sorted_ranges[1:]:
            last_merged = merged[-1]

            if current_range.start <= last_merged.end + 1:
                if current_range.end > last_merged.end:
                    merged[-1] = IngredientRange(last_merged.start, current_range.end)
            else:
                merged.append(current_range)

        return merged


data = fetch(day=5)

ingredient_ranges = []
raw_ranges = []
for _, line in enumerate(data):
    if line == "":
        break
    raw_ranges.append(line)
    ingredient_ranges.append(IngredientRange.from_line(line))

recipe = Recipe(ingredient_ranges)
all_ranges = recipe.merge_ranges()

count = 0
for _range in all_ranges:
    count += _range.size

print(f"Number of valid ingredients: {count}")
