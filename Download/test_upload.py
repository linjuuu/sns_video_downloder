'''
    테스트용 스크립트
    다운로드된 동영상을 구글 드라이브에 업로드하고 다운로드 링크를 생성
'''

import os
from upload_drive import upload_to_drive
from make_link import make_download_link

def test_upload_and_link():
    # 테스트할 파일 경로
    video_path = os.path.join(
        os.path.dirname(__file__), 
        'videos', 
        '32284976621231506533603542288039936',
        '32284976621231506533603542288039936.mp4'
    )
    
    print("=== 구글 드라이브 업로드 테스트 ===")
    print(f"업로드할 파일: {video_path}")
    
    # 파일 존재 확인
    if not os.path.exists(video_path):
        print("❌ 파일을 찾을 수 없습니다!")
        return
    
    try:
        # 1. 구글 드라이브에 업로드
        print("\n1. 구글 드라이브 업로드 중...")
        file_id = upload_to_drive(video_path)
        
        # 2. 다운로드 링크 생성
        print("\n2. 다운로드 링크 생성 중...")
        download_url = make_download_link(file_id)
        
        print("\n=== 결과 ===")
        print(f"✅ 업로드 완료!")
        print(f"📁 파일 ID: {file_id}")
        print(f"🔗 다운로드 링크: {download_url}")
        
        # 3. 링크 테스트 안내
        print("\n=== 테스트 방법 ===")
        print("위 링크를 브라우저에 붙여넣어서 다운로드가 되는지 확인해보세요!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        print(f"상세 오류: {traceback.format_exc()}")

if __name__ == "__main__":
    test_upload_and_link() 