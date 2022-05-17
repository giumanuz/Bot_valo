from pytest import raises, mark

from utils.lib_utils import FlowMatrix


def test_startsEmpty():
    mat = FlowMatrix(row_length=1)
    assert len(mat.list) == 0
    mat = FlowMatrix(row_length=2)
    assert len(mat.list) == 0


def test_addsInitialElement():
    mat = FlowMatrix(row_length=2)
    mat.append(4)
    assert len(mat.list) == 1
    assert mat.list[0] == [4]


def test_ifRowNotFull_AddsElementInSameRow():
    mat = FlowMatrix(row_length=3)
    mat.append(2)
    mat.append(3)
    assert len(mat.list) == 1
    assert mat.list[0] == [2, 3]
    mat.append(4)
    assert len(mat.list) == 1
    assert mat.list[0] == [2, 3, 4]


def test_ifRowIsFull_AddsElementInNewRow():
    mat = FlowMatrix(row_length=2)
    mat.append(2)
    mat.append(3)
    mat.append(4)
    assert len(mat.list) == 2
    assert mat.list[0] == [2, 3]
    assert mat.list[1] == [4]

    mat = FlowMatrix(row_length=1)
    mat.append(2)
    mat.append(3)
    mat.append(4)
    assert len(mat.list) == 3
    assert mat.list[0] == [2]
    assert mat.list[1] == [3]
    assert mat.list[2] == [4]


@mark.parametrize('row_length', (0, -1, -2))
def test_ifRowLengthLessThanOne_WillRaiseError(row_length):
    with raises(AttributeError) as e:
        FlowMatrix(row_length=row_length)
    assert "Row length must be >=1" in str(e.value)


def test_matrixFromList():
    ls = [1, 2, 3, 4]
    mat = FlowMatrix.from_list(ls, row_length=1)
    assert mat.list == [[1], [2], [3], [4]]
    mat = FlowMatrix.from_list(ls, row_length=2)
    assert mat.list == [[1, 2], [3, 4]]
    mat = FlowMatrix.from_list(ls, row_length=3)
    assert mat.list == [[1, 2, 3], [4]]
    mat = FlowMatrix.from_list(ls, row_length=4)
    assert mat.list == [[1, 2, 3, 4]]
    mat = FlowMatrix.from_list(ls, row_length=5)
    assert mat.list == [[1, 2, 3, 4]]


def test_matrixFromLongerList():
    ls = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    mat = FlowMatrix.from_list(ls, row_length=2)
    assert mat.list == [[1, 2], [3, 4], [5, 6], [7, 8], [9]]
    mat = FlowMatrix.from_list(ls, row_length=3)
    assert mat.list == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    mat = FlowMatrix.from_list(ls, row_length=4)
    assert mat.list == [[1, 2, 3, 4], [5, 6, 7, 8], [9]]
    mat = FlowMatrix.from_list(ls, row_length=5)
    assert mat.list == [[1, 2, 3, 4, 5], [6, 7, 8, 9]]
