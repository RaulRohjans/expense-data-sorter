# pylint: disable=too-few-public-methods
'''
Module that handles all the import logic for the
multiple sources
'''

import os
import sys

class Importer:
    '''
    Holds all the logic to send import transactions
    '''

    def __init__(self, transaction_type, file_path):
        self.type = transaction_type
        self.path = file_path

    def start(self):
        '''
        Starts the import process for the given transaction type
        which could be "activobank", "oney" or "caixa"
        '''

        if self.type.lower() == 'activobank':
            self.__import_activobank()
        elif self.type.lower() == 'caixa':
            self.__import_caixa()
        elif self.type.lower() == 'oney':
            self.__import_oney()
        else:
            print('The given import type is not valid, please check'
            'the supported types within the help menu.')
            sys.exit()

    def __validate_path(self):
        '''
        Checks if the path is valid, the file exists, and is a supported type
        '''
        supported_files = ['.xls', '.xlsx']

        if os.path.splitext(self.path)[1] not in supported_files:
            print('The file type provided is not supported, currently only the following '
            'types are:\n', ', '.join(supported_files))
            sys.exit()


        # Check if the file exists
        if not os.path.isfile(self.path):
            print('The provided file does not exist or is invalid.')
            sys.exit()


    def __import_activobank(self):
        '''
        Starts the import process "activobank"
        '''
        self.__validate_path()

        return False

    def __import_caixa(self):
        '''
        Starts the import process "caixa"
        '''
        self.__validate_path()

        return False

    def __import_oney(self):
        '''
        Starts the import process "oney"
        '''
        self.__validate_path()

        return False
