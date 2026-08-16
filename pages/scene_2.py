import streamlit as st
from utils import scene_page_setup, reset_session_state
from ui import render_text, render_user_text

data, DELAY = scene_page_setup("scene_2")

render_text(data['greet'])

if st.session_state.s2_path is None:
    if st.button(data['problem']['a']['request'], use_container_width=True):
        st.session_state.s2_path = 'a'
        st.rerun()
    if st.button(data['problem']['b']['request'], use_container_width=True):
        st.session_state.s2_path = 'b'
        st.rerun()
    if st.button(data['problem']['c']['request'], use_container_width=True):
        st.session_state.s2_path = 'c'
        st.rerun()

if st.session_state.s2_path is not None:
    path = st.session_state.s2_path
    problem_data = data['problem'][path]
    
    render_user_text(problem_data['request'])
    
    render_text(problem_data['response'], delay=DELAY, key=f's2_path_{path}_res')
    
    render_text(problem_data['exercise']['1']['response'], delay=DELAY, key=f's2_path_{path}_ex1_prompt')
    
    if st.session_state.s2_ex1 is None:
        if st.button(problem_data['exercise']['1']['answer_1'], use_container_width=True):
            st.session_state.s2_ex1 = '1'
            st.rerun()
        if st.button(problem_data['exercise']['1']['answer_2'], use_container_width=True):
            st.session_state.s2_ex1 = '2'
            st.rerun()
        if st.button(problem_data['exercise']['1']['answer_3'], use_container_width=True):
            st.session_state.s2_ex1 = '3'
            st.rerun()
            
    if st.session_state.s2_ex1 is not None:
        choice = st.session_state.s2_ex1
        
        render_user_text(problem_data['exercise']['1'][f'answer_{choice}'])
        
        render_text(problem_data['exercise']['2']['response'], delay=DELAY, key=f's2_ex2_{choice}_res')
        render_text(problem_data['exercise']['2'][f'answer_{choice}'], delay=DELAY, key=f's2_ex2_{choice}_ans')
        
        if not st.session_state.s2_ex2_done:
            if st.button("Tiếp tục", use_container_width=True):
                st.session_state.s2_ex2_done = True
                st.rerun()
                
        if st.session_state.s2_ex2_done:
            ex3_resp = problem_data['exercise']['3']['response']
            if ex3_resp and ex3_resp.strip() != "CHƯA CÓ KỊCH BẢN":
                render_text(ex3_resp, delay=DELAY, key=f's2_ex3_{choice}_res')
                
            render_text(problem_data['exercise']['3'][f'answer_{choice}'], delay=DELAY, key=f's2_ex3_{choice}_ans')

            if st.button("Quay lại Trang chủ", use_container_width=True, key=f's2_home_{choice}'):
                reset_session_state()
                st.switch_page("app.py")
