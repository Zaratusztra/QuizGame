# -*- coding: utf-8 -*-
# By Ziemowit "Zaratustra" Wójcicki


from game.users import User
from game.quiz import Quiz
from interface.tui import Ui

from common.stringtools import *

from game import data_storage

class Application:
    """
    Class represent application. It's a "glue" for interface, game engine and data.
    """

    def __init__(self, new_quiz=None):
        self.database_name = 'locals.db'

        self.quiz = new_quiz
        self.current_user = User('guest', 0)
        self.ui = Ui()
        self.setup_actions()


    def setup_actions(self):
        self.possible_options = {
            's' : {'msg': '[S]tart new game', 'action': self.start_new_game},
            'f' : {'msg': 'Load quiz from [F]ile', 'action': self.load_quiz_from_file},
            'v' : {'msg': '[V]iew last score', 'action': self.view_last_user_score},
            'c' : {'msg': '[C]hange login or password', 'action': self.change_login_or_passwd},
            'l' : {'msg': '[L]ogin', 'action': self.login_user},
            'q' : {'msg': '[Q]uit', 'action': self.quit},
        }
 


    def process_command(self, command):
        try:
            self.possible_options[command]['action']()
        except KeyError as err:
            pass


    def main_loop(self):
        self.login_user()
        
        command = "none"
        while command not in ('q', 'quit'):
            msg = self._get_main_menu_str()
            self.ui.output( msg, block=False )
            command = self.ui.input('>').lower()
            self.process_command(command)


    def start_new_game(self):
    
    
        if self.quiz is None:
            self.ui.output('No quiz is loaded...',)
            return
        
        self._redeem_quiz()
        
        final_message = \
        "You earned {} for this quiz.\nDo you want to save your score?" \
        .format(self.quiz.current_score)
        
        save = self.ui.ask(final_message)
        if(save):
            self.save_user_score()


    def login_user(self):
        new_login = self.ui.input("    login:", clear_before=True)
        if new_login == 'guest' or new_login == '':
            self._login_as_guest()
        else:
            passwd = self.ui.input("    password:", clear_before=False)
            new_user = data_storage.load_user(self.database_name, new_login, passwd)
            if new_user is not None:
                self.current_user = new_user
            else:
                self.ui.warning("Login failed!")
                if self.current_user is None:
                    self._login_as_guest()

    def view_last_user_score(self):
        score = self.current_user.score
        name = str(self.current_user)
        message = 'Current {} score: {}'.format(name, score)
        self.ui.output(message)


    def load_quiz_from_file(self):
        fname = self.ui.input('    file-name:', clear_before=True)
        try:
            q = data_storage.load_quiz_from_json(fname)
            self.quiz = q
        except (FileNotFoundError, OSError) as ex:
            self.ui.warning("Error - file not found.")
        except Exception as ex:
            self.ui.warning("Error while processing file... {}".format(ex))
        else:
            self.ui.output("Quiz successfully loaded.")


    def show_main_menu(self):
        for option in self.possible_actions:
            self.ui.output(option)


    def save_user_score(self):
        login = self.current_user.login
        self.current_user.score = self.quiz.current_score
        self._update_user()
        


    def change_login_or_passwd(self):
        option = self.ui.input("   [L]ogin or [P]assword?", clear_before=True)
        if option == 'l' or option == 'L':
            self._change_login()
        elif option == 'p' or option == 'P':
            self._change_password()


    def quit(self):
        pass

    
    def _get_main_menu_str(self):
        msg = "\nYou're login as {}\n".format(self.current_user)
        l = [option['msg'] for option in self.possible_options.values()]
        msg += format_list(l)+'\n'
        return msg


    def _redeem_quiz(self):
        for question in self.quiz:
            quest = '   '+str(question)
            user_answer = self.ui.input(quest, clear_before=True)
            reply = question.get_answer(user_answer)
            self.ui.output(reply)


    def _change_login(self):
        prev_login = self.current_user.login
        self.current_user.login = \
        self.ui.input('  new password:', clear_before=True)
        sefl._update_user(prev_login)


    def _change_password(self):
        self.current_user.password = \
        self.ui.input('  new password:', clear_before=True)
        self._update_user()


    def _update_user(self, previous_login=None):
        if previous_login == None:       #It is needed only when we're changing user login
            previous_login = self.current_user.login
        data_storage.update_user(   
                                    self.database_name, 
                                    previous_login, 
                                    self.current_user
                                )
   
    def _login_as_guest(self):
        self.current_user = User('guest', 0)       
    

