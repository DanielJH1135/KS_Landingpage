import streamlit as st
import pandas as pd
from datetime import datetime
import os
import requests

# ==========================================
# 1. 사용자 설정 (이 부분만 수정하세요!)
# ==========================================
TELEGRAM_TOKEN = "7883185978:AAH7QjxYVMtIa4V29qMRx_IkOf1_IIJvAVY"  # 텔레그램 봇 토큰
CHAT_ID = 1781982606        # 텔레그램 수신자 ID (숫자)

# 상단 이미지/동영상 경로 (URL 혹은 파일경로)
MAIN_IMAGE = "https://images.unsplash.com/photo-1496171367470-9ed9a91ea931?auto=format&fit=crop&q=80&w=800"
# 동영상을 넣고 싶다면 st.video("동영상URL")를 아래 섹션에서 사용하세요.

# ==========================================
# 2. 페이지 기본 설정 및 디자인
# ==========================================
st.set_page_config(
    page_title="사전 예약 이벤트",
    page_icon="🎁",
    layout="centered"
)

# 모바일 최적화를 위한 커스텀 스타일
st.markdown("""
    <style>
    /* 전체 폰트 및 모바일 터치 최적화 */
    .main { background-color: #f9f9f9; }
    div.stButton > button:first-child {
        width: 100%;
        height: 3.5em;
        background-color: #FF4B4B;
        color: white;
        border-radius: 12px;
        font-weight: bold;
        font-size: 18px;
        border: none;
    }
    .stTextInput input, .stSelectbox div {
        height: 3.5em;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 텔레그램 메시지 전송 함수
def send_telegram_msg(name, phone, interest):
    text = f"🔔 [신규 DB 접수]\n- 성함: {name}\n- 연락처: {phone}\n- 관심사: {interest}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.get(url, params=params)
    except:
        pass # 오류 시 무시

# ==========================================
# 3. 화면 구성
# ==========================================

# (1) 메인 비주얼 (이미지)
# 이미지를 바꾸고 싶다면 아래 URL을 수정하세요.
st.image(MAIN_IMAGE, use_container_width=True)

# (2) 동영상 추가 예시 (필요 없으면 앞에 #를 붙여 주석처리 하세요)
# st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# (3) 타이틀 및 설명
st.title("🚀 새로운 서비스의 주인공이 되세요")
st.subheader("지금 신청하시면 런칭 즉시 혜택을 드립니다.")
st.write("---")

# (4) DB 수집 폼
with st.container():
    with st.form("survey_form", clear_on_submit=True):
        st.write("📋 **신청서 작성**")
        
        name = st.text_input("성함", placeholder="이름을 입력해 주세요")
        phone = st.text_input("연락처", placeholder="010-0000-0000")
        interest = st.selectbox(
            "어떤 기능이 가장 기대되나요?",
            ["가장 빠른 배송", "저렴한 가격", "압도적인 품질", "기타 문의"]
        )
        
        st.caption("개인정보는 알림 발송 후 즉시 파기됩니다.")
        agree = st.checkbox("개인정보 수집 및 이용 동의 (필수)")
        
        submit_button = st.form_submit_button("사전 예약 신청 완료")

        if submit_button:
            if not name or not phone:
                st.error("성함과 연락처를 모두 입력해 주세요!")
            elif not agree:
                st.warning("개인정보 수집에 동의해 주세요.")
            else:
                # 텔레그램 알림 발송
                send_telegram_msg(name, phone, interest)
                
                # CSV 파일로 서버에 저장
                new_data = {
                    "시간": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                    "이름": [name],
                    "연락처": [phone],
                    "관심사": [interest]
                }
                df = pd.DataFrame(new_data)
                file_path = "database.csv"
                if not os.path.isfile(file_path):
                    df.to_csv(file_path, index=False, encoding="utf-8-sig")
                else:
                    df.to_csv(file_path, mode='a', header=False, index=False, encoding="utf-8-sig")
                
                st.balloons()
                st.success(f"감사합니다, {name}님! 정상적으로 접수되었습니다.")

# (5) 하단 정보
st.markdown("---")
st.caption("© 2026 랜딩페이지 프로젝트. All rights reserved.")

