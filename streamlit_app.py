import streamlit as st
import re
import pyperclip # 클립보드 사용 위해 추가

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

# 세션 상태 초기화 (앱 처음 로드 시 또는 새로고침 시 한 번만 실행)
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""
if 'output_text' not in st.session_state:
    st.session_state.output_text = ""
# 복사 성공/실패 메시지 표시용 상태
if 'copy_message' not in st.session_state:
    st.session_state.copy_message = ""
if 'copy_message_type' not in st.session_state: # success, info, error 구분용
    st.session_state.copy_message_type = ""

st.set_page_config(page_title="일본어 세로쓰기 → 가로쓰기 변환기", layout="wide") # 페이지 넓게 사용
st.title("📝 일본어 세로쓰기 → 가로쓰기 변환기")
st.caption("세로쓰기 대본을 복사해서 붙여넣으면 가로쓰기로 변환하고 문장 단위로 줄을 나눠줍니다.")

col1, col2 = st.columns(2) # 좌우 영역 분할

with col1: # 왼쪽 칸: 입력 영역
    st.subheader("세로쓰기 텍스트 입력:")
    # 입력값 변경 시 세션 상태 업데이트하는 함수
    def update_input():
        st.session_state.input_text = st.session_state.input_widget
    # 텍스트 입력 상자 (높이 조정, on_change 콜백 설정)
    st.text_area("여기에 붙여넣으세요 👇", value=st.session_state.input_text, height=400, key="input_widget", on_change=update_input, placeholder="복사한 세로쓰기 텍스트를 붙여넣어주세요...")

with col2: # 오른쪽 칸: 출력 영역 및 버튼
    st.subheader("변환 결과:")
    # 결과 텍스트 출력 상자 (높이 조정, 읽기 전용 느낌으로 disabled 설정)
    st.text_area("결과 👇", value=st.session_state.output_text, height=360, key="output_widget", help="변환된 텍스트입니다.", disabled=True)

    # 버튼들을 가로로 나란히 배치하기 위한 컬럼 분할
    btn_col_1, btn_col_2 = st.columns(2)

    with btn_col_1: # 왼쪽 버튼 칸 (변환 버튼)
        # '가로로 변환하기' 버튼
        if st.button("✨ 가로로 변환하기", use_container_width=True): # 버튼 너비 채우기
            if st.session_state.input_text: # 입력값이 있으면 변환 실행
                st.session_state.output_text = convert_vertical_to_horizontal_logic(st.session_state.input_text)
                st.session_state.copy_message = "" # 변환 시 복사 메시지 초기화
                st.session_state.copy_message_type = ""
            else: # 입력값이 없으면 경고
                st.warning("입력창에 텍스트를 먼저 넣어주세요!")
                st.session_state.output_text = ""
                st.session_state.copy_message = ""
                st.session_state.copy_message_type = ""

    with btn_col_2: # 오른쪽 버튼 칸 (복사 버튼)
        # '결과 복사하기' 버튼
        if st.button("📋 결과 복사하기", use_container_width=True):
            if st.session_state.output_text: # 복사할 내용이 있으면
                try:
                    pyperclip.copy(st.session_state.output_text)
                    st.session_state.copy_message = "✅ 클립보드에 복사되었습니다!"
                    st.session_state.copy_message_type = "success"
                except Exception as e: # pyperclip 오류 발생 시 (웹 환경 등)
                    st.error(f"클립보드 복사 중 오류 발생. 웹 환경에서는 지원되지 않을 수 있습니다.")
                    st.session_state.copy_message = "❌ 복사 실패. 직접 복사해주세요."
                    st.session_state.copy_message_type = "error"
            else: # 복사할 내용이 없으면 안내
                st.session_state.copy_message = "ℹ️ 복사할 내용이 없습니다."
                st.session_state.copy_message_type = "info"

    # 복사 결과 메시지 표시 (조건부)
    if st.session_state.copy_message:
        if st.session_state.copy_message_type == "success":
            st.success(st.session_state.copy_message, icon="✅")
        elif st.session_state.copy_message_type == "info":
            st.info(st.session_state.copy_message, icon="ℹ️")
        elif st.session_state.copy_message_type == "error":
             st.error(st.session_state.copy_message, icon="❌")
        # 메시지 표시 후 초기화 (버튼 또 누르기 전까지 유지됨)
        # st.session_state.copy_message = "" # <- 이걸 넣으면 메시지가 바로 사라짐

# --- 입력/출력 모두 지우기 버튼 (페이지 하단 중앙 정렬 느낌) ---
st.markdown("<br>", unsafe_allow_html=True) # 버튼 위에 약간의 간격 추가

# 지우기 버튼을 중앙에 배치하기 위해 컬럼 사용 (약간의 트릭)
_, center_col, _ = st.columns([1, 1, 1]) # 3개 컬럼으로 나누고 가운데 컬럼만 사용
with center_col:
    if st.button("🔄 입력/출력 모두 지우기", use_container_width=True):
        st.session_state.input_text = ""
        st.session_state.output_text = ""
        st.session_state.copy_message = "" # 메시지 상태도 초기화
        st.session_state.copy_message_type = ""
        st.rerun() # 상태 변경 후 즉시 화면 갱신 원하면 사용

# --- 페이지 맨 아래 ---
st.markdown("---")
st.write("@hareharehare_33")
