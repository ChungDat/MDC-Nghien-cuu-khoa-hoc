import streamlit as st
import os
import joblib
import json

@st.cache_resource
def load_model(model_path="rf.joblib"):
    if not os.path.exists(model_path):
        st.error(f"Không tìm thấy tệp mô hình `{model_path}`!")
        return None
    try:
        model = joblib.load(model_path)
        return model
    except Exception as e:
        st.error(f"Lỗi khi tải mô hình từ `{model_path}`: {e}")
        return None

def parse_code_text_file(file_path):
    """Đọc động các tệp định dạng 'code: text'"""
    items = []
    if not os.path.exists(file_path):
        return items
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if not line_str or line_str.startswith("#"):
                continue
            if ":" in line_str:
                parts = line_str.split(":", 1)
                code = parts[0].strip()
                text = parts[1].strip()
            else:
                code = f"ITEM_{len(items)+1:02d}"
                text = line_str
            items.append({"code": code, "text": text})
    return items

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def inject_custom_css():
    st.markdown("""
<style>
@keyframes floatUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
.fade-in {
    animation: floatUp 0.8s ease-out both;
}
.chat-container {
    display: flex;
    flex-direction: column;
    width: 100%;
}
.chat-bubble {
    background-color: #2b2b2b;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 15px;
    color: #ffffff;
    font-size: 16px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    max-width: 85%;
    align-self: flex-start;
    white-space: pre-wrap;
}
.chat-bubble-user {
    background-color: #007bff;
    color: white;
    align-self: flex-end;
}
/* Light mode support */
@media (prefers-color-scheme: light) {
    .chat-bubble {
        background-color: #f1f1f1;
        color: #333333;
    }
    .chat-bubble-user {
        background-color: #007bff;
        color: white;
    }
}
</style>
""", unsafe_allow_html=True)

def render_text(text, delay=0, key=None):
    anim_delay = 0
    if delay > 0 and key:
        if key not in st.session_state:
            st.session_state[key] = True
            anim_delay = delay
            
    style = f"animation-delay: {anim_delay}s;" if anim_delay > 0 else ""
    st.markdown(f'<div class="chat-container"><div class="fade-in chat-bubble" style="{style}">{text}</div></div>', unsafe_allow_html=True)
    
    if anim_delay > 0:
        st.markdown(f"""
        <style>
        div.stButton {{
            animation: floatUp 0.8s ease-out both !important;
            animation-delay: {anim_delay}s !important;
        }}
        </style>
        """, unsafe_allow_html=True)

def render_user_text(text, delay=0, key=None):
    anim_delay = 0
    if delay > 0 and key:
        if key not in st.session_state:
            st.session_state[key] = True
            anim_delay = delay
            
    style = f"animation-delay: {anim_delay}s;" if anim_delay > 0 else ""
    st.markdown(f'<div class="chat-container"><div class="fade-in chat-bubble chat-bubble-user" style="{style}">{text}</div></div>', unsafe_allow_html=True)

    if anim_delay > 0:
        st.markdown(f"""
        <style>
        div.stButton {{
            animation: floatUp 0.8s ease-out both !important;
            animation-delay: {anim_delay}s !important;
        }}
        </style>
        """, unsafe_allow_html=True)
