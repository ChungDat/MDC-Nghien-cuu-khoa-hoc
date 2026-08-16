import warnings
import pandas as pd
import numpy as np
import streamlit as st
from utils import load_model, load_data, create_sidebar, init_session_state, reset_session_state
from db.queries import add_form, add_prediction

warnings.filterwarnings("ignore")

config = load_data("config.json")

st.set_page_config(
    page_title=config["display"]["form_title"],
    layout="wide",
)

LIKERT_FILE_PATH = config["form"]["likert"]
Q_FILE_PATH = config["form"]["questions"]
A_FILE_PATH = config["form"]["answers"]
COLS_PER_ROW = config["display"]["cols_per_row"]

init_session_state()

def _set_all_answers(questions: dict, value_fn):
    """Set all question answers in session state and rerun."""
    for q in questions:
        st.session_state[f"q_{q}"] = value_fn()
    st.rerun()

def on_model_change():
    st.session_state["form_submitted"] = False

models = {
    "Random Forest": "models/v1_rf.joblib",
    "Linear Regression": "models/v1_lr.joblib",
    "Ordinal Logistic Regression": "models/v1_olr.joblib"
}

def main():
    create_sidebar()

    st.title(config["display"]["form_header"])

    # Tải mô hình
    model_name = st.selectbox(
        "Chọn mô hình",
        options=list(models.keys()),
        index=0,
        on_change=on_model_change
    )
    
    model = load_model(models[model_name])
    if model is None:
        st.error("Không thể tải mô hình")
        st.stop()
    else:
        st.success("Đã tải mô hình thành công")
            
    # Đọc danh sách câu hỏi, danh sách chiều tác động, điểm likert
    likert_options = load_data(LIKERT_FILE_PATH)
    questions = load_data(Q_FILE_PATH)
    answers_info = load_data(A_FILE_PATH)
    
    if not questions:
        st.warning(f"Không tìm thấy câu hỏi nào trong `{Q_FILE_PATH}`")
        st.stop()

    if not answers_info:
        st.warning(f"Không tìm thấy mô tả nào trong `{A_FILE_PATH}`")
        st.stop()

    if not likert_options:
        st.warning(f"Không tìm thấy điểm Likert nào trong `{LIKERT_FILE_PATH}`")
        st.stop()
        
    # Lấy danh sách đặc trưng từ mô hình
    base_m = model[0] if isinstance(model, list) else model
    
    if hasattr(base_m, "feature_names_in_"):
        expected_features = list(base_m.feature_names_in_)
    else:
        # Fall back to using the exact keys from the questions file
        expected_features = list(questions.keys())

    expected_targets = ["PAIS_01", "PAIS_02", "PAIS_03", "PAIS_04", "PAIS_05", "PAIS_06", "PAIS_07"]
    n_targets = len(expected_targets)
    
    st.caption("Vui lòng chọn mức độ đánh giá phù hợp nhất với bạn cho từng câu hỏi bên dưới (Thang đo Likert từ 1 đến 5).")
    
    # Thanh công cụ nhanh: Chọn ngẫu nhiên / Đặt lại / Xoá câu trả lời
    col_act1, col_act2, col_act3, _ = st.columns([2, 2, 2, 4])
    with col_act1:
        if st.button("Chọn ngẫu nhiên câu trả lời"):
            _set_all_answers(questions, lambda: int(np.random.randint(1, 6)))
    with col_act2:
        if st.button("Đặt lại về Trung lập (3)"):
            _set_all_answers(questions, lambda: 3)
    with col_act3:
        if st.button("Xoá tất cả câu trả lời"):
            _set_all_answers(questions, lambda: None)

    # Form khảo sát với các Radio Button
    with st.form("likert_vietnamese_form", clear_on_submit=False):
        user_answers = {}
        
        # Nhóm câu hỏi theo tiền tố (Ví dụ: CB, FOMO, CSCT)
        prefixes = {}
        for q in questions.keys():
            prefix = q.split("_")[0] if "_" in q else "Khác"
            prefixes.setdefault(prefix, []).append(q)
            
        tabs = st.tabs([f"Nhóm {p} ({len(qs)} câu)" for p, qs in prefixes.items()])
        for tab, (p, qs) in zip(tabs, prefixes.items()):
            with tab:
                # Chú thích hiển thị bằng st.info
                legend_text = " - ".join([f"**{k}**: {v}" for k, v in likert_options.items()])
                st.info(legend_text)
                
                hcol1, hcol2 = st.columns([8, 2])
                hcol1.write("**Câu hỏi khảo sát**")
                hcol2.write("**Mức độ đánh giá (1 - 5)**")
                st.divider()

                for q in qs:
                    key = f"q_{q}"                    
                    col1, col2 = st.columns([8, 2], vertical_alignment="center")
                    col1.write(questions[q])
                    
                    with col2:
                        val = st.radio(
                            label=f"a_{q}",
                            options=[1, 2, 3, 4, 5],
                            index=None,
                            key=key,
                            horizontal=True,
                            label_visibility="collapsed"
                        )
                    if val:
                        user_answers[q] = val
                    st.divider()
                
        submit_btn = st.form_submit_button(
            "Gửi Khảo Sát & Phân Tích Kết Quả",
            type="primary",
            disabled=st.session_state["form_submitted"],
            use_container_width=True
        )

    if submit_btn:
        missing = [feat for feat in expected_features if feat not in user_answers]
        if missing:
            st.error(f"Bạn chưa chọn câu trả lời cho câu hỏi {missing[0]}")
            st.stop()
        else:
            st.session_state["form_submitted"] = True
            st.rerun()

    if st.session_state["form_submitted"]:
        # Chuẩn bị vector đặc trưng đúng theo thứ tự mô hình yêu cầu
        input_data = {}
        for feat in expected_features:
            input_data[feat] = user_answers[feat]
                
        X_df = pd.DataFrame([input_data])

        if isinstance(model, list):
            # OLR model is a list of 7 sub-models
            preds = []
            for sub_model in model:
                preds.append(sub_model.predict(X_df)[0])
            raw_pred = np.array([preds])
        else:
            raw_pred = model.predict(X_df)
            
        raw_pred_df = pd.DataFrame(raw_pred, columns=expected_targets)

        pred = np.rint(raw_pred)
        pred_clamped = np.clip(pred, 1, 5)[0] # Lấy mảng 1x7
        
        st.session_state["pred_clamped"] = pred_clamped
        st.session_state["raw_pred_df"] = raw_pred_df
        st.session_state["X_df"] = X_df

        avg_pais = float(np.mean(pred_clamped))

        output_data = {}
        for i, feat in enumerate(expected_targets):
            output_data[feat] = int(pred_clamped[i])
        output_data["PAIS_AVG"] = avg_pais

        try:
            input_data_db = {str(key).lower(): value for key, value in input_data.items()}
            output_data_db = {str(key).lower(): value for key, value in output_data.items()}

            form_id = add_form(input_data_db)
            add_prediction(form_id, output_data_db, model_name=model_name)
        except Exception as e:
            st.error(f"Lỗi trong quá trình lưu kết quả dự đoán: {e}")
        
        st.header("Kết quả dự đoán tác động tâm lý")
        
        for i, (ans_code, ans_desc) in enumerate(answers_info.items()):
            if i % COLS_PER_ROW == 0:
                cols = st.columns(COLS_PER_ROW)
            if i < n_targets:
                score = int(pred_clamped[i])

                with cols[i % COLS_PER_ROW]:
                    st.metric(label=ans_code, value=f"Mức {score}/5")
                    st.caption(ans_desc)
        st.write("")

        with st.expander("Chi tiết dữ liệu đầu vào và giá trị chưa làm tròn"):
            st.write("**Vector dữ liệu khảo sát:**")
            st.dataframe(X_df, use_container_width=True)
            
            st.write("**Giá trị dự đoán gốc từ mô hình:**")
            st.dataframe(raw_pred_df, use_container_width=True)

        if st.button("Tiếp tục", type="primary", use_container_width=True):
            if avg_pais <= config["script"]["low_threshold"]:
                st.switch_page("pages/scene_1.py")
            elif avg_pais <= config["script"]["high_threshold"]:
                st.switch_page("pages/scene_2.py")
            else:
                st.switch_page("pages/scene_3.py")

main()
