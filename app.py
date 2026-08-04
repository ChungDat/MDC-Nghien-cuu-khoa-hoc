import warnings
import pandas as pd
import numpy as np
import streamlit as st
from utils import load_rf_model, parse_code_text_file

# Tắt cảnh báo phiên bản unpickle của sklearn
warnings.filterwarnings("ignore")

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Khảo sát thực trạng tổn thương trên không gian mạng và hệ quả học đường",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Thang đo Likert tiếng Việt (1 đến 5)
with open('config/linkert.txt', 'r', encoding='utf-8') as f:
    LIKERT_OPTIONS = {i+1: line.strip() for i, line in enumerate(f)}

Q_FILE_PATH = "config/questions.txt"
A_FILE_PATH = "config/answers.txt"

def main():
    # Header ứng dụng bằng component chuẩn của Streamlit
    st.title("Khảo sát thực trạng tổn thương trên không gian mạng và hệ quả học đường")
    
    # Tải mô hình
    rf_model = load_rf_model("rf.joblib")
    if rf_model is None:
        st.stop()
        
    # Lấy danh sách đặc trưng dự kiến từ mô hình
    if hasattr(rf_model, "feature_names_in_"):
        expected_features = list(rf_model.feature_names_in_)
    else:
        n_features = getattr(rf_model, "n_features_in_", 26)
        expected_features = [f"F_{i+1:02d}" for i in range(n_features)]
        
    n_outputs = getattr(rf_model, "n_outputs_", 7)

    # Đọc danh sách câu hỏi và danh sách chiều tác động (answers)
    questions = parse_code_text_file(Q_FILE_PATH)
    answers_info = parse_code_text_file(A_FILE_PATH)
    
    if not questions:
        st.warning(f"Không tìm thấy câu hỏi nào trong `{Q_FILE_PATH}`")
        st.stop()
        
    st.caption("Vui lòng chọn mức độ đánh giá phù hợp nhất với bạn cho từng câu hỏi bên dưới (Thang đo Likert từ 1 đến 5).")
    
    # Thanh công cụ nhanh: Chọn ngẫu nhiên / Đặt lại
    col_act1, col_act2, col_act3, _ = st.columns([2, 2, 2, 4])
    with col_act1:
        if st.button("🎲 Chọn ngẫu nhiên câu trả lời"):
            for q in questions:
                st.session_state[f"q_{q['code']}"] = int(np.random.randint(1, 6))
            st.rerun()
    with col_act2:
        if st.button("🧹 Đặt lại về Trung lập (3)"):
            for q in questions:
                st.session_state[f"q_{q['code']}"] = 3
            st.rerun()
    with col_act3:
        if st.button("Xoá tất cả câu trả lời"):
            for q in questions:
                st.session_state[f"q_{q['code']}"] = None
            st.rerun()

    # Form khảo sát với các Radio Button
    with st.form("likert_vietnamese_form", clear_on_submit=False):
        user_answers = {}
        
        # Nhóm câu hỏi theo tiền tố (Ví dụ: CB, FOMO, CSCT)
        prefixes = {}
        for q in questions:
            prefix = q["code"].split("_")[0] if "_" in q["code"] else "Khác"
            prefixes.setdefault(prefix, []).append(q)
            
        tabs = st.tabs([f"Nhóm {p} ({len(qs)} câu)" for p, qs in prefixes.items()])
        for tab, (p, qs) in zip(tabs, prefixes.items()):
            with tab:
                # Chú thích hiển thị bằng st.info
                legend_text = " - ".join([f"**{k}**: {v}" for k, v in LIKERT_OPTIONS.items()])
                st.info(legend_text)
                
                # Header row for the table-like layout
                hcol1, hcol2 = st.columns([8, 2])
                hcol1.write("**Câu hỏi khảo sát**")
                hcol2.write("**Mức độ đánh giá (1 - 5)**")
                st.divider()

                for q in qs:
                    key = f"q_{q['code']}"
                    default_val = st.session_state.get(key, 3)
                    
                    col1, col2 = st.columns([8, 2], vertical_alignment="center")
                    col1.write(f"{q['text']}")
                    
                    with col2:
                        val = st.radio(
                            label=f"Chọn câu trả lời cho {q['code']}",
                            options=[1, 2, 3, 4, 5],
                            index=None,
                            key=key,
                            horizontal=True,
                            label_visibility="collapsed"
                        )
                    user_answers[q['code']] = val
                    st.divider()
                
        submit_btn = st.form_submit_button("🚀 Gửi Khảo Sát & Phân Tích Kết Quả", type="primary", use_container_width=True)

    # Xử lý kết quả dự đoán
    if submit_btn:
        # Chuẩn bị vector đặc trưng đúng theo thứ tự mô hình yêu cầu
        input_data = {}
        for feat in expected_features:
            if feat in user_answers:
                input_data[feat] = user_answers[feat]
            else:
                input_data[feat] = 3.0  # Giá trị trung lập nếu thiếu đặc trưng
                
        X_df = pd.DataFrame([input_data])
        
        try:
            # Thực hiện dự đoán với Random Forest
            raw_pred = rf_model.predict(X_df)
            raw_pred_df = pd.DataFrame(raw_pred, columns=['PAIS_01', 'PAIS_02', 'PAIS_03', 'PAIS_04', 'PAIS_05', 'PAIS_06', 'PAIS_07'])
            pred = np.round(raw_pred)
            pred_clamped = np.clip(pred, 1, 5)[0]  # Lấy mảng 1x7
            
            st.header("🎯 Kết quả dự đoán tác động tâm lý")
            
            # Chia thành các cột hiển thị đẹp mắt (sử dụng st.metric)
            cols_per_row = 4
            for i in range(0, n_outputs, cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    idx = i + j
                    if idx < n_outputs:
                        score = int(pred_clamped[idx])
                        # Lấy mã và mô tả từ answers.txt nếu có
                        if idx < len(answers_info):
                            ans_code = answers_info[idx]["code"]
                            ans_desc = answers_info[idx]["text"]
                        else:
                            ans_code = f"PAIS_{idx+1:02d}"
                            ans_desc = f"Chiều tác động thứ {idx+1}"
                            
                        with cols[j]:
                            # Sử dụng st.metric native thay vì HTML
                            st.metric(label=f"{ans_code}", value=f"Mức {score}/5")
                            st.caption(f"{ans_desc}")
                st.write("")

            # Khung chi tiết dữ liệu
            with st.expander("🔍 Chi tiết dữ liệu đầu vào và giá trị chưa làm tròn"):
                st.write("**Vector dữ liệu khảo sát:**")
                st.dataframe(X_df, use_container_width=True)
                
                st.write("**Giá trị dự đoán gốc từ mô hình:**")
                st.dataframe(raw_pred_df, use_container_width=True)
                
        except Exception as e:
            st.error(f"Lỗi trong quá trình tính toán dự đoán: {e}")

if __name__ == "__main__":
    main()
