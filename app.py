import streamlit as st
from openai import OpenAI

# 1. 웹페이지 제목 및 레이아웃 설정
st.set_page_config(page_title="나만의 AI 챗봇", page_icon="🤖")
st.title("🤖 나만의 AI 챗봇")
st.caption("OpenAI API를 활용한 실시간 대화형 챗봇입니다.")

# 2. 사이드바에서 API 키 입력 받기
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[OpenAI API Key 발급받기](https://platform.openai.com/api-keys)"

# 3. 대화 기록 초기화 (대화가 끊기지 않고 이어지도록 세션에 저장)
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요! 무엇을 도와드릴까요?"}]

# 4. 기존 대화 기록을 화면에 표시
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 5. 사용자 입력 처리
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("시작하려면 사이드바에 OpenAI API 키를 입력해 주세요.")
        st.stop()

    # 클라이언트 초기화
    client = OpenAI(api_key=openai_api_key)
    
    # 사용자가 입력한 메시지를 화면에 표시하고 기록에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 6. OpenAI API를 통해 답변 생성
    with st.chat_message("assistant"):
        # 실시간으로 답변이 타이핑되는 효과(Stream) 적용
        stream = client.chat.completions.create(
            model="gpt-4o-mini", # 가성비가 가장 좋은 모델입니다. (원하면 gpt-4o 등으로 변경 가능)
            messages=st.session_state.messages,
            stream=True
        )
        response = st.write_stream(stream)
    
    # AI의 답변을 기록에 추가
    st.session_state.messages.append({"role": "assistant", "content": response})
