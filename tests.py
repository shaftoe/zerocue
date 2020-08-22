from io import BytesIO
import pytest

from zerocue import CueTime, CueError, create_new_cue


@pytest.mark.parametrize(
    "first, second, result",
    [
        (CueTime(0, 0, 0), CueTime(0, 0, 0), CueTime(0, 0, 0)),
        (CueTime(-0, -0, -0), CueTime(0, 0, 0), CueTime(0, 0, 0)),
        (CueTime(-0, -0, -0), CueTime(-0, -0, -0), CueTime(0, 0, 0)),
        (CueTime(-0, -0, -0), CueTime(-0, -0, -0), CueTime(-0, -0, -0)),
        (CueTime(1, 0, 0), CueTime(0, 0, 1), CueTime(0, 59, 74)),
        (CueTime(134, 34, 27), CueTime(35, 5, 26), CueTime(99, 29, 1)),
        (CueTime(1, 0, 0), CueTime(0, 0, 74), CueTime(0, 59, 1)),
        (CueTime(5, 10, 10), CueTime(4, 0, 73), CueTime(1, 9, 12)),
    ]
)
def test_cuetime_subtraction(first, second, result):
    assert first - second == result


@pytest.mark.parametrize(
    "invalid_values",
    [
        ("a", "b", "c"),
        ("-1", "0", "0"),
        ("0", "-1", "0"),
        ("0", "0", "-1"),
        (None, 1, 7),
        (0, 60, 7),
        (0, 0, 75),
        (0, 0, 100),
        (-1, 0, 0),
        (0, -1, 0),
        (0, 0, -1),
    ]
)
def test_cuetime_raises_exceptions(invalid_values):
    with pytest.raises(CueError):
        CueTime(*invalid_values)


def test_create_new_cue():
    with open("data/example.cue", "rb") as source, \
            open("data/example_zeroed.cue", "rb") as target, \
            BytesIO() as temp:
        create_new_cue(source, temp)
        temp.seek(0)
        assert temp.read() == target.read()
