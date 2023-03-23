from utils import my_sorted


def test_my_sorted():
    lst = [0, 4, 2, 12, 23]
    assert my_sorted(lst) == [0, 2, 4, 12, 23]
    assert my_sorted(lst, reverse=True) == [23, 12, 4, 2, 0]
    assert my_sorted(lst, key=lambda x: -x) == [23, 12, 4, 2, 0]
    assert my_sorted(lst, key=lambda x: -x, reverse=True) \
           == [0, 2, 4, 12, 23]
