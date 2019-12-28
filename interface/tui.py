# -*- coding: utf-8 -*-
# By Ziemowit "Zaratustra" Wójcicki

import os
import getpass

class Ui:


    def __init__(self):
        pass
    
    def __del__(self):
        self.quit()

    def _hline(self, ch, l):
        s = '\n'
        for i in range(l):
            s += ch
        s += '\n'
        return s

    def _neutral_clear_screen(self):
        for i in range(100): print('\n')

    def _clear_screen(self):
        try:
            if os.name == 'posix':
                os.system('clear')
            elif os.name == 'nt':
                os.system('cls')
            else:
                self._neutral_clear_screen()
        except Exception:
            self._neutral_clear_screen()

    def output(self, *args, block = True):
        self._clear_screen()
        print('\n')
        for i in args:
            print('    ', i)
        if block: 
            input("\n\nPress any key...")
            self._clear_screen()

    def ask(self, arg):
        res = self.input('\n  '+arg+'\n    [y/N]\n')
        if res.lower() == 'y':
            return True
        else:
            return False
    
    def get_login_data(self, repeat_password=False):
        self._clear_screen()
        login = input('\n\n\n      login:')
        if (login != 'guest' and login != 'Guest') and login != '':
            #passwd = input('password:')
            passwd = getpass.getpass(prompt='      password:')
            if repeat_password == True:
                repeat_msg = '      repeat your password:'
                repeat_passwd = getpass.getpass(prompt=repeat_msg)
                if passwd != repeat_passwd:
                    raise Exception("Passwords are not the same.")
        else:
            passwd = ''
        return (login, passwd)

    def get_commandline(self, arg=''):
        return self.input(arg, clear_before=False)

    def input(self, arg='', clear_before=True):
        if clear_before:
            self._clear_screen()
            arg = '\n\n    '+str(arg)
        user_input = input(str(arg))
        self._clear_screen()
        return user_input

    def warning(self, warn):
        self._clear_screen()
        print(self._hline('=', len(warn)+27))
        print("\n       WARNING: {}\n\n".format(warn))
        print(self._hline('=', len(warn)+27))
        input('\n<press any key>')
        self._clear_screen()

    def quit(self):
        self._clear_screen()
        print('Finishing... have a nice day')

