from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Путь к вашему JSON-файлу с ключом
SERVICE_ACCOUNT_FILE = 'webinar2024.json'

# ID вашей Google Таблицы
SPREADSHEET_ID = '1JcqqBY_PLBoX3ZYQ3ykWbh5sLx4XypSw-intbw_cNLY'

# Аутентификация
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets'])

# Создание сервиса
service = build('sheets', 'v4', credentials=creds)

# Получаем данные из столбца A
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Лист1!A:A').execute()
values = result.get('values', [])

# Находим первую пустую строку
first_empty_row = len(values) + 1

# Записываем значение "12345" в первую пустую строку столбца A
new_value = [['12345']]
result = service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID, 
    range=f'Лист1!A{first_empty_row}',
    valueInputOption='USER_ENTERED', 
    body={'values': new_value}).execute()

print(f"Значение '12345' добавлено в ячейку A{first_empty_row}")
print(f"{result.get('updatedCells')} ячеек обновлено.")

# Считываем обновленные данные для проверки
updated_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Лист1!A:A').execute()
updated_values = updated_result.get('values', [])
print(f"Обновленные данные в столбце A: {updated_values}")