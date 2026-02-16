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

# 웅장한 태양광 발전소 사진
MAIN_IMAGE = "https://images.unsplash.com/photo-1508514177221-188b1cf16e9d?q=80&w=2070&auto=format&fit=crop"

# ==========================================
# 2. 페이지 기본 설정 및 디자인 (디테일 수정)
# ==========================================
st.set_page_config(
    page_title="전력절감, 태양광 솔루션은 KS입니다.",
    page_icon="⚡",
    layout="centered"
)

st.markdown("""
    <style>
    /* 1. 타이틀 크기 조절 (한 줄에 들어오도록 폰트 축소 및 줄바꿈 방지) */
    h1 {
        font-size: 2.1rem !important; 
        white-space: nowrap !important;
        word-break: keep-all !important;
        text-align: center;
    }
    
    /* 2. 질문 라벨(성함, 연락처, 문의사항)만 골라서 볼드체 및 크기 업 */
    div[data-testid="stWidgetLabel"] p {
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        color: #1e1e1e !important;
        margin-bottom: -5px !important; /* 입력창과의 간격 최적화 */
    }
    
    /* 3. 문의사항 박스 테두리 잔상 및 이상한 레이아웃 제거 */
    div[data-testid="stSelectbox"] label {
        background: none !important;
        border: none !important;
        padding: 0 !important;
    }

    /* 4. 개인정보 동의 체크박스는 일반 폰트로 (볼드 해제) */
    div[data-testid="stCheckbox"] label p {
        font-weight: normal !important;
        font-size: 0.95rem !important;
    }
    
    /* 5. 버튼 디자인 */
    div.stButton > button:first-child {
        width: 100%;
        height: 3.5em;
        background-color: #D32F2F;
        color: white;
        border-radius: 12px;
        font-weight: bold;
        font-size: 18px;
        border: none;
        margin-top: 10px;
    }
    
    /* 입력창 디자인 */
    .stTextInput input, .stSelectbox div {
        height: 3.2em;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# 텔레그램 메시지 전송 함수
def send_telegram_msg(name, phone, interest):
    text = f"🔔 [신규 DB 접수]\n- 성함: {name}\n- 연락처: {phone}\n- 관심사: {interest}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": text}
    try: requests.get(url, params=params)
    except: pass

# ==========================================
# 3. 화면 구성
# ==========================================

# (1) 메인 비주얼
st.image(MAIN_IMAGE, use_container_width=True)

# (2) 타이틀 (사이즈 줄임 적용됨)
st.title("🚀 까다로운 축사, 주차장도 한번에 해결!")
st.subheader("KS만의 최적화된 태양광 솔루션으로 전력 요금을 절감하세요.")
st.write("---")

# (3) DB 수집 폼
with st.container():
    with st.form("survey_form", clear_on_submit=True):
        # 헤더 부분도 볼드체로 강조
        st.markdown("### 📋 **무료 상담 신청서**")
        
        name = st.text_input("성함", placeholder="성함을 입력해 주세요")
        
        phone = st.text_input("연락처", placeholder="010-0000-0000")
        
        # 문의 사항 라벨 (CSS로 박스 현상 해결)
        interest = st.selectbox(
            "문의 사항 (최적의 조건으로 안내해 드립니다)",
            ["한전 수전합리화사업(전력요금 절감)", "주차장 태양광", "축사 지붕 태양광", "기타 문의"]
        )
        
        st.write("") 
        agree = st.checkbox("개인정보 수집 및 이용 동의 (필수)")
        st.caption("※ 입력하신 정보는 상담 알림 발송 후 안전하게 파기됩니다.")
        
        submit_button = st.form_submit_button("지금 바로 상담 신청하기")

        if submit_button:
            if not name or not phone:
                st.error("성함과 연락처를 모두 입력해 주세요!")
            elif not agree:
                st.warning("개인정보 수집에 동의해 주세요.")
            else:
                send_telegram_msg(name, phone, interest)
                # CSV 저장
                new_data = {"시간": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "이름": [name], "연락처": [phone], "관심사": [interest]}
                df = pd.DataFrame(new_data)
                df.to_csv("database.csv", mode='a', header=not os.path.exists("database.csv"), index=False, encoding="utf-8-sig")
                st.balloons()
                st.success(f"신청 완료! {name}님, 담당자가 신속하게 연락드리겠습니다.")

st.markdown("---")
st.caption("© 2026 KS Solar Energy Project. All rights reserved.")
