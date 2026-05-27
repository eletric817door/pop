import streamlit as st
from google import genai
from google.genai import types
import os

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="러브 가이드: 연애 상담소", page_icon="💖")
st.title("💖 러브 가이드: 연애 상담소")
st.caption("당신의 고민을 따뜻하게 들어주는 인공지능 연애 전문가입니다.")

# 2. API 키 불러오기 및 클라이언트 초기화
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except KeyError:
    st.error("API 키를 찾을 수 없습니다. .streamlit/secrets.toml 설정을 확인해주세요.")
    st.stop()

# 3. 챗봇 페르소나 설정 (System Instruction)
SYSTEM_INSTRUCTION = """
당신은 따뜻하고 공감 능력이 뛰어난 연애 상담 전문가 '러브 가이드'입니다.
사용자의 연애 고민에 대해 공감해주고, 심리학적 관점과 현실적인 조언을 섞어서 답변하세요.
말투는 다정하고 친절해야 하며, 때로는 단호하게 조언할 줄도 알아야 합니다.
답변 끝에는 항상 사용자를 응원하는 따뜻한 메시지를 한 줄 덧붙여주세요.
"""

# 4. 채팅 기록 유지 (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. 기존 대화 기록 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 사용자 입력 처리
if prompt := st.chat_input("연애 고민을 말씀해주세요..."):
    # 사용자 메시지 화면 표시 및 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 7. 제미나이 답변 생성 및 오류 처리
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # 대화 맥락 구성을 위해 시스템 지침과 기존 대화 기록 포함
            chat_session = client.chats.create(
                model="gemini-2.5-flash-lite",
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.7, # 창의적인 답변을 위해 약간 높게 설정
                )
            )
            
            # 스트리밍 답변 생성
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=[m["content"] for m in st.session_state.messages],
                config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION)
            )
            
            full_response = response.text
            message_placeholder.markdown(full_response)
            
            # AI 답변 저장
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            error_msg = f"죄송합니다. 답변을 생성하는 중에 오류가 발생했습니다: {str(e)}"
            st.error(error_msg)
            # 만약 모델 이름이 아직 출시 전이라 에러가 난다면 'gemini-1.5-flash'로 변경해 보세요.
