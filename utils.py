import os
import json
import joblib
import streamlit as st


@st.cache_resource
def load_model(model_path: str = "rf.joblib"):
    """Tải và cache mô hình joblib từ đĩa cứng."""
    if not os.path.exists(model_path):
        st.error(f"Không tìm thấy tệp mô hình `{model_path}`!")
        return None
    try:
        return joblib.load(model_path)
    except Exception as e:
        st.error(f"Lỗi khi tải mô hình từ `{model_path}`: {e}")
        return None


@st.cache_data
def load_data(file_path: str):
    """Đọc file JSON và trả về nội dung. Được cache theo đường dẫn file trong suốt phiên làm việc."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Không tìm thấy file: `{file_path}`")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Lỗi khi đọc tệp JSON `{file_path}`: {e}")
        return None


def create_sidebar():
    with st.sidebar:
        st.write("**Điều hướng**")
        st.page_link("app.py", label="Khảo sát")
        st.page_link("pages/dashboard.py", label="Dashboard")


def init_session_state():
    """Khởi tạo tất cả các biến session state mặc định."""
    defaults = {
        "form_submitted": False,
        "pred_clamped": None,
        "raw_pred_df": None,
        "X_df": None,
        "authenticated": False,
        "s1_path": None,
        "s1_ex1": None,
        "s1_ex2": None,
        "s2_path": None,
        "s2_ex1": None,
        "s2_ex2_done": False,
        "s3_a_done": None,
        "s3_b_done": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def reset_session_state():
    """Khôi phục tất cả các khóa session state liên quan đến khảo sát về trạng thái ban đầu."""
    keys_to_keep = ["authenticated"]
    for key in list(st.session_state.keys()):
        if key not in keys_to_keep:
            del st.session_state[key]


def scene_page_setup(scene_key: str) -> tuple[dict, float]:
    """
    Thiết lập chung cho các trang scene.

    Tải cấu hình và dữ liệu scene, cấu hình trang, chèn CSS và
    khởi tạo session state. Gọi một lần ở cấp module trong mỗi trang scene.

    Tham số:
        scene_key: Khóa sử dụng trong config.json, ví dụ: 'scene_1', 'scene_2', 'scene_3'.

    Trả về:
        (data, delay) — dict kịch bản scene đã phân tích và giá trị delay hoạt ảnh.
    """
    from ui import inject_custom_css  # import cục bộ để tránh phụ thuộc vòng lập

    config = load_data("config.json")
    st.set_page_config(
        page_title=config["display"][f"{scene_key}_title"],
        layout="centered",
    )
    data = load_data(config["script"][scene_key])
    delay: float = config["display"]["delay"]
    inject_custom_css()
    init_session_state()
    return data, delay
