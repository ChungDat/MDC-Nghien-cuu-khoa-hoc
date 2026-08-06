import warnings
import pandas as pd
import numpy as np
import streamlit as st
from utils import load_model, load_data

# Tắt cảnh báo phiên bản unpickle của sklearn
warnings.filterwarnings("ignore")

config = load_data("config.json")

# Cấu hình trang Streamlit
st.set_page_config(
    page_title=config["display"]["form_title"],
    page_icon="📋",
    layout="wide",
)

LINKERT_FILE_PATH = config["form"]["linkert"]
Q_FILE_PATH = config["form"]["questions"]
A_FILE_PATH = config["form"]["answers"]
COLS_PER_ROW = config["display"]["cols_per_row"]


def main():
    st.title(config["display"]["form_header"])
    
    # Tải mô hình
    model = load_model(config["model"])
    if model is None:
        st.stop()
        
    # Lấy danh sách đặc trưng dự kiến từ mô hình
    if hasattr(model, "feature_names_in_"):
        expected_features = list(model.feature_names_in_)
    else:
        n_features = getattr(model, "n_features_in_", 26)
        expected_features = [f"F_{i+1:02d}" for i in range(n_features)]
        
    n_outputs = getattr(model, "n_outputs_", 7)

    # Đọc danh sách câu hỏi, danh sách chiều tác động, điểm linkert
    linkert_options = load_data(LINKERT_FILE_PATH)
    questions = load_data(Q_FILE_PATH)
    answers_info = load_data(A_FILE_PATH)
    
    if not questions:
        st.warning(f"Không tìm thấy câu hỏi nào trong `{Q_FILE_PATH}`")
        st.stop()

    if not answers_info:
        st.warning(f"Không tìm thấy mô tả nào trong `{A_FILE_PATH}`")
        st.stop()

    if not linkert_options:
        st.warning(f"Không tìm thấy điểm Likert nào trong `{LINKERT_FILE_PATH}`")
        st.stop()
        
    st.caption("Vui lòng chọn mức độ đánh giá phù hợp nhất với bạn cho từng câu hỏi bên dưới (Thang đo Likert từ 1 đến 5).")
    
    # Thanh công cụ nhanh: Chọn ngẫu nhiên / Đặt lại / Xoá câu trả lời
    col_act1, col_act2, col_act3, _ = st.columns([2, 2, 2, 4])
    with col_act1:
        if st.button("Chọn ngẫu nhiên câu trả lời"):
            for q in questions.keys():
                st.session_state[f"q_{q}"] = int(np.random.randint(1, 6))
            st.rerun()
    with col_act2:
        if st.button("Đặt lại về Trung lập (3)"):
            for q in questions.keys():
                st.session_state[f"q_{q}"] = 3
            st.rerun()
    with col_act3:
        if st.button("Xoá tất cả câu trả lời"):
            for q in questions.keys():
                st.session_state[f"q_{q}"] = None
            st.rerun()

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
                legend_text = " - ".join([f"**{k}**: {v}" for k, v in linkert_options.items()])
                st.info(legend_text)
                
                hcol1, hcol2 = st.columns([8, 2])
                hcol1.write("**Câu hỏi khảo sát**")
                hcol2.write("**Mức độ đánh giá (1 - 5)**")
                st.divider()

                for q in qs:
                    key = f"q_{q}"
                    default_val = st.session_state.get(key, 3)
                    
                    col1, col2 = st.columns([8, 2], vertical_alignment="center")
                    col1.write(f"{questions[q]}")
                    
                    with col2:
                        val = st.radio(
                            label=f"Chọn câu trả lời cho {q}",
                            options=[1, 2, 3, 4, 5],
                            index=None,
                            key=key,
                            horizontal=True,
                            label_visibility="collapsed"
                        )
                    if val:
                        user_answers[q] = val
                    st.divider()
                
        submit_btn = st.form_submit_button("Gửi Khảo Sát & Phân Tích Kết Quả", type="primary", use_container_width=True)

    # Xử lý kết quả dự đoán
    if submit_btn:
        # Chuẩn bị vector đặc trưng đúng theo thứ tự mô hình yêu cầu
        input_data = {}
        for feat in expected_features:
            if feat in user_answers:
                input_data[feat] = user_answers[feat]
            else:
                st.error(f"Bạn chưa chọn câu trả lời cho câu hỏi {feat}")
                st.stop()
                
        X_df = pd.DataFrame([input_data])
        
        try:
            # Thực hiện dự đoán với Random Forest
            raw_pred = model.predict(X_df)
            raw_pred_df = pd.DataFrame(raw_pred, columns=['PAIS_01', 'PAIS_02', 'PAIS_03', 'PAIS_04', 'PAIS_05', 'PAIS_06', 'PAIS_07'])
            pred = np.round(raw_pred)
            pred_clamped = np.clip(pred, 1, 5)[0]  # Lấy mảng 1x7
            
            st.header("Kết quả dự đoán tác động tâm lý")
            
            for i, (ans_code, ans_desc) in enumerate(answers_info.items()):
                if i % COLS_PER_ROW == 0:
                    cols = st.columns(COLS_PER_ROW)
                if i < n_outputs:
                    score = int(pred_clamped[i])

                    with cols[i % COLS_PER_ROW]:
                        st.metric(label=f"{ans_code}", value=f"Mức {score}/5")
                        st.caption(f"{ans_desc}")
                st.write("")

            # Khung chi tiết dữ liệu
            with st.expander("Chi tiết dữ liệu đầu vào và giá trị chưa làm tròn"):
                st.write("**Vector dữ liệu khảo sát:**")
                st.dataframe(X_df, use_container_width=True)
                
                st.write("**Giá trị dự đoán gốc từ mô hình:**")
                st.dataframe(raw_pred_df, use_container_width=True)
                
        except Exception as e:
            st.error(f"Lỗi trong quá trình tính toán dự đoán: {e}")

if __name__ == "__main__":
    main()
