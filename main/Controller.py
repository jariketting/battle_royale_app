"""
Game controller class

Class made by Jari
"""

from Player import Player


class Controller:
    # these are private variables and should not be accessed outside this class.
    _round = 1  # stores games current round
    _turn = 0  # stores player that is turning ?randomize this number to have a random player start
    _players = []  # stores players in game

    # stores colors
    _color = [
        [191, 0, 0],  # red
        [51, 193, 0],  # green
        [0, 140, 183],  # blue
        [244, 225, 48],  # yellow
        [161, 0, 183],  # purple
        [255, 255, 255],  # black
        [0, 0, 0],  # white
        [191, 92, 0]  # orange
    ]

    # turn to next round
    def next_round(self):
        self._round += 1

    # get current round
    def get_round(self):
        return self._round

    def get_players(self):
        return self._players

    def add_player(self, name):
        self._players.append(Player())

        self._players[-1].set_name(name)
        self._players[-1].set_color(*self._color[len(self.get_players()) - 1])
