import sys
import argparse
import gspread
import csv
from oauth2client.service_account import ServiceAccountCredentials

DEFAULT_EXPORT_DIR = "/tmp"

def download_spreadsheet(credentials_file, spreadsheet_name, sheet_index, export_directory):
    output_filename = f'{export_directory}/{spreadsheet_name}.csv'

    # define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)

    # authorize the clientsheet 
    client = gspread.authorize(creds)

    # get the instance of the Spreadsheet
    sheet = client.open(spreadsheet_name)

    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(sheet_index)

    with open(output_filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(sheet_instance.get_all_values())

def _get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('credentials_file', help="Archivo de credenciales")
    parser.add_argument('spreadsheet_name', help="Nombre del spreadsheet")
    parser.add_argument('sheet_index', type=int, help="Indice de la hoja del spreadsheet a descargar (comienza con cero)")
    parser.add_argument('-e', '--export_directory', default=DEFAULT_EXPORT_DIR, 
    help="Directorio en el cual descargar el archivo")
    return parser.parse_args()

if __name__ == "__main__":
    args = _get_arguments()
    download_spreadsheet(args.credentials_file, args.spreadsheet_name, args.sheet_index, args.export_directory)