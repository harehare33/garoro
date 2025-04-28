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
        is_terminator = part in ['。', '」', '』', '？', '！'] # 이전 오타 수정됨
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

# --- 텍스트 변환 핵심 로직 함수 (캐싱 유지) ---
@st.cache_data
def convert_vertical_to_horizontal_logic(input_text):
    print(f"캐시되지 않음: '{input_text[:20]}...' 변환 로직 실행 중")
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

# 세션 상태 초기화
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""
if 'output_text' not in st.session_state:
    st.session_state.output_text = ""
# input_widget 키가 없을 경우를 대비한 초기화 (안전장치)
if 'input_widget' not in st.session_state:
    st.session_state.input_widget = ""

st.set_page_config(page_title="일본어 세로쓰기 → 가로쓰기 변환기", layout="wide")
st.title("📝 일본어 세로쓰기 → 가로쓰기 변환기")
st.caption("세로쓰기 대본을 복사해서 붙여넣으면 가로쓰기로 변환하고 문장 단위로 줄을 나눠줍니다.")

col1, col2 = st.columns(2) # 좌우 영역 분할

with col1: # 왼쪽 칸: 입력 영역
    st.subheader("세로쓰기 텍스트 입력:")
    # ⭐ on_change 콜백은 제거하거나 유지해도 되지만, 버튼 로직에서 직접 위젯 키를 사용하므로 필수는 아님.
    #    여기서는 일단 제거하여 단순화 시도.
    # def update_input():
    #     st.session_state.input_text = st.session_state.input_widget
    st.text_area("여기에 붙여넣으세요 👇", value=st.session_state.input_text, height=400, key="input_widget", placeholder="복사한 세로쓰기 텍스트를 붙여넣어주세요...")
    # ⭐ input_text 상태는 지우기 버튼 등 다른 곳에서 사용될 수 있으므로 value 연결은 유지.

with col2: # 오른쪽 칸: 출력 영역
    st.subheader("변환 결과:")
    st.text_area("결과 👇 (직접 선택해서 복사하세요)", value=st.session_state.output_text, height=400, key="output_widget", help="변환된 텍스트입니다. 마우스로 선택 후 Ctrl+C (Cmd+C)로 복사하세요.")
    # disabled=True 제거됨

# --- 페이지 하단 중앙 버튼 영역 (수정됨) ---
st.markdown("---")
_, center_col, _ = st.columns([1, 1.5, 1])
with center_col:
    if st.button("✨ 가로로 변환하기", use_container_width=True):
        # ⭐ 버튼 클릭 시점의 input_widget 값을 직접 사용!
        current_input_value = st.session_state.get('input_widget', '') # 위젯 키가 없을 경우 빈 문자열 반환
        if current_input_value:
            # 변환 로직에 현재 위젯 값 전달
            st.session_state.output_text = convert_vertical_to_horizontal_logic(current_input_value)
            # 입력 상태(input_text)도 현재 위젯 값으로 동기화 (선택사항)
            st.session_state.input_text = current_input_value
        else:
            st.warning("입력창에 텍스트를 먼저 넣어주세요!")
            st.session_state.output_text = ""
            st.session_state.input_text = "" # 입력 상태도 비움

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔄 입력/출력 모두 지우기", use_container_width=True):
        # ⭐ 지우기 버튼: input_widget의 상태와 input_text 상태 모두 초기화
        st.session_state.input_text = ""
        st.session_state.output_text = ""
        st.session_state.input_widget = "" # 입력 위젯 자체의 상태도 초기화
        # 캐시 지우기 (선택사항)
        # convert_vertical_to_horizontal_logic.clear()
        st.rerun()

# --- 페이지 맨 아래 (변경 없음) ---
st.write("@hareharehare_33")

