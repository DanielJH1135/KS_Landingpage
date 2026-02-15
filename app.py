import streamlit as st
from datetime import datetime
import pandas as pd
import os

# 1. 페이지 설정 (모바일 브라우저 타이틀 및 아이콘)
st.set_page_config(
    page_title="사전 예약 이벤트",
    page_icon="🎁",
    layout="centered"  # 모바일 가독성을 위해 centered 레이아웃 사용
)

# 2. 모바일 최적화 커스텀 스타일 (CSS)
st.markdown("""
    <style>
    /* 전체 폰트 크기 조정 */
    html, body, [class*="css"] {
        font-family: 'Pretendard', sans-serif;
    }
    /* 버튼을 모바일 가로 꽉 차게 설정 */
    div.stButton > button:first-child {
        width: 100%;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }
    /* 입력창 모바일 터치 영역 최적화 */
    .stTextInput input {
        height: 3em;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 랜딩페이지 콘텐츠
st.image("https://images.unsplash.com/photo-1496171367470-9ed9a91ea931?auto=format&fit=crop&q=80&w=800", use_container_width=True)

st.title("🚀 서비스 런칭 알림 신청")
st.write("지금 사전 예약하시면 **선착순 100명**께 한정판 굿즈와 할인 쿠폰을 드립니다!")

# 4. 데이터 수집 폼
with st.container():
    st.info("💡 입력하신 정보는 서비스 알림 외 용도로 사용되지 않습니다.")
    
    with st.form("survey_form", clear_on_submit=True):
        name = st.text_input("성함", placeholder="홍길동")
        phone = st.text_input("연락처", placeholder="010-0000-0000")
        interest = st.selectbox(
            "가장 관심 있는 분야",
            ["서비스 이용 방법", "이용 가격", "제휴 문의", "기타"]
        )
        agree = st.checkbox("개인정보 수집 및 이용 동의 (필수)")
        
        submit_button = st.form_submit_button("혜택 받고 사전 신청하기")

        if submit_button:
            if not name or not phone:
                st.error("성함과 연락처를 입력해주세요.")
            elif not agree:
                st.warning("개인정보 동의가 필요합니다.")
            else:
                # 5. DB 저장 로직 (여기서는 CSV 파일로 예시)
                new_data = {
                    "수집시간": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                    "이름": [name],
                    "연락처": [phone],
                    "관심사": [interest]
                }
                df = pd.DataFrame(new_data)
                
                # 파일이 없으면 만들고, 있으면 추가
                file_path = "collected_data.csv"
                if not os.path.isfile(file_path):
                    df.to_csv(file_path, index=False, encoding="utf-8-sig")
                else:
                    df.to_csv(file_path, mode='a', header=False, index=False, encoding="utf-8-sig")
                
                st.balloons()
                st.success(f"축하합니다 {name}님! 신청이 완료되었습니다.")

# 6. 하단 푸터 (모바일 배려)
st.markdown("---")
st.caption("© 2024 My Service Team. All rights reserved.")