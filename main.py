'''
Module where main logic is executed, it interacts with importers,
offers some commands to view data, and allows display of statistics
'''

import argparse
import sys

from importer import Importer
from utils import throw_error

def main():
    '''
    Starts the program execution
    '''

    # Create the parser instance
    parser = argparse.ArgumentParser(description='Transaction Importer and Statistical Tool')

    # Add arguments
    parser.add_argument('--import', type=str, dest='import_type', required=True,
                        help='The import statement type. Ex: "activobank", "caixa", "oney"')
    parser.add_argument('--path', type=str, required='--import' in sys.argv,
                        help='The path of the file to be imported.')

    # Parse arguments
    args = parser.parse_args()

    if not args.import_type or not args.path:
        throw_error("Invalid arguments, please check help and try again.")

    # Start data import
    imp = Importer(args.import_type, args.path)
    imp.start()
    return

if __name__ == '__main__':
    main()
