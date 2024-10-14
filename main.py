'''
Module where main logic is executed, it interacts with importers,
offers some commands to view data, and allows display of statistics
'''

import argparse
import sys
from importer import Importer

def start_statistics():
    '''
    Starts the server for the dashboard with statistics
    '''
    return 0

def main():
    '''
    Starts the program execution
    '''

    # Create the parser instance
    parser = argparse.ArgumentParser(description='Transaction Importer and Statistical Tool')

    # Add arguments
    parser.add_argument('--import', type=str, dest='import_type', required=False,
                        help='The import statement type. Ex: "activobank", "caixa", "oney"')
    parser.add_argument('--path', type=str, required='--import' in sys.argv,
                        help='The path of the file to be imported.')
    parser.add_argument('--statistics', type=bool, required=False,
                        help='Show the statistics dashboard.')

    # Parse arguments
    args = parser.parse_args()

    # In case of an import operation, start the corresponding logic
    if args.import_type and args.path:
        imp = Importer(args.import_type, args.path)
        imp.start()
        return

    # Display statistics dashboard as the default behavior
    start_statistics()

if __name__ == '__main__':
    main()
