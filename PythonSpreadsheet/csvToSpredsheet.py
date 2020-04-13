import gspread
from oauth2client.service_account import ServiceAccountCredentials


"""
Script para subir con Python valores a una hoja de Google Spreadsheets
Necesario: Google developer console Google Drive API y Google Sheets API
Obtener JSON para tener credenciales y poder modificar el spreadsheet
Más info en:
    https://www.youtube.com/watch?v=7I2s81TsCnc
"""

SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/spreadsheets']


def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_option(
        "-c", "--credentials",
        help="path to authentifiaction json crendentials",
    )
    parser.add_option(
        "-k", "--key",
        help="key to the spreadsheet. Usually a part of the URL",
        )
    parser.add_option(
        "-s", "--sheet",
        help="number of the sheet to be written",
        default=0,
    )
    return parser.parse_args()


def init_sheet(credentials_path, key, work_sheet):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, SCOPE)
    gc = gspread.authorize(credentials)
    return gc.open_by_key(key).get_worksheet(work_sheet)


def main():
    args = parse_options()
    sheet = init_sheet(args.credentials, args.key, args.sheet)
    for i in range(10):
        sheet.append_row(["Prueba number: ".format(i)])


if __name__ == "__main__":
    main()
