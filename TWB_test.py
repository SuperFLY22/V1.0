import requests

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

# 파라미터 설정
params = {
    'downloadYn': '1',
    'srchDate': '2025-04-22',
    'srchDatesh': '20250422',
    'srchAl': 'TWB',
    'srchFln': '',
    'srchDep': '',
    'srchArr': 'RKPC',  #인천 RKSI, 김포 RKSS, 제주 RKPC, 대구 RKTN, 
    'dummy': '223848270',
    'cmd': 'get-records',
    'limit': '100',
    'offset': '0'
}

# 요청
response = requests.get(
    'https://ubikais.fois.go.kr:8030/sysUbikais/biz/fpl/selectArr.fois',
    headers=headers,
    cookies=cookies,
    params=params
)

# 응답 처리
if response.status_code == 200:
    try:
        data = response.json()
        records = data.get('records', [])
        print(f"\n📋 총 {len(records)}개의 항공편이 검색되었습니다.\n")

        for i, flight in enumerate(records, start=1):
            flt = flight.get('fpId', '정보없음')         # 항공편 번호
            reg = flight.get('acId', '정보없음')         # 등록번호
            eta = flight.get('eta', '정보없음')          # 예정 도착 시간
            ata = flight.get('ata', '정보없음')          # 실제 도착 시간
            status = flight.get('arrStatus', '정보없음') # 도착 상태
            spot = flight.get('standArr', '정보없음')    # 도착 스팟

            print(f"[{i}] FLT: {flt} | REG: {reg} | ETA: {eta} | ATA: {ata} | STS: {status} | SPOT: {spot}")
    except Exception as e:
        print("❌ JSON 파싱 실패:", e)
else:
    print(f"❌ 요청 실패 - 상태코드: {response.status_code}")
