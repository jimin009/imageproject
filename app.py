import streamlit as st
import openai
from PIL import Image
import requests
from io import BytesIO
import os

# 프롬프트 예시
PROMPT_EXAMPLE = "예시: '운동화, 파란색, 심플한 디자인'"

st.title('신발 이미지 생성기 (GPT-4o)')
st.write('아래 예시를 참고해 신발 종류와 원하는 색상, 디자인을 입력하세요.')
st.info(PROMPT_EXAMPLE)

# 사용자 입력
shoe_type = st.text_input('신발 종류를 입력하세요 (예: 운동화, 구두 등)')
color_design = st.text_input('좋아하는 색이나 디자인을 입력하세요 (예: 파란색, 심플한 디자인 등)')

# OpenAI API Key (직접 코드에 입력, 사용자 입력란 제거)
import os
from dotenv import load_dotenv

load_dotenv()

# --- OpenAI API KEY ---
openai.api_key = os.getenv("OPENAI_API_KEY")

if st.button('이미지 생성'):
    if not (shoe_type and color_design):
        st.warning('모든 입력란을 채워주세요.')
    else:
        prompt = f"{shoe_type}, {color_design} 신발의 실사 이미지"
        st.write(f"프롬프트: {prompt}")
        try:
            response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="1024x1024"  # 지원되는 해상도로 변경
            )
            image_url = response.data[0].url
            image_response = requests.get(image_url)
            img = Image.open(BytesIO(image_response.content))
            st.image(img, caption='생성된 신발 이미지', use_column_width=True)
            # 다운로드 버튼
            img_bytes = BytesIO()
            img.save(img_bytes, format='PNG')
            st.download_button(
                label="이미지 다운로드",
                data=img_bytes.getvalue(),
                file_name="generated_shoe.png",
                mime="image/png"
            )
        except Exception as e:
            st.error(f"이미지 생성 중 오류 발생: {e}")


