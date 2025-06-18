'''
    입력 : 
    instagrapi 클라이언트 객체
    
    동작 : 
    모든 사용자의 메시지를 읽고, 릴스나 동영상이 포함된 메시지만 처리
'''

'''
    알고리즘 
    
    1. instagrapi 연결
    2. 메시지 읽을 계정 로그인, 계정 (id : "linju_downloader", pw : "toem0812!")
    3. 해당 계정의 메시지함에서 메시지들 정보 읽어오기 
    
'''

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import instagrapi
from security import instagram_id, instagram_pw
from deliver import deliver_video_info
import re
import traceback

# 1. instagrapi 연결
cl = instagrapi.Client()

# 2. 메시지 읽을 계정 로그인
cl.login(username=instagram_id, password=instagram_pw)

def read_all_messages(cl):
    """
    모든 사용자의 메시지를 읽고 처리하는 함수
    
    Args:
        cl: instagrapi 클라이언트 객체
    """
    try:
        # 모든 대화 목록 가져오기
        threads = cl.direct_threads()
        print(f"총 {len(threads)}개의 대화를 찾았습니다.")
        
        for thread in threads:
            # 대화 상대 이름 출력
            users = thread.users
            if users:
                print(f"\n{users[0].username}님과의 대화:")
            
            # 메시지 가져오기
            messages = cl.direct_messages(thread.id)
            print(f"  · 메시지 {len(messages)}개 발견")
            
            for message in messages:
                try:
                    # 릴스나 동영상이 포함된 메시지인지 확인
                    has_media = False
                    video_info = {
                        'platform': 'instagram',
                        'author': users[0].username,
                        'timestamp': message.timestamp,
                        'message_id': message.id
                    }
                    
                    # 릴스 공유 확인
                    if message.reel_share:
                        print("  · 릴스 공유 발견")
                        has_media = True
                        video_info.update({
                            'video_url': message.reel_share.media.reel_id,
                            'thumbnail_url': message.reel_share.media.thumbnail_url,
                            'caption': message.reel_share.text
                        })
                    
                    # 클립 확인
                    elif message.clip:
                        print("  · 클립 발견")
                        has_media = True
                        video_info.update({
                            'video_url': message.clip.video_url,
                            'thumbnail_url': message.clip.thumbnail_url,
                            'caption': message.clip.caption_text
                        })
                    
                    # 미디어 공유 확인
                    elif message.media_share:
                        print("  · 미디어 공유 발견")
                        has_media = True
                        video_info.update({
                            'video_url': message.media_share.video_url,
                            'thumbnail_url': message.media_share.thumbnail_url,
                            'caption': message.media_share.caption_text
                        })
                    
                    # 동영상이 포함된 메시지인 경우 처리
                    if has_media:
                        print(f"  · 동영상 정보: {video_info}")
                        deliver_video_info(video_info)
                    else:
                        print("  · 동영상이 포함되지 않은 메시지 건너뜀")
                            
                except Exception as e:
                    print(f"  · 메시지 처리 실패: {e}")
                    print(f"  · 상세 오류: {traceback.format_exc()}")
                    continue
                    
    except Exception as e:
        print(f"메시지 읽기 실패: {e}")
        print(f"상세 오류: {traceback.format_exc()}")

# 3. 해당 계정의 메시지함에서 메시지들 정보 읽어오기 
read_all_messages(cl)