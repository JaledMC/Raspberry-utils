import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import random


def autenticacion():
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('/Users/work/Documents/gspread/prueba-subir-archvios-drive-b709c27e983d.json', scopes=scopes)
    gc = gspread.authorize(credentials)
    return gc


def get_sheets(gc, name):
    try:
        sh = gc.open(name)
    except Exception:
        print('Creando archivo ' + name)
        sh = gc.create(name)
    return sh


def get_worksheet(sh, name):
    try:
        wks = sh.worksheet(name)
    except Exception:
        print('Creando pestaña ' + name)
        wks = sh.add_worksheet(title=name, rows="1000", cols="28")
    return wks


def aleatorio():
    numeros = []
    for i in range(10):
        numeros.append(random.randint(1, 101))
    return numeros


if __name__ == "__main__":
    gc = autenticacion()
    sh = get_sheets(gc, 'test')
    wks = get_worksheet(sh, str(datetime.now().strftime("%d/%m/%Y")))
    sh.share('n.moustafa@sialitech.com', perm_type='user', role='writer')
    for a in aleatorio():
        wks.append_row([a])
