# -*- coding: utf-8 -*-
# By Ziemowit "Zaratustra" Wójcicki

import os
import sys
import logging
import configparser

from game.users import User
from game.quiz import Quiz
from interface.tui import Ui

from common.stringtools import *

from game import data_storage

class Application:
    """Class represent main application logic. It's a "glue" for interface, game engine and data management. 
    Application should be started by creating an instance of this class and invoking method "main_loop".
    """

    def __init__(self, new_quiz=None):
        
        self.__configure()

        self.quiz = new_quiz
        self.current_user = User('guest', 0)
        self.ui = Ui()

        self.setup_actions()

    def __configure(self):
        # self.__config will be used in all __XXX_config() procedures.
        self.__config = configparser.ConfigParser()
        
        self.__database_config()
        self.__logger_config()

    def __database_config(self):
        dbname = str()
        try:
            self.__config.read('config.ini')
            dbname = self.__config['DATABASE']['name']
        except Exception:
            dbname = 'local.db'
        if os.path.isfile(dbname):
            self.database_name = dbname
        else:
            dbname = 'QuizGame/{}'.format(dbname)
            if os.path.isfile(dbname):
                self.database_name = dbname
            else:
                self.database_name = None

    def __logger_config(self):
        logging_level = str()
        log_file = str()
        mode = 'a'
        if '--debug' in sys.argv:
            logging_level = logging.DEBUG
            log_file = 'debug.log'
        else:
            try: #TO-DO: Problem is, when only one of parameter will be undefined, the all configuration from file fails.
                logging_level = self.__config['LOGGER']['level']
                log_file = self.__config['LOGGER']['file']
                mode = 'w' if self.__config['LOGGER']['file'] == 'false' else 'a'
            except Exception:
                logging_level = logging.INFO
                log_file = 'last_session.log'
        logging.basicConfig(filename=log_file, level=logging_level, filemode=mode)
    
    def __get_main_menu_str(self):
        msg = "\nYou're logged as {}\n".format(self.current_user)
        l = [option['msg'] for option in self.possible_options.values()]
        msg += format_list(l)+'\n'
        return msg


    def __redeem_quiz(self):
        for question in self.quiz:
            quest = str(question)
            user_answer = self.ui.input(quest)
            reply = question.get_answer(user_answer)
            self.ui.output(reply)


    def __change_login(self):
        prev_login = self.current_user.login
        self.current_user.login = \
        self.ui.input('new login:')
        self.__update_user(prev_login)


    def __change_password(self):
        self.current_user.password = \
        self.ui.input('new password:')
        self.__update_user()


    def __update_user(self, previous_login=None):
        if previous_login == None:       #It is needed only when we're changing user login
            previous_login = self.current_user.login
        data_storage.update_user(   
                                    self.database_name, 
                                    previous_login, 
                                    self.current_user
                                )
   
    def __login_as_guest(self):
        self.current_user = User('guest', 0)
    
    def login_user(self):
        if self.database_name == None:
            logging.info("Database was not found. Trying to log user as guest.")
            self.ui.warning("Database was not found. You will be logged as guest.")
            self.__login_as_guest()
        new_login, passwd = self.ui.get_login_data()
        if new_login == 'guest' or new_login == '':
            self.__login_as_guest()
        else:
            new_user = data_storage. \
            load_user(self.database_name, new_login, passwd)
            if new_user is not None:
                self.current_user = new_user
            else:
                self.ui.warning("Login failed!")
                logging.warning("Failed attempt to log-in: {}".format(new_login))
                if self.current_user is None:
                    self.__login_as_guest()

    def view_last_user_score(self):
        score = self.current_user.score
        name = str(self.current_user)
        message = 'Current {} score: {}'.format(name, score)
        self.ui.output(message)
    
    def show_users_list(self):
        users_list = [User(l[0],l[1]) for l \
            in data_storage.load_users_list(self.database_name)]
        sorted(users_list, key=lambda user: user.score)
        message = "Current users:\n"
        for user in users_list:
            message += "User:" + user.login + " - score: " + str(user.score) + "\n"
        self.ui.output(message)

    def load_quiz_from_file(self):
        fname = self.ui.input('file-name:')
        try:
            q = data_storage.load_quiz_from_json(fname)
            self.quiz = q
        except (FileNotFoundError, OSError) as ex:
            self.ui.warning("Error - file not found.")
            logging.debug(ex)
        except Exception as ex:
            self.ui.warning(ex)
            logging.debug('Unexpected error while processing file - {}'.format(ex))
        else:
            self.ui.output("Quiz successfully loaded.")


    def show_main_menu(self):
        for option in self.possible_options:
            self.ui.output(option)


    def save_user_score(self):
        login = self.current_user.login
        self.current_user.score = self.quiz.current_score
        self.__update_user(login)
        

    def change_login_or_passwd(self):
        option = self.ui.input("[L]ogin or [P]assword?")
        if option == 'l' or option == 'L':
            self.__change_login()
        elif option == 'p' or option == 'P':
            self.__change_password()
    
    def add_new_user(self):
        new_login, new_passwd = self.ui.get_login_data(repeat_password=True)
        if new_passwd == None:
            self.ui.warning("Provided passwords are not the same!")
        else:
            if data_storage.add_user(self.database_name, new_login, new_passwd) == False:
                log = "Adding user {} to database failed".format(new_login)
                logging.info(log)
                self.ui.warning("Sorry, some kind of error has occured. Operation probably failed.")

    def delete_user(self):
        user_login, user_passwd = self.ui.get_login_data()
        if self.ui.input("Are you sure, you want to delete user {}?\
             [Y/n]".format(user_login)) not in ['n','N']:
            data_storage.delete_user(self.database_name, user_login, user_passwd)
        

    def quit(self):
        pass

    def setup_actions(self):
        self.possible_options = {
            's' : {'msg': ' [S]tart new game', 'action': self.start_new_game},
            'f' : {'msg': ' Load quiz from [F]ile', 'action': self.load_quiz_from_file},
            'v' : {'msg': ' [V]iew last score', 'action': self.view_last_user_score},
            'c' : {'msg': ' [C]hange login or password', 'action': self.change_login_or_passwd},
            'l' : {'msg': ' [L]ogin', 'action': self.login_user},
            'a' : {'msg': ' [A]dd new user', 'action': self.add_new_user},
            'd' : {'msg': ' [D]elete user', 'action': self.delete_user},
            'q' : {'msg': ' [Q]uit', 'action': self.quit},
            'r' : {'msg': ' show [R]anking', 'action': self.show_users_list}
        }
 
    def start_new_game(self):
        if self.quiz is None:
            self.ui.output('No quiz is loaded...',)
            return
        
        self.__redeem_quiz()
        
        final_message = \
        "You earned {} for this quiz.\nDo you want to save your score?" \
        .format(self.quiz.current_score)
        
        save = self.ui.ask(final_message)
        if(save):
            self.save_user_score()

    def process_command(self, command):
        try:
            self.possible_options[command]['action']()
        except KeyError as err:
            err_msg="Sorry, some kind of error has occured:\n{}".format(err)
            self.ui.warning(err_msg)

    def main_loop(self):
        self.login_user()
        
        command = "none"
        while command not in ('q', 'quit'):
            msg = self.__get_main_menu_str()
            self.ui.output( msg, block=False )
            command = self.ui.get_commandline('>').lower()
            self.process_command(command)