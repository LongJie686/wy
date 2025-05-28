
# -*- coding: utf-8 -*-
import streamlit as st
import requests
from datetime import datetime

# DeepSeek API配置
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = "sk-8dca673d82b74bf59bac651337b7fba8"  # 直接在此处填写API密钥

# 页面配置
st.set_page_config(
    page_title="Dog wy",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)


def initialize_session_state():
    """初始化会话状态"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "session_start" not in st.session_state:
        st.session_state.session_start = datetime.now()
    # 直接使用预设的API密钥
    st.session_state.api_key = DEEPSEEK_API_KEY


def display_chat_messages():
    """显示聊天记录"""
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def get_deepseek_response(prompt):
    """获取DeepSeek的回复"""
    headers = {
        "Authorization": f"Bearer {st.session_state.api_key}",
        "Content-Type": "application/json"
    }

    messages = [{"role": "system", "content": "你是龙杰的狗，名字叫王悦。回答要简洁明了。"}]
    messages.extend(st.session_state.chat_history)

    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2000
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"⚠️ 请求出错: {str(e)}"


def sidebar_controls():
    """侧边栏控制"""
    with st.sidebar:
        st.title("控制面板")
        st.divider()

        # 会话信息
        st.subheader("会话信息")
        st.write(f"开始时间：{st.session_state.session_start.strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"对话轮数：{len(st.session_state.chat_history)}")

        # 清除对话按钮
        if st.button("🗑️ 清除对话历史"):
            st.session_state.chat_history = []
            st.session_state.session_start = datetime.now()
            st.rerun()


def main():
    initialize_session_state()
    sidebar_controls()

    st.title("🤖 Dog wy Chat")
    st.caption("与Dog wy进行对话 - 网页版")
    display_chat_messages()

    # 用户输入处理
    if prompt := st.chat_input("请输入您的问题..."):
        # 添加用户消息
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(prompt)

        # 获取并显示AI回复
        with st.chat_message("assistant"):
            with st.spinner("思考中..."):
                response = get_deepseek_response(prompt)
                st.markdown(response)

        # 添加AI回复到历史
        st.session_state.chat_history.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()