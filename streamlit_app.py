import streamlit as st
import re

# --- split_by_punctuation 함수 (변경 없음) ---
def split_by_punctuation(text):
    if not text: return []
    result = []
    parts = re.split(r'(。|」|』|？|！)', text)
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

# --- 텍스트 변환 핵심 로직 함수 (변경 없음) ---
def convert_vertical_to_horizontal_logic(input_text):
    lines = input_text.strip().split('\n')
    paragraphs = []
    paragraph = ''
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if paragraph: paragraphs.append(paragraph); paragraph = ''
        elif not stripped.isdigit():
             paragraph += stripped
    if paragraph: paragraphs.append(paragraph)

    result_lines = []
    for line in paragraphs:
        line = line.strip()
        if not line: continue
        cleaned_line = re.sub(r'^\s*\d+[\s\.]*\s*', '', line).strip()
        if not cleaned_line: continue
        result_lines.extend(split_by_punctuation(cleaned_line))
    return "\n".join(result_lines)

# --- Streamlit 웹 화면 구성 (수정됨) ---

# 1. 세션 상태 초기화 (앱 처음 로드 시 또는 새로고침 시 한 번만 실행)
#    입력값과 출력값을 저장할 공간을 미리 만들어 둡니다.
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""
if 'output_text' not in st.session_state:
    st.session_state.output_text = ""

st.set_page_config(page_title="세로쓰기 → 가로쓰기 변환기", layout="wide")
st.title("📝 일본어 세로쓰기 → 가로쓰기 변환기")
st.caption("세로쓰기 대본을 복사해서 붙여넣으면 가로쓰기로 변환하고 문장 단위로 줄을 나눠줍니다.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("세로쓰기 텍스트 입력:")
    # 2. 입력 상자: value를 session_state와 연결하고, on_change로 입력 시 session_state 업데이트
    #    이렇게 하면 사용자가 입력하는 즉시 st.session_state.input_text 값이 바뀝니다.
    def update_input():
        st.session_state.input_text = st.session_state.input_widget # 위젯의 현재 값을 input_text 상태로 복사
    st.text_area("여기에 붙여넣으세요 👇", value=st.session_state.input_text, height=400, key="input_widget", on_change=update_input)

with col2:
    st.subheader("변환 결과:")

    # 3. 변환 버튼: 클릭 시 로직 실행 후 결과를 output_text 세션 상태에 저장
    if st.button("✨ 가로로 변환하기"):
        if st.session_state.input_text:
            # 변환 결과를 output_text 세션 상태에 저장
            st.session_state.output_text = convert_vertical_to_horizontal_logic(st.session_state.input_text)
        else:
            st.warning("입력창에 텍스트를 먼저 넣어주세요!")
            st.session_state.output_text = "" # 입력 없으면 출력도 비움

    # 4. 출력 상자: value를 output_text 세션 상태와 연결
    st.text_area("결과 👇 (직접 복사해서 사용하세요)", value=st.session_state.output_text, height=400, key="output_widget", help="변환된 텍스트입니다.")

# 5. 지우기 버튼: 클릭 시 input_text와 output_text 세션 상태를 직접 비움
#    이렇게 상태를 바꾸면 Streamlit이 자동으로 화면을 다시 그려서 빈 상자가 표시됩니다.
if st.button("🔄 입력/출력 지우기"):
    st.session_state.input_text = ""
    st.session_state.output_text = ""
    # st.rerun()은 여기서 명시적으로 호출할 필요 없음 (상태 변경 시 자동 리런)

st.markdown("---")
st.write("Made with Streamlit")
