# -*- coding: utf-8 -*-
# interface.py
# By Ziemowit "Zaratustra" Wójcicki

import os

class Ui:
    def __init__(self):
        pass

    def _hline(ch, l):
        s = '\n'
        for i in range(l):
            s += ch
        s += '\n'
        return s

    def _clear_screen(self):
        if os.name == 'posix':
            os.system('clear')
        elif os.name == 'nt':
            os.system('cls')
        else:
            for i in range(100): print('\n')

    def output(self, *args, block = True):
        self._clear_screen()
        print('\n')
        for i in args:
            print('    ', i)
        if block: 
            input("\n\nPress any key...")
            self._clear_screen()

    def ask(self, arg):
        res = self.input(arg+'\n[y/N]')
        if res.lower() == 'y':
            return True
        else:
            return False

    def input(self, arg='', clear_before=False):
        if clear_before:
            self._clear_screen()
            arg = '\n\n     '+str(arg)
        return input(arg)
        self._clear_screen()

    def warning(self, warn):
        self._clear_screen()
        print(Ui._hline('=', len(warn)+27))
        print("\n       WARNING: {}\n\n".format(warn))
        print(Ui._hline('=', len(warn)+27))
        input('\n<press any key>')
        self._clear_screen()

    def quit(self):
        self._clear_screen()
        print('Finishing... have a nice day')

