'''
Miscellaneous utils used across the project
'''

import sys

def throw_error(*messages):
    '''
    Throws an application erros and
    exists the app
    '''
    print(messages)
    sys.exit(1)
