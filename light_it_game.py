"""
Light IT game
"""
from subprocess import run
from random import randint


class Gamer:
    """
    Gamer class describes gamer instance
    """

    def __init__(self, name, health=100):
        """
        Gamer initialization

        Args:
            name (str): displays gamer name
            health (int): displays health value

        Raises:
            TypeError: if the `health` not an integer
            ValueError: if the `health` less than 100 or more than 10000
        """
        if not isinstance(health, int):
            raise TypeError("The `health` value must be an integer")

        if health < 100 or health > 10000:
            raise ValueError("Initial `health` must be between 100 and 10000")

        # initial health value (int)
        self._init_health = health

        # how many percent of self.health must remain for self.danger to be True
        self._danger_zone_percent = 35

        # the symbol for visualizing health line
        self._health_line_symbol = "."
        # how many symbols for full health line
        self._health_line_len = 50

        # gamer name (str)
        self.name = name
        # gamer health (int)
        self.health = health

    @property
    def danger(self):
        """
        Danger value getter

        if self.health <= self._danger_zone_percent / 100 * self._init_health
        self.danger will be True else False

        Returns:
            self._danger (bool)
        """
        return self._danger

    @property
    def health_line(self):
        """
        Visual line of the health status

        example of the self.health_line: .............................
        if self._health_line_symbol == '#':
        it will look like this: #############################

        Returns:
            self._health_line (str): line of symbols (self._health_line_symbol)
        """
        return self._health_line

    @property
    def name(self):
        """
        Name getter

        Returns:
            self._name (str): name value
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Name setter

        Args:
            value (str): name value must be a string instance

        Raises:
            TypeError: if value, not the string instance
            ValueError: if value less than 1 or more than 20
        """
        if not isinstance(value, str):
            raise TypeError("Name value must be a string")

        name_length = len(value.strip())

        if name_length < 1 or name_length > 20:
            raise ValueError("Name length must be between 1 and 20")

        self._name = value

    @property
    def health(self):
        """
        Health value getter

        Returns:
            self._health (int)
        """
        return self._health

    @health.setter
    def health(self, value):
        """
        Health value setter

        when self.health value changes this method recount self.danger and
        self.health_line

        Args:
            value (int): the value must be an integer

        Raises:
            ValueError: if the value not an integer instance
        """
        if not isinstance(value, int):
            raise ValueError("Health value must be an integer")

        self._health = value
        self._danger = False

        if self.health <= self._danger_zone_percent / 100 * self._init_health:
            self._danger = True

        if self.health >= self._init_health:
            self._health = self._init_health

        if self.health <= 0:
            self._health = 0

        health_percent = self.health / self._init_health * 100
        health_line_int = int(self._health_line_len / 100 * health_percent)
        self._health_line = self._health_line_symbol * health_line_int

    def get_damaged(self):
        """
        `get_damaged` method reduces self.health value on 18-25 diapason
        """
        value = randint(18, 25)
        print(f"{self} damaged (18-25 diapason): -{value}")
        self.health -= value

    def get_large_damaged(self):
        """
        `get_large_damaged` method reduces self.health value on 10-35 diapason
        """
        value = randint(10, 35)
        print(f"{self} damaged (10-35 diapason): -{value}")
        self.health -= value

    def get_healed(self):
        """
        `get_healed` method increases self.health value on 18-25 diapason
        """
        value = randint(18, 25)
        print(f"{self} healed (18-25 diapason): +{value}")
        self.health += value

    def __str__(self):
        """
        Representation of a Gamer instance object
        """
        return self.name


class Computer(Gamer):
    """
    Computer class describes computer instance
    """

    def get_damaged(self):
        """
        Extending `get_damaged` logic

        `get_damaged` is the method of the superclass (Gamer)

        Using self.get_healed() instead of self.get_damaged() when:
        self.health <= self._danger_zone_percent / 100 * self._init_health
        increases computer's chances on healing

        if self.danger:
            self.get_healed()
        else:
            super().get_damaged()
        """
        if self.danger:
            self.get_healed()
        else:
            super().get_damaged()


class Game:
    """
    Game class describes Game instance and the game logic
    """

    def __init__(self, computer, gamer):
        """
        Game initialization

        Args:
            computer (Computer): an instance of the Computer class
            gamer (int): an instance of the Gamer class

        Raises:
            ValueError: if `computer` not the Computer class instance
            ValueError: if `gamer` not the Gamer class instance
            ValueError: if `computer` and `gamer` are the same instance
        """
        if not isinstance(computer, Computer):
            raise ValueError("Computer must be the Computer class instance")

        if not isinstance(gamer, Gamer):
            raise ValueError("Gamer must be the Gamer class instance")

        if computer is gamer:
            raise ValueError("`computer` and `gamer` cannot be the same instance")

        self._computer = computer
        self._gamer = gamer
        self._steps = {
            "step_1": [computer.get_damaged, gamer.get_damaged],
            "step_2": [computer.get_large_damaged, gamer.get_large_damaged],
            "step_3": [computer.get_healed, gamer.get_healed],
        }

    def move(self):
        """
        `move` method selects random key from self._steps and random method
        from the key's value (list) and calls this method
        """
        steps_keys_list = list(self._steps.keys())
        steps_len = len(steps_keys_list) - 1
        step_title = steps_keys_list[randint(0, steps_len)]
        step_len = len(self._steps[step_title]) - 1
        step = self._steps[step_title][randint(0, step_len)]

        step()

    def run_game(self):
        """
        `run_game` method starts eventloop of the game and prints all events to
        the console and clears the console after each round
        """
        while True:
            input("Hit ENTER to step")

            # this just clears the terminal window for each step
            run("clear", check=True)

            self.move()

            print("----------------------------------------------------------")
            print(f"{self._computer} health: {self._computer.health}")
            print(self._computer.health_line)
            print(f"{self._gamer} health: {self._gamer.health}")
            print(self._gamer.health_line)
            print("----------------------------------------------------------")

            if self._computer.health <= 0:
                print(f"{self._gamer} won!")
                return

            if self._gamer.health <= 0:
                print(f"{self._computer} won!")
                return


if __name__ == "__main__":
    GAMER_NAME = ""

    while len(GAMER_NAME.strip()) == 0 or len(GAMER_NAME) > 20:
        GAMER_NAME = input("Enter your name: ")

    COMPUTER_INSTANCE = Computer("Computer")
    GAMER_INSTANCE = Gamer(GAMER_NAME.strip())

    GAME = Game(COMPUTER_INSTANCE, GAMER_INSTANCE)

    GAME.run_game()
