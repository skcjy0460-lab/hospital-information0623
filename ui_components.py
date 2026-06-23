"""
환자(공개)용 화면에서 병원 정보를 카드 형태로 보여주는 렌더링 함수 모음.
"""
import streamlit as st
import pandas as pd

DAY_ORDER = ["월", "화", "수", "목", "금", "토", "일", "공휴일"]


def render_hospital_card(hospital: dict):
    with st.container(border=True):
        col_photo, col_info = st.columns([1, 2])

        with col_photo:
            photos = [p for p in [hospital.get("photo_url_1"), hospital.get("photo_url_2")] if p]
            if photos:
                for p in photos:
                    st.image(p, use_container_width=True)
            else:
                st.markdown("📷 *등록된 사진이 없습니다*")

        with col_info:
            st.subheader(hospital.get("name", "이름 미등록"))

            location = " ".join(filter(None, [hospital.get("sido"), hospital.get("sigungu")]))
            if location:
                st.caption(f"📍 {location}" + (f" · {hospital['address']}" if hospital.get("address") else ""))

            if hospital.get("main_specialty"):
                st.markdown(f"🌟 **메인 진료과목:** {hospital['main_specialty']}")
            if hospital.get("special_features"):
                st.markdown(f"✨ **특화 진료:** {hospital['special_features']}")

            depts = hospital.get("departments", [])
            if depts:
                dept_names = sorted({d["department_name"] for d in depts})
                chips = "&nbsp;".join(
                    f'<span style="background-color:#EEF2FF;color:#3730A3;padding:3px 10px;'
                    f'border-radius:14px;font-size:0.85em;margin-right:4px;">{name}</span>'
                    for name in dept_names
                )
                st.markdown(f"**진료과:** {chips}", unsafe_allow_html=True)

            hotline = hospital.get("hotline_phone")
            if hotline:
                st.markdown(
                    f'<a href="tel:{hotline}" style="display:inline-block;margin-top:8px;padding:8px 18px;'
                    f'background-color:#FF4B4B;color:white;border-radius:8px;text-decoration:none;'
                    f'font-weight:bold;">📞 핫라인 문의: {hotline}</a>',
                    unsafe_allow_html=True,
                )
                if hospital.get("hotline_note"):
                    st.caption(hospital["hotline_note"])

        staff = hospital.get("medical_staff", [])
        if staff:
            with st.expander(f"👨‍⚕️ 의료진 보기 ({len(staff)}명)"):
                for s in sorted(staff, key=lambda x: x.get("display_order") or 0):
                    line = f"**{s['staff_name']}**"
                    extra = " · ".join(filter(None, [s.get("position"), s.get("department")]))
                    if extra:
                        line += f" · {extra}"
                    st.markdown(line)
                    if s.get("specialty_detail"):
                        st.caption(s["specialty_detail"])

        hours = hospital.get("business_hours", [])
        if hours:
            with st.expander("🕒 진료시간 보기"):
                render_business_hours_table(hours)


def render_business_hours_table(hours: list):
    hours_by_day = {h["day_of_week"]: h for h in hours}
    rows = []
    for day in DAY_ORDER:
        h = hours_by_day.get(day)
        if not h:
            continue
        if h.get("is_closed"):
            time_str = "휴진"
        else:
            open_t = (h.get("open_time") or "")[:5]
            close_t = (h.get("close_time") or "")[:5]
            time_str = f"{open_t} ~ {close_t}" if open_t or close_t else "-"
            if h.get("lunch_start") and h.get("lunch_end"):
                time_str += f" (점심 {h['lunch_start'][:5]}~{h['lunch_end'][:5]})"
        row = {"요일": day, "진료시간": time_str, "비고": h.get("note") or ""}
        rows.append(row)

    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.caption("등록된 진료시간 정보가 없습니다.")
