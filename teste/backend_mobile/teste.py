from google.oauth2 import service_account
import googleapiclient.discovery

def testar_credenciais():
    credentials = service_account.Credentials.from_service_account_file("sistemaNortrCromo_googleConsole.json")
    drive_service = googleapiclient.discovery.build('drive', 'v3', credentials=credentials)
    arquivos = drive_service.files().list(pageSize=1).execute()
    print("Arquivos listados:", arquivos)

if __name__ == "__main__":
    testar_credenciais()
