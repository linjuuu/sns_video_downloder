'''
    입력 : 
    video_url (str) - 다운로드할 동영상 URL
    thumbnail_url (str) - 썸네일 이미지 URL
    caption (str) - 동영상 설명
    author (str) - 작성자
    timestamp (datetime) - 작성 시간
    platform (str) - 동영상 플랫폼 (instagram, twitter, tiktok)
    message_id (str) - 메시지 ID
    
    동작 :
    비디오 파일을 다운로드 받아 파일로 저장함 
'''

import os
import requests
from datetime import datetime
import traceback
import shutil
import json

def download_video(video_url, thumbnail_url, caption, author, timestamp, platform, message_id):
    """
    소셜 미디어 동영상을 다운로드하는 함수
    
    Args:
        video_url (str): 다운로드할 동영상 URL
        thumbnail_url (str): 썸네일 이미지 URL
        caption (str): 동영상 설명
        author (str): 작성자
        timestamp (datetime): 작성 시간
        platform (str): 동영상 플랫폼
        message_id (str): 메시지 ID
    """
    try:
        # 기본 다운로드 폴더 생성
        base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Download")
        os.makedirs(base_dir, exist_ok=True)
        
        # videos 폴더 생성
        videos_dir = os.path.join(base_dir, "videos")
        os.makedirs(videos_dir, exist_ok=True)
        
        # 메시지별 폴더 생성
        message_dir = os.path.join(videos_dir, message_id)
        os.makedirs(message_dir, exist_ok=True)
        
        # URL을 문자열로 변환
        video_url_str = str(video_url)
        thumbnail_url_str = str(thumbnail_url)
        
        # 동영상 파일 저장
        video_filename = f"{message_id}.mp4"
        video_path = os.path.join(message_dir, video_filename)
        
        # 동영상 다운로드
        print(f"  · 동영상 다운로드 시작: {video_url_str}")
        response = requests.get(video_url_str, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        downloaded = 0
        
        with open(video_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    # 진행률 출력
                    if total_size > 0:
                        percent = int(100 * downloaded / total_size)
                        print(f"\r  · 다운로드 진행률: {percent}%", end='')
        print()  # 줄바꿈
        
        # 메타데이터 저장
        metadata = {
            'platform': platform,
            'caption': caption,
            'author': author,
            'timestamp': timestamp.strftime('%Y%m%d_%H%M%S'),
            'thumbnail_url': thumbnail_url_str,
            'video_url': video_url_str,
            'message_id': message_id,
            'download_time': datetime.now().strftime('%Y%m%d_%H%M%S')
        }
        
        # 메타데이터 파일 저장 (같은 폴더에)
        metadata_filename = f"{message_id}.json"
        metadata_path = os.path.join(message_dir, metadata_filename)
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
            
        print(f"  · {platform} 동영상 다운로드 완료: {message_id}")
        print(f"  · 저장 위치: {message_dir}")
        
    except Exception as e:
        print(f"  · 동영상 다운로드 실패: {e}")
        print(f"  · 상세 오류: {traceback.format_exc()}")
        
        # 실패 시 생성된 폴더 정리
        if os.path.exists(message_dir):
            shutil.rmtree(message_dir)