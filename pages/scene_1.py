import streamlit as st
from utils import load_data, inject_custom_css, render_text, render_user_text

st.set_page_config(page_title="Scene 1", layout="centered")

config = load_data("config.json")
data = load_data(config['script']['scene_1'])
inject_custom_css()

if 's1_path' not in st.session_state:
    st.session_state.s1_path = None
if 's1_ex1' not in st.session_state:
    st.session_state.s1_ex1 = None
if 's1_ex2' not in st.session_state:
    st.session_state.s1_ex2 = None

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
    render_text(data['problem']['b']['response'], delay=0.8, key='s1_b_res')

if st.session_state.s1_path == 'a':
    render_user_text(data['problem']['a']['request'])
    render_text(data['problem']['a']['response'], delay=0.8, key='s1_a_res')
    
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
            render_text(data['problem']['a']['exercise']['1']['response_1'], delay=0.8, key='s1_ex1_res1')
        else:
            render_text(data['problem']['a']['exercise']['1']['response_2'], delay=0.8, key='s1_ex1_res2')
            
        render_text(data['problem']['a']['exercise']['2']['response'], delay=0.8, key='s1_ex2_prompt')
        
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
                render_text(data['problem']['a']['exercise']['2']['response_1'], delay=0.8, key='s1_ex2_res1')
            else:
                render_text(data['problem']['a']['exercise']['2']['response_2'], delay=0.8, key='s1_ex2_res2')
