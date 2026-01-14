import streamlit as st
import pandas as pd
from datetime import datetime
import io

# 1. 페이지 설정
st.set_page_config(page_title="IRM 관리 시스템", layout="wide")

# 데이터 저장소 초기화
if 'db' not in st.session_state:
    st.session_state['db'] = []

# 2. 다국어 설정 및 항목 명칭
lang_dict = {
    "KO": {
        "title": "IRM 관리 시스템",
        "tab1": "인플루언서 등록 및 분석", "tab2": "데이터베이스/리스트",
        "name": "이름", "account": "SNS 계정",
        "ship_date": "제품 발송일", "guide_date": "가이드 전달일",
        "product_info": "발송 제품 및 수량", "post_date": "포스팅 날짜",
        "narrative": "브랜드 서사 적합도", "pro": "협업 전문성",
        "quant": "정량 데이터", "context": "콘텐츠 원문 및 댓글",
        "note": "코멘트 (특이점)",
        "save": "분석 결과 저장",
        "download": "데이터 다운로드 (엑셀 호환 CSV)",
        "table_cols": ["Date", "Name", "Account", "Tier", "ER", "Products", "Post_Date", "Comment"]
    },
    "EN": {
        "title": "IRM Management System",
        "tab1": "Add & Analyze", "tab2": "Database / List",
        "name": "Name", "account": "Account",
        "ship_date": "Shipping Date", "guide_date": "Guide Sent Date",
        "product_info": "Products & Qty", "post_date": "Posting Date",
        "narrative": "Narrative Fit", "pro": "Professionalism",
        "quant": "Quantitative Data", "context": "Content & Comments",
        "note": "Comment (Notes)",
        "save": "Save Analysis",
        "download": "Download Data (CSV)",
        "table_cols": ["Date", "Name", "Account", "Tier", "ER", "Products", "Post_Date", "Comment"]
    }
}

lang = st.sidebar.selectbox("🌐 Language", ["KO", "EN"])
t = lang_dict[lang]

st.title(f"🚀 {t['title']}")
tab1, tab2 = st.tabs([t['tab1'], t['tab2']])

# --- Tab 1: 인플루언서 등록 ---
with tab1:
    c_info1, c_info2 = st.columns(2)
    with c_info1:
        name = st.text_input(t['name'], placeholder="성함/닉네임")
    with c_info2:
        account = st.text_input(t['account'], placeholder="@아이디")

    c_proc1, c_proc2 = st.columns(2)
    with c_proc1:
        ship_date = st.text_input(t['ship_date'], placeholder="2024-01-01")
        product_info = st.text_input(t['product_info'], placeholder="발송 제품명")
    with c_proc2:
        guide_date = st.text_input(t['guide_date'], placeholder="2024-01-02")
        post_date = st.text_input(t['post_date'], placeholder="2024-01-10 예정")

    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"📊 {t['narrative']}")
        n1 = st.slider("결핍 해결력", 1, 5, 3)
        n2 = st.slider("슬로건 반영", 1, 5, 3)
        n3 = st.slider("라이프스타일 융합", 1, 5, 3)
        st.subheader(f"🤝 {t['pro']}")
        p1 = st.slider("마감 준수", 1, 5, 3)
        p2 = st.slider("가이드 이행", 1, 5, 3)
        p3 = st.slider("소통 매너", 1, 5, 3)
        
    with col2:
        st.subheader(f"📈 {t['quant']}")
        reach = st.number_input("Reach (조회수)", value=5000, min_value=1)
        likes = st.number_input("Likes", value=200)
        comments = st.number_input("Comments", value=50)
        shares = st.number_input("Shares", value=10)
        er = ((likes + comments + shares) / reach) * 100
        st.metric("Engagement Rate (ER)", f"{er:.2f}%")

    st.subheader(f"📝 {t['context']}")
    caption = st.text_area("캡션 원문", height=70)
    replies = st.text_area("댓글 반응", height=70)

    st.subheader(f"🖋️ {t['note']}")
    marketer_comment = st.text_area("특이사항 입력", height=70, label_visibility="collapsed")

    if st.button(t['save'], use_container_width=True):
        qual_score = (n1+n2+n3+p1+p2+p3) / 30 * 100
        total_score = (qual_score * 0.7) + (min(er * 10, 100) * 0.3)
        
        if total_score >= 85: tier = "Partner"
        elif total_score >= 70: tier = "Advocate"
        elif total_score >= 40: tier = "Supporter"
        else: tier = "Explorer"

        st.session_state['db'].append({
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Name": name, "Account": account, "Tier": tier, "ER": f"{er:.2f}%",
            "Products": product_info, "Post_Date": post_date, "Ship_Date": ship_date,
            "Guide_Date": guide_date, "Qual": int(qual_score), "Comment": marketer_comment,
            "Caption": caption, "Comments": replies
        })
        st.success("데이터베이스에 저장되었습니다!")

# --- Tab 2: 데이터베이스 확인 및 다운로드 ---
with tab2:
    if not st.session_state['db']:
        st.info("저장된 데이터가 없습니다.")
    else:
        df = pd.DataFrame(st.session_state['db'])
        
        # 엑셀에서 바로 열어도 한글이 안 깨지도록 'utf-8-sig' 인코딩 사용
        csv_data = df.to_csv(index=False).encode('utf-8-sig')
        
        st.download_button(
            label=f"📥 {t['download']}",
            data=csv_data,
            file_name=f"IRM_Report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime='text/csv',
            use_container_width=True
        )
        
        st.dataframe(df[t['table_cols']], use_container_width=True, hide_index=True)
