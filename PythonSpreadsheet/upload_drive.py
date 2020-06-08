from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import argparse

def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u", "--upload",
        help="path to authentifiaction json crendentials",
    )
    parser.add_argument(
        "-d", "--download",
        help="donwnload the file",
        )
    parser.add_argument(
        "-r", "--remove",
        help="remove the file in google drive",
    )
    parser.add_argument(
        "-i", "--info",
        help="permissions of the file in google drive",
    )
    return parser.parse_args()

def autenticacion():
    """ 
        metodo que carga las credecniales.Es necesario archivo client_secret.json y settings.yaml

        client_secret.json: https://gsuitedevs.github.io/PyDrive/docs/build/html/quickstart.html
        settings.yaml: https://gsuitedevs.github.io/PyDrive/docs/build/html/oauth.html#automatic-and-custom-authentication-with-settings-yaml
    """
    gauth=GoogleAuth()
    gauth.LoadCredentialsFile()
    drive = GoogleDrive(gauth)
    return drive

def upload_drive(drive, path_file):
    """
        metodo que sube un archivo
        inputs:
            drive: instancia de la autentifiacion
            path_file: ruta y nombre del archivo que quiero subir 
    """
    file1 = drive.CreateFile()
    file1.SetContentFile(path_file)
    file1.Upload() 
    print('title: %s, id: %s' % (file1['title'], file1['id']))

def delete_drive(drive, id_file):
    """
        metodo que borra un archivo, si se pasa el id
        inputs:
            drive: instancia de la autentifiacion
            id_file: id del archivo que quiero subir 
    """
    file1 = drive.CreateFile({'id': id_file})
    file1.Trash()

def permisos_drive(drive, id_file):
    """
        metodo que muestra los permisos de un archivo, si se pasa el id
        inputs:
            drive: instSancia de la autentifiacion 
            id_file: id del archivo que quiero subir
    """

    file1 = drive.CreateFile({'id': id_file})
    file1.GetPermissions()
    print(file1['permissions'])    

if __name__ == "__main__":
    drive=autenticacion()
    args = parse_options()
    
    if args.upload:
        upload_drive(drive, args.upload)
    if args.remove:
        delete_drive(drive, args.remove)
    if args.info:
        permisos_drive(drive, args.info)