
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

def execute_sql_select(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchone()

def execute_sql_query(connection, query, values):
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()

def load_user(dbname, login='guest', password=''):
    """
    Load user from by "login" in database named in "dbname".
    """
    # This function needs attention! Is not readable enough.
    # Checking password should be delegated into another function, used in "delete_user" function.

    query_select_user = \
    'SELECT score, password FROM Users where login="{}"'.format(login)
    
    user = None

    try:
        login = str(login)
        password = str(password)

        connection = sqlite3.connect(dbname)
        user_data = execute_sql_select(connection, query_select_user)
        if user_data is None:
            return user_data

        if password == user_data[1]:     # user_data = (login, score, password)
            user = User(login, user_data[0])
        else:
            return None
    except ValueError as err:
        logging.debug(err)
        return None
    except Exception:
        pass
    finally:
        connection.close()
    return user

def update_user(dbname, current_login, user_new):

    login = user_new.login
    score = user_new.score
    query_update = 'UPDATE Users SET login=?, score=? WHERE login=?'

    connection = sqlite3.connect(dbname)
    execute_sql_query(connection, query_update, (login, score, current_login))
    connection.close()


def add_user(dbname, login, passwd):
    query_add_user = 'INSERT INTO Users VALUES (?,?)'

    connection = sqlite3.connect(dbname)
    # execute_sql_insert
    connection.close()

def delete_user(dbname, login, passwd):
    query_delete_user = 'DELETE FROM Users WHERE login=?'

    connection = sqlite3.connect(dbname)
    # execute_sql_delete
    connection.close()
