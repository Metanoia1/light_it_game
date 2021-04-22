"""
Test for Game class
Command line: python -m pytest tests/test_game.py
"""
import pytest

from light_it_game import Game, Computer, Gamer


@pytest.fixture
def game_values():
    return {
        "computer": Computer("Computer"),
        "gamer": Gamer("qwerty"),
    }


@pytest.fixture
def game(game_values):
    return Game(**game_values)


def test_create(game, game_values):
    assert getattr(game, "_computer") == game_values.get("computer")
    assert getattr(game, "_gamer") == game_values.get("gamer")


@pytest.mark.parametrize(
    "computer, ex",
    [(1, ValueError), (Gamer("sadfsa"), ValueError), (7.55, ValueError)],
)
def test_invalid_computer_instance(computer, ex):
    with pytest.raises(ex):
        Game(computer, Gamer("235235"))


@pytest.mark.parametrize(
    "gamer, ex",
    [(1, ValueError), ("asdf", ValueError), (7.55, ValueError)],
)
def test_invalid_gamer_instance(gamer, ex):
    with pytest.raises(ex):
        Game(Computer("asdkjflaskf"), gamer)


def test_invalid_computer_and_gamer(game):
    with pytest.raises(ValueError):
        comp = Computer("comp")
        Game(comp, comp)


def test_move(game):
    for _ in range(100):
        game.move()
    result = (
        game._computer.health != game._computer._init_health
        or game._gamer.health != game._gamer._init_health
    )
    assert result is True
