"""
Test for Computer class
Command line: python -m pytest tests/test_computer.py
"""
import pytest

from light_it_game import Computer


@pytest.fixture
def computer_values():
    return {
        "name": "qqqqqqqqqqqqqqqqqqqq",
        "health": 1000,
    }


@pytest.fixture
def computer(computer_values):
    return Computer(**computer_values)


def test_create(computer, computer_values):
    for attr_name in computer_values:
        assert getattr(computer, attr_name) == computer_values.get(attr_name)


@pytest.mark.parametrize(
    "name, ex",
    [(1, TypeError), ("", ValueError), ("qqqqqqqqqqqqqqqqqqqqq", ValueError)],
)
def test_invalid_computer_name(name, ex, computer_values):
    computer_values["name"] = name
    with pytest.raises(ex):
        Computer(**computer_values)


@pytest.mark.parametrize("health, ex", [(99, ValueError), (10001, ValueError)])
def test_invalid_computer_health(health, ex, computer_values):
    computer_values["health"] = health
    with pytest.raises(ex):
        Computer(**computer_values)


def test_health_setter(computer, computer_values):
    computer.health = 350
    assert getattr(computer, "health") == 350
    assert getattr(computer, "health_line") == "................."
    assert getattr(computer, "danger") == True
    computer.health = 0
    assert getattr(computer, "health") == 0
    assert getattr(computer, "health_line") == ""
    assert getattr(computer, "danger") == True
    computer.health = -1000
    assert getattr(computer, "health") == 0
    assert getattr(computer, "health_line") == ""
    assert getattr(computer, "danger") == True
    computer.health = 700000
    assert getattr(computer, "health") == computer_values["health"]
    assert getattr(computer, "health_line") == 50 * "."
    assert getattr(computer, "danger") == False


def test_danger(computer):
    computer.health = 350
    assert getattr(computer, "danger") == True
    computer.health = 351
    assert getattr(computer, "danger") == False


def test_health_line(computer):
    computer.health = 350
    assert getattr(computer, "health_line") == "................."
    computer.health = 0
    assert getattr(computer, "health_line") == ""
    computer.health = 700000
    assert getattr(computer, "health_line") == 50 * "."


def test_get_damaged(computer, computer_values):
    computer.get_damaged()
    assert getattr(computer, "health") < computer_values["health"]
    computer.health = computer_values["health"] - 18
    computer.get_damaged()
    assert getattr(computer, "health") != computer_values["health"]
    computer.health = 350
    computer.get_damaged()
    assert getattr(computer, "health") > 350


def test_get_large_damaged(computer, computer_values):
    computer.get_large_damaged()
    assert getattr(computer, "health") < computer_values["health"]
    computer.health = 10
    computer.get_large_damaged()
    assert getattr(computer, "health") == 0


def test_get_healed(computer, computer_values):
    computer.get_healed()
    assert getattr(computer, "health") == computer_values["health"]
    computer.health = computer_values["health"] - 18
    computer.get_healed()
    assert getattr(computer, "health") == computer_values["health"]


def test_str(computer):
    assert str(computer.name) in str(computer)
