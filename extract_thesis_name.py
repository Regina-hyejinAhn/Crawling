import os
import re
import PyPDF2
import pdfplumber

# PDF에서 제목과 출판년도를 추출하는 함수
def extract_title_and_year(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]  # 첫 페이지 텍스트 추출
        text = first_page.extract_text()

        # 제목과 출판년도를 추출하기 위한 정규식 패턴 설정 (간단 예시)
        title_pattern = re.compile(r'(?<=Title:\s)(.*)')
        year_pattern = re.compile(r'\b(19|20)\d{2}\b')  # 1900년대, 2000년대 연도 패턴

        title_match = title_pattern.search(text)
        year_match = year_pattern.search(text)

        # 제목과 출판년도 추출
        title = title_match.group(1) if title_match else "Unknown_Title"
        year = year_match.group(0) if year_match else "Unknown_Year"

        return title, year

# 새로운 파일 이름으로 저장하는 함수
def save_with_new_name(pdf_path):
    title, year = extract_title_and_year(pdf_path)
    # 제목과 출판년도를 결합하여 파일명 생성
    new_file_name = f"{title}_{year}.pdf".replace(" ", "_")  # 공백을 '_'로 대체
    new_file_path = os.path.join(os.path.dirname(pdf_path), new_file_name)
    os.rename(pdf_path, new_file_path)
    print(f"파일이 {new_file_path}로 저장되었습니다.")

# PDF 파일 경로 설정 (사용자가 제공한 파일 경로로 설정)
pdf_path = "논문.pdf"  # 이 부분을 업로드된 파일 경로로 대체
save_with_new_name(pdf_path)