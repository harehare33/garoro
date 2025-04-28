import tkinter as tk
import tkinter.font as tkfont
import re

# --- split_by_punctuation 함수는 이전 버전 그대로 두세요 ---
# (이전 답변에서 ...을 제외하도록 수정한 버전 사용)
def split_by_punctuation(text):
    # ... (이전 답변의 최종 버전 내용) ...
    if not text: return []
    result = []
    parts = re.split(r'(。|」|』|？|！)', text) # 줄임표 제외
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
# --- split_by_punctuation 함수 끝 ---


def convert_text():
    input_text = input_box.get("1.0", tk.END)

    # 1. 모든 줄을 붙여서 단락 복원 (⭐ 숫자 줄 필터링 추가)
    lines = input_text.strip().split('\n')
    paragraphs = []
    paragraph = ''

    for line in lines:
        stripped = line.strip() # 각 줄의 앞뒤 공백 제거
        if not stripped: # 빈 줄이면 단락 구분
            if paragraph:
                paragraphs.append(paragraph)
                paragraph = ''
        else:
            # ⭐⭐⭐ 핵심 수정: 현재 줄(stripped)이 숫자로만 되어 있는지 확인! ⭐⭐⭐
            if not stripped.isdigit(): # 숫자로만 된 줄이 *아니라면* (즉, 글자나 기호가 있다면)
                paragraph += stripped # 가로 문장에 이어붙임
            # else: 숫자로만 된 줄이면 아무것도 안 하고 넘어감 (무시!)

    # 마지막 줄 처리
    if paragraph:
        paragraphs.append(paragraph)

    # 2. 한 문단씩 처리 (이제 paragraph에는 숫자가 섞여있지 않음)
    result_lines = []
    for line in paragraphs: # 이제 이 line은 '178「사、' 이런 식이 아니라 '「사、' 형태일 것임
        line = line.strip()
        if not line:
            continue

        # (선택사항) 맨 앞의 숫자 제거 로직은 여전히 유용할 수 있으니 남겨둡니다.
        # (혹시 '1. 대사' 처럼 붙어있는 경우 대비)
        cleaned_line = re.sub(r'^\s*\d+[\s\.]*\s*', '', line).strip()

        if not cleaned_line:
            continue

        # 🔸 SE: 단위로 나누기 (기존과 동일)
        if 'SE:' in cleaned_line:
            parts = re.split(r'(SE:.*?)(?=\s*SE:|$)', cleaned_line)
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                if part.startswith('SE:'):
                    result_lines.append(part)
                else:
                    result_lines.extend(split_by_punctuation(part))
        else:
            # 🔹 일반 문장은 문장부호로만 분리 (기존과 동일)
            result_lines.extend(split_by_punctuation(cleaned_line))

    # 3. 결과 합치기
    result = '\n'.join(result_lines)

    # 출력창에 넣기
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, result)


def clear_input():
    input_box.delete("1.0", tk.END)
    output_box.delete("1.0", tk.END)


# --- 이하 Tkinter GUI 설정 코드는 동일 ---
# ... (창 설정, 폰트, 입력창, 버튼, 출력창 코드) ...
# 창 설정
root = tk.Tk()
root.title("세로쓰기 → 가로쓰기 변환기")
root.geometry("600x500")

# 폰트 설정 (BIZ UDPゴシック 폰트가 없으면 다른 일본어 지원 폰트로 변경하세요)
try:
    custom_font = tkfont.Font(family="BIZ UDPゴシック", size=13)
except tk.TclError:
    try:
        custom_font = tkfont.Font(family="Yu Gothic", size=13) # 다른 예시 폰트
    except tk.TclError:
        custom_font = tkfont.Font(size=13) # 기본 폰트

# 입력창
input_box = tk.Text(root, height=10, font=custom_font)
input_box.pack(padx=10, pady=(10, 5), fill="both", expand=True)

# 버튼 프레임
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

btn_convert = tk.Button(button_frame, text="가로로 변환", command=convert_text, width=15)
btn_convert.pack(side="left", padx=5)

btn_clear = tk.Button(button_frame, text="입력 전체 삭제", command=clear_input, width=15)
btn_clear.pack(side="left", padx=5)

# 출력창 + 스크롤바
output_frame = tk.Frame(root)
output_frame.pack(padx=10, pady=(5, 10), fill="both", expand=True)

scrollbar = tk.Scrollbar(output_frame)
scrollbar.pack(side="right", fill="y")

output_box = tk.Text(output_frame, height=10, font=custom_font, bg="#f0f0f0", wrap="word", yscrollcommand=scrollbar.set)
output_box.pack(side="left", fill="both", expand=True)
scrollbar.config(command=output_box.yview)

# 실행
root.mainloop()

def clear_input():
    input_box.delete("1.0", tk.END)
    output_box.delete("1.0", tk.END)

# --- 이하 Tkinter GUI 설정 코드는 동일 ---
# 창 설정
root = tk.Tk()
root.title("세로쓰기 → 가로쓰기 변환기")
root.geometry("600x500")

# 폰트 설정 (BIZ UDPゴシック 폰트가 없으면 다른 일본어 지원 폰트로 변경하세요)
try:
    custom_font = tkfont.Font(family="BIZ UDPゴシック", size=13)
except tk.TclError:
    try:
        custom_font = tkfont.Font(family="Yu Gothic", size=13) # 다른 예시 폰트
    except tk.TclError:
        custom_font = tkfont.Font(size=13) # 기본 폰트

# 입력창
input_box = tk.Text(root, height=10, font=custom_font)
input_box.pack(padx=10, pady=(10, 5), fill="both", expand=True)

# 버튼 프레임
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

btn_convert = tk.Button(button_frame, text="가로로 변환", command=convert_text, width=15)
btn_convert.pack(side="left", padx=5)

btn_clear = tk.Button(button_frame, text="입력 전체 삭제", command=clear_input, width=15)
btn_clear.pack(side="left", padx=5)

# 출력창 + 스크롤바
output_frame = tk.Frame(root)
output_frame.pack(padx=10, pady=(5, 10), fill="both", expand=True)

scrollbar = tk.Scrollbar(output_frame)
scrollbar.pack(side="right", fill="y")

output_box = tk.Text(output_frame, height=10, font=custom_font, bg="#f0f0f0", wrap="word", yscrollcommand=scrollbar.set)
output_box.pack(side="left", fill="both", expand=True)
scrollbar.config(command=output_box.yview)

# 실행
root.mainloop()