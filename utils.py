import streamlit as st
import os
import joblib

@st.cache_resource
def load_rf_model(model_path="rf.joblib"):
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
