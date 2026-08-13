import streamlit as st
from utils import load_data, inject_custom_css, render_text, render_user_text

config = load_data("config.json")

st.set_page_config(page_title=config["display"]["scene_3_title"], layout="centered")

data = load_data(config["script"]["scene_3"])
DELAY = config["display"]["delay"]

inject_custom_css()

if 's3_a_done' not in st.session_state:
    st.session_state.s3_a_done = None
if 's3_b_done' not in st.session_state:
    st.session_state.s3_b_done = None

render_text(data['greet'])

problem_data = data['problem']

render_text(problem_data['a']['response'], delay=DELAY, key="s3_a_res")

if st.session_state.s3_a_done is None:
    if st.button(problem_data['a']['answer_1'], use_container_width=True):
        st.session_state.s3_a_done = '1'
        st.rerun()
    if st.button(problem_data['a']['answer_2'], use_container_width=True):
        st.session_state.s3_a_done = '2'
        st.rerun()

if st.session_state.s3_a_done is not None:
    choice_a = st.session_state.s3_a_done
    render_user_text(problem_data['a'][f'answer_{choice_a}'])
    
    render_text(problem_data['b']['response'], delay=DELAY, key="s3_b_res")
    
    if st.session_state.s3_b_done is None:
        if st.button(problem_data['b']['answer_1'], use_container_width=True):
            st.session_state.s3_b_done = '1'
            st.rerun()
        if st.button(problem_data['b']['answer_2'], use_container_width=True):
            st.session_state.s3_b_done = '2'
            st.rerun()
            
    if st.session_state.s3_b_done is not None:
        choice_b = st.session_state.s3_b_done
        render_user_text(problem_data['b'][f'answer_{choice_b}'])
        
        render_text(problem_data['b'][f'response_{choice_b}'], delay=DELAY, key=f"s3_b_res_{choice_b}")

        if st.button("Quay lại Trang chủ", use_container_width=True, key=f's3_home_{choice_b}'):
            st.switch_page("app.py")

