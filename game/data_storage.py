
# -*- coding: utf-8 -*-
# By Ziemowit "Zaratustra" Wójcicki

import sys
import logging
import json
import sqlite3

from .quiz import Quiz, Riddle
from .users import User


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


def load_user(dbname, login='guest', password=''):
    """
    Load user from by "login" in database named in "dbname".
    """

    query_select_user = \
    'SELECT score, password FROM Users where login="{}"'.format(login)
    
    user = None

    try:
        login = str(login)
        password = str(password)

        connection = sqlite3.connect(dbname)
        cursor = connection.cursor()
        cursor.execute(query_select_user)
        user_data = cursor.fetchone()
        if user_data is None:
            return None

        if password == user_data[1]:     # user_data = (login, score, password)
            user = User(login, user_data[0])
        else:
            return None
    except ValueError:
        return None
    except Exception:
        return None
    else:
        cursor.close()
    return user


def update_user(dbname, current_login, user_new):

    login = user_new.login
    score = user_new.score

    query_update_score = 'UPDATE Users SET login=?, score=? WHERE login=?'
    print('executing: ', query_update_score, file=sys.stderr)
    input()

    try:
        connection = sqlite3.connect(dbname)
        cursor = connection.cursor()
        
        cursor.execute(query_update_score, (login, score, current_login))
        connection.commit()

        connection.close()
    except Exception:
        pass

