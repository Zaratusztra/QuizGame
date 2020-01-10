
# -*- coding: utf-8 -*-
# By Ziemowit "Zaratustra" Wójcicki

class User:
    """
    Class represents user in system.
    """

    def __init__(self, login = 'guest', score = 0):
        self._login = str(login)
        self._score = int(score)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, new_score):
        if new_score < 0:
            self._score = 0
        else:
            self._score = int(new_score)

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, new_login):
        self._login = str(new_login)

    def __str__(self):
        return self._login
