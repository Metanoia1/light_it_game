"""
Test for Gamer class
Command line: python -m pytest tests/test_gamer.py
"""
import pytest

from light_it_game import Gamer


@pytest.fixture
def gamer_values():
    return {
        "name": "qqqqqqqqqqqqqqqqqqqq",
        "health": 1000,
    }


@pytest.fixture
def gamer(gamer_values):
    return Gamer(**gamer_values)


def test_create(gamer, gamer_values):
    for attr_name in gamer_values:
        assert getattr(gamer, attr_name) == gamer_values.get(attr_name)


@pytest.mark.parametrize(
    "name, ex",
    [(1, TypeError), ("", ValueError), ("qqqqqqqqqqqqqqqqqqqqq", ValueError)],
)
def test_invalid_gamer_name(name, ex, gamer_values):
    gamer_values["name"] = name
    with pytest.raises(ex):
        Gamer(**gamer_values)


@pytest.mark.parametrize("health, ex", [(99, ValueError), (10001, ValueError)])
def test_invalid_gamer_health(health, ex, gamer_values):
    gamer_values["health"] = health
    with pytest.raises(ex):
        Gamer(**gamer_values)


@pytest.mark.parametrize("health, ex", [("asdfsadf", TypeError), (5.55, TypeError)])
def test_invalid_gamer_health_instance(health, ex):
    with pytest.raises(ex):
        Gamer("Name", health)


def test_health_setter(gamer, gamer_values):
    gamer.health = 350
    assert getattr(gamer, "health") == 350
    assert getattr(gamer, "health_line") == "................."
    assert getattr(gamer, "danger") == True
    gamer.health = 0
    assert getattr(gamer, "health") == 0
    assert getattr(gamer, "health_line") == ""
    assert getattr(gamer, "danger") == True
    gamer.health = -1000
    assert getattr(gamer, "health") == 0
    assert getattr(gamer, "health_line") == ""
    assert getattr(gamer, "danger") == True
    gamer.health = 700000
    assert getattr(gamer, "health") == gamer_values["health"]
    assert getattr(gamer, "health_line") == 50 * "."
    assert getattr(gamer, "danger") == False
    with pytest.raises(ValueError):
        gamer.health = "asldkf"
    with pytest.raises(ValueError):
        gamer.health = 7.77


def test_danger(gamer):
    gamer.health = 350
    assert getattr(gamer, "danger") == True
    gamer.health = 351
    assert getattr(gamer, "danger") == False


def test_health_line(gamer):
    gamer.health = 350
    assert getattr(gamer, "health_line") == "................."
    gamer.health = 0
    assert getattr(gamer, "health_line") == ""
    gamer.health = 700000
    assert getattr(gamer, "health_line") == 50 * "."


def test_get_damaged(gamer, gamer_values):
    gamer.get_damaged()
    assert getattr(gamer, "health") < gamer_values["health"]
    gamer.health = 18
    gamer.get_damaged()
    assert getattr(gamer, "health") == 0


def test_get_large_damaged(gamer, gamer_values):
    gamer.get_large_damaged()
    assert getattr(gamer, "health") < gamer_values["health"]
    gamer.health = 10
    gamer.get_large_damaged()
    assert getattr(gamer, "health") == 0


def test_get_healed(gamer, gamer_values):
    gamer.get_healed()
    assert getattr(gamer, "health") == gamer_values["health"]
    gamer.health = gamer_values["health"] - 18
    gamer.get_healed()
    assert getattr(gamer, "health") == gamer_values["health"]


def test_str(gamer):
    assert str(gamer.name) in str(gamer)
