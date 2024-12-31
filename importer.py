# pylint: disable=too-few-public-methods, no-member, broad-exception-caught
'''
Module that handles all the import logic for the
multiple sources
'''

import os
import sys
import pandas as pd

from utils import throw_error
from gsheets import GSheets


class Importer:
    '''
    Holds all the logic to send import transactions
    '''

    def __init__(self, transaction_type, file_path):
        self.type = transaction_type
        self.path = file_path

        # Init google sheets service
        self.gsheets = GSheets()

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
            throw_error('The given import type is not valid, please check'
            'the supported types within the help menu.')

    def __validate_path(self):
        '''
        Checks if the path is valid, the file exists, and is a supported type
        '''
        supported_files = ['.xls', '.xlsx']

        if os.path.splitext(self.path)[1] not in supported_files:
            throw_error('The file type provided is not supported, currently only the following '
            'types are:\n', ', '.join(supported_files))

        # Check if the file exists
        if not os.path.isfile(self.path):
            throw_error('The provided file does not exist or is invalid.')

    def __import_activobank(self):
        '''
        Starts the import process "activobank"

        In this Excel file, the table columns start on line 8
        We only want the data in the columns B (date), C (description)
        and D (value)
        '''
        self.__validate_path()

        df = pd.read_excel(self.path, skiprows=8 - 1) # Actual data starts at row 8, skip all above

        # Filter out the trash
        filter_columns = {'Data Valor': 'date', 'Descrição': 'description', 'Valor': 'value'}
        fdf = df[filter_columns.keys()]

        # Now we prepare the data to be inserted into the table
        # for each of the records, we want to add the bank, and a None
        # value for the category, since the user should be the one deciding
        # where it belongs
        expenses_to_insert = fdf.values.tolist()
        expenses_to_insert = [[
            entry[0].strftime('%Y-%m-%d') if pd.notnull(entry[0]) else None,
            'ActivoBank',
            entry[2],
            None,
            entry[1]
            ] for entry in expenses_to_insert]

        # Finally we only need to add the data to the excel spreadsheet
        self.gsheets.add_expense(expenses_to_insert)

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
