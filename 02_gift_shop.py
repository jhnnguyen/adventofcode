from utils.data import fetch


class ProductID:
    def __init__(self, value: str):
        self._value = value
        self._id_length = len(value)

    def _is_invalid_part_1(self) -> bool:
        # Part 1
        if self._id_length % 2 != 0:
            return False
        return (
            self._value[: self._id_length // 2] == self._value[self._id_length // 2 :]
        )

    def _repeated_chunks(self, chunk_length: int) -> bool:
        chunk = self._value[0:chunk_length]
        equivalent_string = chunk * (self._id_length // chunk_length)
        return equivalent_string == self._value

    def is_invalid(self) -> bool:
        # Part 2 - brute force this baby
        id_length = len(self._value)
        for chunk_length in range(1, id_length // 2 + 1):
            if self._repeated_chunks(chunk_length):
                return True
        return False

    def value(self) -> int:
        return int(self._value)


class ProductIDRange:
    def __init__(self, id_string: str):
        start, end = id_string.split("-")

        self._start = int(start)
        self._end = int(end)

        self._range = range(self._start, self._end + 1)

    def get_invalid_ids(self) -> list[int]:
        invalid_ids = []
        for product_id in self._range:
            product_id_obj = ProductID(str(product_id))
            if product_id_obj.is_invalid():
                invalid_ids.append(product_id)
        return invalid_ids

    def get_invalid_sum(self) -> int:
        invalid_ids = self.get_invalid_ids()
        return sum(invalid_ids)


raw_data = fetch(day=2)
data = raw_data[0].split(",")

total_sum = 0
for _data in data:
    product_id_range = ProductIDRange(_data)
    total_sum += product_id_range.get_invalid_sum()

print(f"Total sum invalid product IDs: {total_sum}")
