
# -*- coding: utf-8 -*-
# By Ziemowit "Zaratustra" Wójcicki

class User:

    def __init__(self, login = 'guest', score = 0, last_score = 0):
        try:
            self._login = str(login)
            self._score = int(score)
            self._last_score = int(last_score)
        except:
            raise ValueError

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
    def last_score(self):
        return self._last_score

    @last_score.setter
    def last_score(self, new_lscore):
        if new_lscore < 0:
            self._last_score = 0
        else:
            self._last_score = int(new_lscore)

    def __str__(self):
        return self._login

