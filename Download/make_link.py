'''
    입력 : 
    구글 드라이브에 업로드된 파일의 file_id
    
    동작 :
    다운로드 링크를 생성함  
    반환 : 다운로드 가능한 URL
'''

def make_download_link(file_id):
    """
    구글 드라이브 파일 ID로 다운로드 가능한 링크를 생성하는 함수
    Args:
        file_id (str): 구글 드라이브 파일 ID
    Returns:
        str: 다운로드 가능한 URL
    """
    # 구글 드라이브 파일 직접 다운로드 링크 포맷
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    print(f"다운로드 링크 생성: {download_url}")
    return download_url