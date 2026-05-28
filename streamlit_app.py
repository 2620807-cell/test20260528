import streamlit as st

# 1. 앱 제목 및 설명 (출력)
st.title("🏆 이번 대회 3등은 누구?")
st.write("참가자들의 이름과 점수를 입력하면, 정확히 **3등**을 한 주인공을 찾아줍니다!")

# 2. 사용자 입력 받기 (입력)
# 스트림릿의 text_area를 활용해 여러 줄을 한 번에 입력받습니다.
st.subheader("📝 참가자 정보 입력")
default_data = "김철수 95\n이영희 88\n박민수 92\n최수연 79\n정태양 85"
user_input = st.text_area(
    "이름과 점수를 띄어쓰기로 구분해서 입력해 주세요. (한 줄에 한 명씩)",
    value=default_data,
    height=150
)

# 분석 시작 버튼
if st.button("📊 3등 결과 확인하기"):
    
    # 데이터를 저장할 리스트
    participants = []
    
    # 3. 입력된 텍스트 처리 (반복문 & 조건문)
    lines = user_input.split("\n")
    for line in lines:
        line = line.strip()
        if not line:  # 빈 줄은 건너뜁니다 (조건문)
            continue
            
        try:
            # 공백을 기준으로 이름과 점수 분리
            name, score_str = line.split()
            score = float(score_str) # 점수를 숫자로 변환
            
            # 리스트에 딕셔너리 형태로 추가
            participants.append({"이름": name, "점수": score})
        except ValueError:
            st.error(f"⚠️ 입력 형식이 올바르지 않은 줄이 있습니다: '{line}' (예: 홍길동 90)")
            st.stop() # 오류 발생 시 프로그램 중단

    # 4. 데이터 검증 및 정렬 (조건문)
    if len(participants) < 3:
        st.warning("🏃‍♂️ 참가자가 3명 미만입니다. 최소 3명 이상의 정보를 입력해 주세요!")
    else:
        # 점수를 기준으로 내림차순(높은 순) 정렬
        # lambda를 사용해 딕셔너리의 '점수' 값을 기준으로 정렬합니다.
        participants.sort(key=lambda x: x["점수"], reverse=True)
        
        # 5. 등수 매기기 (동점자 처리 포함 반복문 & 조건문)
        ranked_participants = []
        current_rank = 1
        
        for i in range(len(participants)):
            # 첫 번째 사람이거나, 이전 사람과 점수가 다르면 등수 업데이트
            if i > 0 and participants[i]["점수"] < participants[i-1]["점수"]:
                current_rank = i + 1  # 공동 순위 반영 (예: 공동 1등이 2명이면 다음은 3등)
                
            participants[i]["순위"] = current_rank
            ranked_participants.append(participants[i])

        # 6. 전체 순위 출력 (반복문)
        st.write("---")
        st.subheader("📈 전체 순위 표")
        
        # 스트림릿 테이블로 보기 좋게 출력
        st.table(ranked_participants)
        
        # 7. 3등 찾기 결과 출력 (조건문 & 반복문)
        st.write("---")
        third_place_winners = [p["이름"] for p in ranked_participants if p["순위"] == 3]
        
        if third_place_winners:
            # 3등이 여러 명일 수도 있으므로 조인해서 출력
            winners_str = ", ".join(third_place_winners)
            st.balloons() # 축하 효과!
            st.success(f"🎉 축하합니다! 이번 대회의 **3등**은 바로 **[{winners_str}]** 입니다!")
        else:
            # 동점자 상황 때문에 3등이 건너뛰어진 경우 (예: 공동 2등이 2명이라 바로 4등으로 넘어간 경우)
            st.info("💡 공동 순위 영향으로 인해 정확히 '3등'으로 표시된 참가자가 없습니다.")