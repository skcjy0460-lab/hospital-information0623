"""
지역 병원 정보 안내 - 환자용 메인 페이지

이 앱은 두 개의 화면으로 구성됩니다.
1) app.py (이 파일)            : 환자가 보는 공개 조회 화면
2) pages/01_관리자_병원관리.py  : 컨설턴트/병원 담당자가 비밀번호로 접속하는 관리자 화면

좌측 사이드바 상단의 페이지 네비게이션에서 "관리자_병원관리"를 선택하면
관리자 화면으로 이동할 수 있습니다.
"""
import streamlit as st

from constants import SIDO_LIST, STANDARD_DEPARTMENTS
from ui_components import render_hospital_card
import db

st.set_page_config(page_title="지역 병원 정보 안내", page_icon="🏥", layout="wide")

st.title("🏥 지역 병원 정보 안내")
st.caption("우리 동네 병원의 의료진 구성, 진료과, 진료시간을 한눈에 확인하세요.")

with st.sidebar:
    st.header("🔍 검색 필터")
    sido = st.selectbox("시/도", ["전체"] + SIDO_LIST)
    sigungu = st.text_input("시/군/구", placeholder="예: 수성구")
    keyword = st.text_input("병원명 검색", placeholder="예: OO병원")
    department = st.selectbox("진료과", ["전체"] + STANDARD_DEPARTMENTS)
    st.divider()
    st.caption("관리자이신가요? 좌측 상단 페이지 메뉴에서 '관리자_병원관리'를 선택해주세요.")

try:
    hospitals = db.fetch_hospitals(
        sido=None if sido == "전체" else sido,
        sigungu=sigungu if sigungu else None,
        keyword=keyword if keyword else None,
        department=None if department == "전체" else department,
    )
except Exception as e:
    st.error(
        "병원 정보를 불러오는 중 오류가 발생했습니다. "
        "Supabase 연결 설정(Secrets)을 확인해주세요."
    )
    st.exception(e)
    st.stop()

if not hospitals:
    st.info("조건에 맞는 병원 정보가 없습니다. 필터를 조정해보세요.")
else:
    st.success(f"총 **{len(hospitals)}개** 병원이 검색되었습니다.")
    for h in hospitals:
        render_hospital_card(h)
