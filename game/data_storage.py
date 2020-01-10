
# -*- coding: utf-8 -*-
# By Ziemowit "Zaratustra" Wójcicki

import os
import sys
import logging
import json
import sqlite3
import hashlib

from .quiz import Quiz, Riddle
from .users import User


def hash_password(password, it=100000):
    password = password.encode("utf-8")
    try:
        it = int(it)
    except ValueError:
        it = int(10)
    hash_password = hashlib.pbkdf2_hmac('sha256', password, b'salt', it) #placeholder
    return hash_password

def verify_password(stored_password, provided_password):
    provided_password = hash_password(provided_password)
    return str(stored_password) == str(provided_password)


def load_quiz_from_json(filename):
    """
    Load and returns quiz as set of tuples question-answers-correct answer.
    param filename: type str
    return quiz.Quiz
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
    """Execute sql select query passed as the second argument to the database sqlite3.Connection passed as the first argument and return firs fetched result.
    return: [?]
    """
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchone()

def execute_sql_query(connection, query, values):
    """Execute sql query, where values are inserted into correct fields in query.
    param connection: type sqlite3.Connection
    param query: type str
    param values: type str
    return: no value
    """
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()

def load_users_list(dbname):
    cursor = sqlite3.connect(dbname).cursor()
    cursor.execute("SELECT login, score FROM Users;")
    return cursor.fetchall()

def load_user(dbname, login='guest', password=''):
    """Load user from by "login" in database named in "dbname" and then returns as object users.User.
    param dbname: type str
    param login: type str
    param password: type str
    return: users.User
    """
    # This function needs attention! Is not readable enough.
    # Checking password should be delegated into another function, used in "delete_user" function.

    query_select_user = \
    'SELECT score, password FROM Users where login="{}"'.format(login)

    try:
        login = str(login)
        password = str(password)
        password = str(hash_password(password))

        connection = sqlite3.connect(dbname)
        user_data = execute_sql_select(connection, query_select_user)
        if user_data is None:
            return user_data
        logging.info("Comparing {} to {}".format(password, user_data[1]))
        if verify_password(password, user_data[1]):     # user_data = (score, password)
            return User(login, user_data[0])
        else:
            return None
    except ValueError as err:
        logging.debug(err)
        return None
    except sqlite3.Error as err:
        logging.info(err)
        return None
    finally:    #finally is always executed before leaving try statement. "Returns" here would overwrite all the others. I still need a reminder.
        connection.close()

def update_user(dbname, current_login, user_new):
    """Update user data.
    param dbname: type str -- name of the database to update
    param current_login: type str
    param user_new: users.User -- new datas used to overwrite current user datas
    return: no value
    """

    login = user_new.login
    score = user_new.score
    query_update = 'UPDATE Users SET login=?, score=? WHERE login=?'

    try:
        connection = sqlite3.connect(dbname)
        execute_sql_query(connection, query_update, (login, score, current_login))
    except sqlite3.Error as err:
        logging.info(err)
    finally:
        connection.close()

def add_user(dbname, login, passwd):
    """Adds user with login and password passed as arguments into database. Return False if error has occured during the execution of query.
    param dbname: type str --  name of the database to update
    param login: type str -- NEW user login
    param passwd: type str -- NEW user password
    return: boolean
    """
    passwd = str(hash_password(passwd))
    query_add_user = 'INSERT INTO Users VALUES (?,?,?)'

    try:
        connection = sqlite3.connect(dbname)
        execute_sql_query(connection, query_add_user, (login, 0, passwd))
    except sqlite3.Error as err:
        logging.debug(err)
        return False
    finally:
        connection.close()
    return True

def delete_user(dbname, login, passwd):
    """Delete user by login AND password(!) from database. Return False if error has occured during the execution of query.
    param dbname: type str --  name of the database to update
    param login: type str -- user login
    param passwd: type str -- user password
    return: boolean
    """
    query_delete_user = 'DELETE FROM Users WHERE login=? AND password=?'
    passwd = str(hash_password(passwd))

    try:
        connection = sqlite3.connect(dbname)
        execute_sql_query(connection, query_delete_user, (login, passwd))
    except sqlite3.Error as err:
        logging.debug(err)
        return False
    finally:
        connection.close()
    return True