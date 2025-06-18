'''
    입력 : 
    video_info (dict) - 동영상 정보를 담은 딕셔너리
    
    동작 :
    여러 플랫폼의 동영상 정보를 통합 처리하고 Download 폴더의 get_video.py로 전달
'''

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Download.get_video import download_video

def process_video_info(video_info):
    """
    동영상 정보를 플랫폼별로 처리하는 함수
    
    Args:
        video_info (dict): 동영상 정보
        
    Returns:
        dict: 처리된 동영상 정보
    """
    platform = video_info.get('platform', 'unknown')
    
    # 플랫폼별 처리
    if platform == 'instagram':
        # 인스타그램 릴스 처리
        return {
            'video_url': video_info['video_url'],
            'thumbnail_url': video_info['thumbnail_url'],
            'caption': video_info['caption'],
            'author': video_info['author'],
            'timestamp': video_info['timestamp'],
            'platform': platform,
            'message_id': video_info['message_id']
        }
    elif platform == 'twitter':
        # 트위터 동영상 처리 (추후 구현)
        pass
    elif platform == 'tiktok':
        # 틱톡 동영상 처리 (추후 구현)
        pass
    else:
        print(f"  · 지원하지 않는 플랫폼: {platform}")
        return None

def deliver_video_info(video_info):
    """
    동영상 정보를 Download 폴더로 전달하는 함수
    
    Args:
        video_info (dict): 동영상 URL, 썸네일, 설명, 작성자, 타임스탬프 정보
    """
    try:
        # 동영상 정보 처리
        processed_info = process_video_info(video_info)
        if not processed_info:
            return
            
        # Download 폴더의 get_video.py로 정보 전달
        download_video(
            video_url=processed_info['video_url'],
            thumbnail_url=processed_info['thumbnail_url'],
            caption=processed_info['caption'],
            author=processed_info['author'],
            timestamp=processed_info['timestamp'],
            platform=processed_info['platform'],
            message_id=processed_info['message_id']
        )
        print(f"  · {processed_info['platform']} 동영상 정보 전달 완료")
    except Exception as e:
        print(f"  · 동영상 정보 전달 실패: {e}")