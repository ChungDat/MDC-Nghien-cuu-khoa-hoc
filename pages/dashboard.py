import streamlit as st
import pandas as pd
import altair as alt
from db.queries import get_all
from utils import load_data, create_sidebar, init_session_state

config = load_data("config.json")

st.set_page_config(page_title=config["display"]["dashboard_title"], layout="wide")
create_sidebar()
init_session_state()


@st.cache_data(ttl=60)
def load_dashboard_data():
    raw_data = get_all()
    if not raw_data:
        return pd.DataFrame(), pd.DataFrame()

    forms_list = []
    predictions_list = []

    for item in raw_data:
        pred = item.pop("predictions")
        forms_list.append(item)
        predictions_list.append(pred)

    df_forms = pd.DataFrame(forms_list)
    df_preds = pd.DataFrame(predictions_list)
    return df_forms, df_preds


def main():
    if not st.session_state["authenticated"]:
        with st.form("auth_form"):
            password = st.text_input("Nhập mật khẩu quản trị", type="password")
            if st.form_submit_button("Đăng nhập"):
                if password == st.secrets["admin"]["ADMIN_PASSWORD"]:
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("Mật khẩu không chính xác.")
        st.stop()

    st.title(config["display"]["dashboard_title"])

    df_forms, df_preds = load_dashboard_data()

    if df_forms.empty:
        st.warning("Chưa có dữ liệu khảo sát nào trong hệ thống.")
        st.stop()

    st.divider()

    st.header(f"Tổng số lượt khảo sát: {len(df_forms)}")

    form_cols = [c for c in df_forms.columns if c not in ["id", "created_at"]]

    st.divider()

    st.header("Điểm tác động trung bình")

    NON_SCORE_COLS = {"form_id", "model", "created_at"}
    pred_cols = []
    if not df_preds.empty:
        pred_cols = [c for c in df_preds.columns if c not in NON_SCORE_COLS]
        if pred_cols:
            score_cols = st.columns(len(pred_cols))
            for i, p_col in enumerate(pred_cols):
                with score_cols[i]:
                    st.metric(p_col.upper(), f"{df_preds[p_col].mean():.2f}")
        else:
            st.info("Không tìm thấy cột dự đoán.")

        if "model" in df_preds.columns:
            st.divider()
            st.subheader("Phân bố mô hình sử dụng")
            model_counts = df_preds["model"].value_counts().reset_index()
            model_counts.columns = ["Mô hình", "Số lượng"]
            st.dataframe(model_counts, use_container_width=True)
    else:
        st.info("Chưa có dữ liệu dự đoán.")

    st.divider()

    st.header("Điểm trung bình theo từng câu hỏi")
    if form_cols:
        avg_answers = df_forms[form_cols].mean().reset_index()
        avg_answers.columns = ["Câu hỏi", "Điểm trung bình"]

        chart = alt.Chart(avg_answers).mark_bar().encode(
            x=alt.X("Điểm trung bình:Q", scale=alt.Scale(domain=[0, 5])),
            y=alt.Y("Câu hỏi:N", sort="-x"),
        )
        st.altair_chart(chart, use_container_width=True)

    st.divider()

    st.header("Phân bố câu trả lời theo từng câu hỏi")
    if form_cols:
        tabs = st.tabs(form_cols)
        for tab, col in zip(tabs, form_cols):
            with tab:
                counts = (
                    df_forms[col]
                    .value_counts()
                    .reindex([1, 2, 3, 4, 5], fill_value=0)
                    .reset_index()
                )
                counts.columns = ["Mức điểm", "Số lượng"]

                chart = alt.Chart(counts).mark_bar().encode(
                    x=alt.X("Mức điểm:O", axis=alt.Axis(labelAngle=0)),
                    y=alt.Y("Số lượng:Q"),
                )
                st.altair_chart(chart, use_container_width=True)

    st.divider()

    st.header("Dữ liệu chi tiết")
    tab1, tab2 = st.tabs(["Dữ liệu khảo sát", "Dữ liệu dự đoán"])

    with tab1:
        st.dataframe(df_forms, use_container_width=True)

    with tab2:
        st.dataframe(df_preds, use_container_width=True)


main()
