import streamlit as st
import re

# --- split_by_punctuation 함수 (이전에 최종 수정된 버전) ---
# (이 함수는 웹에서도 똑같이 필요해요)
def split_by_punctuation(text):
    if not text: return []
    result = []
    parts = re.split(r'(。|」|』|？|！)', text) # 줄임표는 분리 기준으로 사용 안 함
    current_sentence = ""
    i = 0
    while i < len(parts):
        part = parts[i]
        if not part: i += 1; continue
        current_sentence += part
        is_terminator = part in ['。', '」', '』', '？', '！']
        is_question_or_exclamation = part in ['？', '！']
        next_part_is_closing_quote = False
        if i + 1 < len(parts):
            j = i + 1
            while j < len(parts) and not parts[j]: j += 1
            if j < len(parts) and parts[j] in ['」', '』']:
                next_part_is_closing_quote = True
        if is_terminator and not (is_question_or_exclamation and next_part_is_closing_quote):
            cleaned_sentence = current_sentence.strip()
            if cleaned_sentence: result.append(cleaned_sentence)
            current_sentence = ""
        i += 1
    cleaned_sentence = current_sentence.strip()
    if cleaned_sentence: result.append(cleaned_sentence)
    return result

# --- 텍스트 변환 핵심 로직 함수 ---
# (기존 convert_text 함수에서 UI 부분 빼고 로직만 가져옴)
def convert_vertical_to_horizontal_logic(input_text):
    # 1. 숫자 줄 필터링 및 단락 복원
    lines = input_text.strip().split('\n')
    paragraphs = []
    paragraph = ''
    for line in lines:
        stripped = line.strip()
        if not stripped: # 빈 줄이면 단락 구분
            if paragraph: paragraphs.append(paragraph); paragraph = ''
        elif not stripped.isdigit(): # 숫자로만 된 줄이 *아니라면* 이어붙임
             paragraph += stripped
    # 마지막 줄 처리
    if paragraph: paragraphs.append(paragraph)

    # 2. 문단 처리 및 문장 분리
    result_lines = []
    for line in paragraphs:
        line = line.strip()
        if not line: continue
        # 맨 앞 숫자 제거 (예: '1. 대사' 같은 경우 대비)
        cleaned_line = re.sub(r'^\s*\d+[\s\.]*\s*', '', line).strip()
        if not cleaned_line: continue

        # SE: 처리 로직은 필요하면 여기에 추가할 수 있습니다.
        # 지금은 SE: 관련 특별 처리는 포함하지 않았습니다.

        # 문장 부호 기준으로 분리
        result_lines.extend(split_by_punctuation(cleaned_line))

    # 결과 줄들을 합쳐서 반환
    return "\n".join(result_lines)

# --- Streamlit 웹 화면 구성 ---
st.set_page_config(page_title="세로쓰기 → 가로쓰기 변환기", layout="wide") # 웹페이지 기본 설정

st.title("📝 일본어 세로쓰기 → 가로쓰기 변환기") # 큰 제목
st.caption("세로쓰기 대본을 복사해서 붙여넣으면 가로쓰기로 변환하고 문장 단위로 줄을 나눠줍니다.") # 작은 설명

col1, col2 = st.columns(2) # 화면을 좌우 두 칸으로 나눔

with col1: # 왼쪽 칸
    st.subheader("세로쓰기 텍스트 입력:")
    # 여러 줄 텍스트 입력 상자 만들기 (높이 조절)
    input_text = st.text_area("여기에 붙여넣으세요 👇", height=400, key="input_text_area")

with col2: # 오른쪽 칸
    st.subheader("변환 결과:")
    output_text = "" # 결과를 담을 변수 초기화

    # '가로로 변환하기' 버튼 만들기
    if st.button("✨ 가로로 변환하기"):
        if input_text: # 입력된 텍스트가 있으면
            # 변환 로직 함수 호출해서 결과 얻기
            output_text = convert_vertical_to_horizontal_logic(input_text)
        else: # 입력된 텍스트가 없으면 경고 메시지
            st.warning("입력창에 텍스트를 먼저 넣어주세요!")

    # 결과 텍스트 출력 상자 (읽기 전용처럼 보이게)
    st.text_area("결과 👇 (직접 복사해서 사용하세요)", value=output_text, height=400, key="output_text_area", help="변환된 텍스트입니다. 필요한 곳에 복사해서 사용하세요.")

# (선택사항) 입력/출력 내용 지우기 버튼
if st.button("🔄 입력/출력 지우기"):
    # Streamlit의 세션 상태를 이용해서 입력/출력 값 초기화 (페이지 새로고침 효과)
    st.session_state.input_text_area = ""
    st.session_state.output_text_area = "" # 직접 값을 바꾸기보다 키를 통해 초기화
    st.rerun() # 페이지를 다시 로드해서 변경사항 반영

st.markdown("---") # 구분선
# hareharehare_33
st.write("Made with Streamlit")