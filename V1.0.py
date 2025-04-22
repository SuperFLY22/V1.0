import streamlit as st
import requests

st.subheader("✈️ TWB 항공편 도착 정보 조회")

# 로그인 세션 쿠키
cookies = {
    'SCOUTER': 'z6o4bt7d1he1go',
    'JSESSIONID': 'oZaOqftAplLeCfso27BvQzHc74ve5xfb3X9ffpGGXIN04Lu2lZs2RaZ1zSR8e2cy.amV1c19kb21haW4vdWJpa2Fpc18x'
}

# 헤더
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://ubikais.fois.go.kr:8030/sysUbikais/biz/fpl/arr'
}

# 공항 선택
airport_code = st.selectbox(
    "도착 공항을 선택하세요",
    options=["RKSI", "RKSS", "RKPC", "RKTN", "PKTU", "RKPS"],
    format_func=lambda x: {
        "RKSI": "인천 (RKSI)",
        "RKSS": "김포 (RKSS)",
        "RKPC": "제주 (RKPC)",
        "RKTN": "대구 (RKTN)",
        "PKTU": "청주 (PKTU)",
        "RKPS": "김해 (RKPS)",
    }[x]
)

from datetime import date

# 날짜 입력 (기본값은 오늘)
today = date.today()
srch_date = st.date_input("조회할 날짜 선택", value=today)

# 조회 버튼
if st.button("항공편 조회"):

    date_dash = srch_date.strftime("%Y-%m-%d")
    date_plain = srch_date.strftime("%Y%m%d")

    params = {
        'downloadYn': '1',
        'srchDate': date_dash,
        'srchDatesh': date_plain,
        'srchAl': 'TWB',
        'srchFln': '',
        'srchDep': '',
        'srchArr': airport_code,
        'dummy': '223848270',
        'cmd': 'get-records',
        'limit': '100',
        'offset': '0'
    }

    response = requests.get(
        'https://ubikais.fois.go.kr:8030/sysUbikais/biz/fpl/selectArr.fois',
        headers=headers,
        cookies=cookies,
        params=params
    )

    if response.status_code == 200:
        try:
            data = response.json()
            records = data.get('records', [])
            st.success(f"총 {len(records)}개의 항공편이 검색되었습니다.")

            for i, flight in enumerate(records, start=1):
                st.write(f"**[{i}] FLT:** {flight.get('fpId', '정보없음')} | "
                         f"**REG:** {flight.get('acId', '정보없음')} | "
                         f"**ETA:** {flight.get('eta', '정보없음')} | "
                         f"**ATA:** {flight.get('ata', '정보없음')} | "
                         f"**STS:** {flight.get('arrStatus', '정보없음')} | "
                         f"**SPOT:** {flight.get('standArr', '정보없음')}")
        except Exception as e:
            st.error("JSON 파싱 실패")
            st.error(str(e))
    else:
        st.error(f"요청 실패 - 상태코드: {response.status_code}")
