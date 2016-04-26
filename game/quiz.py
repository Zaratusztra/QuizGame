
# -*- coding: utf-8 -*-
#By Ziemowit "Zaratustra" Wójcicki


from .users import User



class Quiz:


    def __init__(self, riddles):
        self.riddles = riddles
        self.current_score = 0

    def __iter__(self):
        self.current_score = 0
        self._it = 0
        self._limit = len(self._riddles)
        return self
    
    def __next__(self):
        if self._it < self._limit:
            self._it += 1
            current_riddle = self._riddles[self._it-1]
            return Question(self, current_riddle)
        else:
            raise StopIteration

    @property
    def riddles(self):
        return self._riddles

    @riddles.setter
    def riddles(self, new_riddles):
        if isinstance(new_riddles, list):
            self._riddles = new_riddles
        else:
            raise ValueError        

    @property
    def current_score(self):
        return self._current_score
    
    @current_score.setter
    def current_score(self, new_score):
        self._current_score = int(new_score)


class Question:


    def __init__(self, owner, riddle):
        self.owner = owner
        self.riddle = riddle

    @property
    def riddle(self):
        return self._riddle

    @riddle.setter
    def riddle(self, new_riddle):
        if isinstance( new_riddle, Riddle ):
            self._riddle = new_riddle
        else:
            raise ValueError

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, new_owner):
        if isinstance( new_owner, Quiz):
            self._owner = new_owner
        else:
            raise ValueError
    
    def __str__(self):
        return str(self.riddle)

    def get_answer(self, ans):
        if self.riddle.is_correct_answer(ans):
            self.owner.current_score += self.riddle.value
            return "Correct!"
        else:
            return "Incorrect answer"

class Riddle:
    
    
    def __init__(self, msg, answers, correct_answer, val=1):
        try:
            self._content = str(msg)
            self._answers = list(answers)
            self._correct_answer = str(correct_answer)
            self._value = int(val)
        except (ValueError, TypeError) as err:
            pass

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value < 0:
            self._value = 0
        else:
            self.value = new_value
    
    def __str__(self):
        ret =  '\n===========================================================\n'
        ret += self._content + '\n-----------------------------------------------------------\n\n'
        for ans in self._answers:
            ret += ans
            ret += '\n'
        ret += '\n===========================================================\n'
        return ret

    def is_correct_answer(self, ans):
        return self._correct_answer == str(ans)


