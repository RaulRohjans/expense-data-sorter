# pylint: disable=too-few-public-methods, no-member, broad-exception-caught
'''
Module that handles all the import logic for the
multiple sources
'''

import os
import sys
import pandas as pd
from database import (
    Expense,
    db
)


class Importer:
    '''
    Holds all the logic to send import transactions
    '''

    def __init__(self, transaction_type, file_path):
        self.type = transaction_type
        self.path = file_path
        self.db_session = db.get_session()

    def __del__(self):
        # Close db session when destroyed
        self.db_session.close()

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

        In this Excel file, the table columns start on line 8
        We only want the data in the columns B (date), C (description)
        and D (value)
        '''
        # Validate file
        self.__validate_path()

        filter_columns = {'Data Valor': 'date', 'Descrição': 'description', 'Valor': 'value'}

        # Read excel file data
        df = pd.read_excel(self.path, skiprows=8 - 1) # Actual data starts at row 8, skip all above

        # Filter wanted columns
        fdf = df[filter_columns.keys()]

        # Prepare data for db insertion
        df.rename(columns=filter_columns)
        expenses = [Expense(**data) for data in fdf]

        try:
            # Bulk insert data
            self.db_session.add_all(expenses, inplace=True)
        except Exception as e:
            # Rollback changes in case of error
            self.db_session.rollback()
            print("The following error ocurred while importing transactions:\n", e)

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
