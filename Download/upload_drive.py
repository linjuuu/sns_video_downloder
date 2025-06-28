'''
    입력 : 
    다운로드된 파일 경로 (file_path)
    
    동작 :
    구글 드라이브에 연결하여 파일을 업로드함 
    반환 : 업로드된 파일의 Google Drive file id
'''

import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def set_public_permission(service, file_id):
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    service.permissions().create(fileId=file_id, body=permission).execute()
    print("공개 권한 부여 완료")

# 서비스 계정 키 파일 경로 (구글 클라우드에서 발급받은 json)
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), 'service_account.json')
SCOPES = ['https://www.googleapis.com/auth/drive']

def upload_to_drive(file_path):
    """
    다운로드된 파일을 구글 드라이브에 업로드하는 함수
    Args:
        file_path (str): 업로드할 파일의 경로
    Returns:
        str: 업로드된 파일의 Google Drive file id
    """
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=credentials)

    file_metadata = {'name': os.path.basename(file_path)}
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file_id = file.get('id')
    print(f"구글 드라이브 업로드 완료: {file_path} → file_id={file_id}")

    # anyone 권한 부여
    set_public_permission(service, file_id)

    return file_id

