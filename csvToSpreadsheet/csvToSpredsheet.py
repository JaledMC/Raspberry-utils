import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import config

"""
Necesario: Google developer console Google Drive API y Google Sheets API
Obtener JSON para tener credenciales y poder modificar el spreadsheet
"""

scope = config.SCOPE
credentials = ServiceAccountCredentials.from_json_keyfile_name(config.CREDENTIALS, config.SCOPE)
gc = gspread.authorize(credentials)
sheet = gc.open_by_key(config.KEY)
sheet1 = sheet.get_worksheet(0)

def add_row(row):
    """Append rows to an spreadsheet using gspread:
    Args:
        row (list): List of parameters to append.
    Returns:
        None
    """
    sheet1.append_row(row)
