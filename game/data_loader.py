
# -*- coding: utf-8 -*-
# By Ziemowit "Zaratustra" Wójcicki

import json

from .quiz import Quiz, Riddle


def load_quiz_from_json(filename):
    """
    TO-DO
    """

    quiz_dict = json.load(open(filename))

    riddles = list()

    for key in quiz_dict.keys():

        msg = quiz_dict[key]["Question"]
        answers = quiz_dict[key]["Answers"]
        correct_answer = quiz_dict[key]["Correct_answer"]

        riddle = Riddle(msg, answers, correct_answer)
        
        riddles.append(riddle)

    new_quiz = Quiz(riddles)
    return new_quiz
