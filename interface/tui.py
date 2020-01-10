# -*- coding: utf-8 -*-
# By Ziemowit "Zaratustra" Wójcicki

import os
import getpass

class Ui:
    """Class Ui provides methods for terminal input-output."""

    def __init__(self):
        pass
    
    def __del__(self):
        self.quit()

    def __hline(self, ch, l):
        s = '\n'
        for i in range(l):
            s += ch
        s += '\n'
        return s

    def __dirty__clear_screen(self):
        for i in range(100): print('\n')

    def __clear_screen(self):
        if os.name == 'posix':
            try:
                os.system('clear')
            except Exception:
                self.__dirty__clear_screen()
        elif os.name == 'nt':
            try:
                os.system('cls')
            except Exception:
                self.__dirty__clear_screen()
        else:
            self.__dirty__clear_screen()

    def output(self, *args, block = True):
        self.__clear_screen()
        print('\n')
        for i in args:
            print('    ', i)
        if block: 
            input("\n\nPress any key...")
            self.__clear_screen()

    def ask(self, arg):
        res = self.input('\n  '+arg+'\n    [y/N]\n')
        if res.lower() == 'y':
            return True
        else:
            return False
    
    def get_login_data(self, repeat_password=False):
        self.__clear_screen()
        login = input('\n\n\n      login:')
        if (login != 'guest' and login != 'Guest') and login != '':
            passwd = getpass.getpass(prompt='      password:')
            if repeat_password == True:
                repeat_msg = '      repeat your password:'
                repeat_passwd = getpass.getpass(prompt=repeat_msg)
                if passwd != repeat_passwd:
                    passwd = None
        else:
            passwd = ''
        return (login, passwd)

    def get_commandline(self, arg=''):
        return self.input(arg, clear_before=False)

    def input(self, arg='', clear_before=True):
        if clear_before:
            self.__clear_screen()
            arg = '    \n\n'+str(arg)
        inp = input(str(arg))
        self.__clear_screen()
        return inp

    def warning(self, warn):
        self.__clear_screen()
        print(self.__hline('=', len(warn)+27))
        print("\n       WARNING: {}\n\n".format(warn))
        print(self.__hline('=', len(warn)+27))
        input('\n<press any key>')
        self.__clear_screen()

    def quit(self):
        self.__clear_screen()
        print('Finishing... have a nice day')
