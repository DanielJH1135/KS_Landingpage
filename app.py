import streamlit as st
import pandas as pd
from datetime import datetime
import os
import requests

# ==========================================
# 1. 사용자 설정
# ==========================================
TELEGRAM_TOKEN = "7883185978:AAH7QjxYVMtIa4V29qMRx_IkOf1_IIJvAVY"
CHAT_ID = 1781982606

# [수정] 언스플래쉬 이미지는 원본 소스 링크 형식을 사용해야 화면에 나옵니다.
MAIN_IMAGE = "https://images.unsplash.com/photo-1509391366360-feaffa663abd?q=80&w=2070&auto=format&fit=crop"

# ==========================================
# 2. 페이지 기본 설정 및 디자인
# ==========================================
st.set_page_config(
    page_title="전력절감, 태양광 솔루션은 KS입니다.",
    page_icon="⚡",
    layout="centered"
)

# 모바일 및 가시성 최적화 커스텀 스타일
st.markdown("""
    <style>
    /* 전체 배경 */
    .main { background-color: #f9f9f9; }
    
    /* 질문(Label) 스타일 수정: 볼드체 + 3포인트 크게 */
    label {
        font-size: 1.2rem !important; /* 기본보다 약 3pt 크게 */
        font-weight: 800 !important;   /* 아주 굵게 */
        color: #31333F !important;
        margin-bottom: 10px !important;
    }
    
    /* 버튼 스타일 */
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
    
    /* 입력창 디자인 */
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
        pass

# ==========================================
# 3. 화면 구성
# ==========================================

# (1) 메인 비주얼
st.image(MAIN_IMAGE, use_container_width=True, caption="KS 태양광 솔루션")

# (2) 타이틀 및 설명
st.title("🚀 까다로운 축사, 주차장도 한번에 해결!")
st.subheader("지금 신청하시면 최적의 맞춤 설계를 도와드립니다.")
st.write("---")

# (3) DB 수집 폼
with st.container():
    with st.form("survey_form", clear_on_submit=True):
        st.write("📋 **아래 정보를 입력해 주세요**")
        
        # 질문들이 CSS에 의해 볼드/확대되어 보입니다.
        name = st.text_input("성함", placeholder="성함을 입력해 주세요")
        phone = st.text_input("연락처", placeholder="010-0000-0000")
        interest = st.selectbox(
            "문의 사항 (최적의 조건으로 안내해 드립니다)",
            ["한전 수전합리화사업(전력요금 절감)", "주차장 태양광", "축사 지붕 태양광", "기타 문의"]
        )
        
        st.caption("개인정보는 알림 발송 후 즉시 파기됩니다.")
        agree = st.checkbox("개인정보 수집 및 이용 동의 (필수)")
        
        submit_button = st.form_submit_button("상담 신청 완료")

        if submit_button:
            if not name or not phone:
                st.error("성함과 연락처를 모두 입력해 주세요!")
            elif not agree:
                st.warning("개인정보 수집에 동의해 주세요.")
            else:
                send_telegram_msg(name, phone, interest)
                
                # CSV 저장
                new_data = {
                    "시간": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                    "이름": [name],
                    "연락처": [phone],
                    "관심사": [interest]
                }
                df = pd.DataFrame(new_data)
                file_path = "database.csv"
                df.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False, encoding="utf-8-sig")
                
                st.balloons()
                st.success(f"감사합니다, {name}님! 담당자가 곧 연락드리겠습니다.")

# (4) 하단 정보
st.markdown("---")
st.caption("© 2026 KS Solar Energy Project. All rights reserved.")
