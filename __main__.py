#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By Ziemowit "Zaratustra" Wójcicki

import argparse

from game.users import User
from game.quiz import Quiz
from game.interface import Ui
from common.stringtools import *

class Application:


    def __init__(self, new_quiz=None):
        self.quiz = new_quiz
        self.current_user = User('guest', 0)
        self.ui = Ui()
        self.setup_actions()

    def setup_actions(self):
        self.possible_options = [
                                '[S]tart new game',
                                #'[V]iew last score',
                                'View [T]otal score'
                                '[L]ogin',
                                'Load quiz from [F]ile',
                                '[Q]uit',
                                ]

    def process_command(self, command):
        if command == 's':
            self.start_new_game()
        elif command == 'v':
            self.view_last_user_score()
        elif command == 't':
            self.view_user_total_score()
        elif command == 'l':
            self.load_quiz_from_file()
        elif command == 'q':
            self.ui.quit()


    def main_loop(self):
        self.login_user()
        msg = "\nYou're login as {}\n".format(self.current_user)
        msg += format_list(self.possible_options)+'\n'
        command = "none"
        while command not in ('q', 'quit'):
            self.ui.output( msg, block=False )
            command = self.ui.input('>').lower()
            self.process_command(command)

    def start_new_game(self):
        if self.quiz is None:
            self.ui.output('No quiz is loaded...',)
            return
        for question in self.quiz:
            #self.ui.output( question.get_answer(self.ui.input(question)) )
            user_answer = self.ui.input(question, clear_before=True)
            reply = question.get_answer(user_answer)
            self.ui.output(reply)
        final_message = \
        "You earned {} for this quiz.\nDo you want to save your score?".format(self.quiz.current_score)
        save = self.ui.ask(final_message)
        if(save):
            self.save_user_score()

    def login_user(self):
        new_user_login = self.ui.input("login:")
        #loading new user by login and asking for password

    #def view_last_user_score(self): # TO-DO
    #    pass

    def view_user_total_score(self):
        pass

    def load_quiz_from_file(self):
        #START!
        return

    def show_main_menu(self):
        for option in self.possible_actions:
            self.ui.output(option)
    
    def save_user_score():
        self.current_user.score = self.quiz.current_score


if __name__ == '__main__':
    from game.quiz import Riddle
    r = list()
    r.append(Riddle('correct answer is a', ['(a) Answer', '(b) Answer'], 'a'))
    r.append(Riddle('correct answer is b', ['(a) Answer', '(b) Answer'], 'b'))
    r.append(Riddle('correct answer is c', ['(a) Answer', '(b) Answer', '(c) Answer'], 'c'))
    q = Quiz(r)
    app = Application(q)
    app.main_loop()


