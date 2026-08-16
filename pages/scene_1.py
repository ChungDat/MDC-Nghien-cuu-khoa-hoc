import streamlit as st
from utils import scene_page_setup, reset_session_state
from ui import render_text, render_user_text

data, DELAY = scene_page_setup("scene_1")

render_text(data['greet'])

if st.session_state.s1_path is None:
    col1, col2 = st.columns(2)
    with col1:
        if st.button(data['problem']['a']['request'], use_container_width=True):
            st.session_state.s1_path = 'a'
            st.rerun()
    with col2:
        if st.button(data['problem']['b']['request'], use_container_width=True):
            st.session_state.s1_path = 'b'
            st.rerun()

if st.session_state.s1_path == 'b':
    render_user_text(data['problem']['b']['request'])
    render_text(data['problem']['b']['response'], delay=DELAY, key='s1_b_res')

    if st.button("Quay lại Trang chủ", use_container_width=True, key="s1_home_b"):
        reset_session_state()
        st.switch_page("app.py")

if st.session_state.s1_path == 'a':
    render_user_text(data['problem']['a']['request'])
    render_text(data['problem']['a']['response'], delay=DELAY, key='s1_a_res')
    
    if st.session_state.s1_ex1 is None:
        col1, col2 = st.columns(2)
        with col1:
            if st.button(data['problem']['a']['exercise']['1']['answer_1'], use_container_width=True):
                st.session_state.s1_ex1 = '1'
                st.rerun()
        with col2:
            if st.button(data['problem']['a']['exercise']['1']['answer_2'], use_container_width=True):
                st.session_state.s1_ex1 = '2'
                st.rerun()

    if st.session_state.s1_ex1 is not None:
        choice_1 = st.session_state.s1_ex1
        render_user_text(data['problem']['a']['exercise']['1'][f'answer_{choice_1}'])
        
        if choice_1 == '1':
            render_text(data['problem']['a']['exercise']['1']['response_1'], delay=DELAY, key='s1_ex1_res1')
        else:
            render_text(data['problem']['a']['exercise']['1']['response_2'], delay=DELAY, key='s1_ex1_res2')
            
        render_text(data['problem']['a']['exercise']['2']['response'], delay=DELAY, key='s1_ex2_prompt')
        
        if st.session_state.s1_ex2 is None:
            col1, col2 = st.columns(2)
            with col1:
                if st.button(data['problem']['a']['exercise']['2']['answer_1'], use_container_width=True):
                    st.session_state.s1_ex2 = '1'
                    st.rerun()
            with col2:
                if st.button(data['problem']['a']['exercise']['2']['answer_2'], use_container_width=True):
                    st.session_state.s1_ex2 = '2'
                    st.rerun()
                    
        if st.session_state.s1_ex2 is not None:
            choice_2 = st.session_state.s1_ex2
            render_user_text(data['problem']['a']['exercise']['2'][f'answer_{choice_2}'])
            
            if choice_2 == '1':
                render_text(data['problem']['a']['exercise']['2']['response_1'], delay=DELAY, key='s1_ex2_res1')
            else:
                render_text(data['problem']['a']['exercise']['2']['response_2'], delay=DELAY, key='s1_ex2_res2')

            if st.button("Quay lại Trang chủ", use_container_width=True, key="s1_home_a"):
                reset_session_state()
                st.switch_page("app.py")
