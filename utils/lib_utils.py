class FlowMatrix:
    def __init__(self, row_length: int):
        if row_length <= 0:
            raise AttributeError("Row length must be >=1")
        self._row_width = row_length
        self._list: list[list] = []

    @property
    def list(self):
        return self._list

    def append(self, element):
        self._create_cell_if_necessary()
        self._list[-1].append(element)

    def is_empty(self):
        return len(self._list) == 0

    def _create_cell_if_necessary(self):
        if self.is_empty() or self._row_is_full():
            self._list.append([])

    def _row_is_full(self):
        return len(self._list[-1]) == self._row_width

    @classmethod
    def from_list(cls, ls: list, row_length: int):
        from math import ceil

        rl = row_length
        inner_cells_qnt = ceil(len(ls) / rl)
        matrix = cls(row_length)
        matrix._list = [
            [x for x in ls[j * rl:(j + 1) * rl]]
            for j in range(inner_cells_qnt)
        ]
        return matrix
