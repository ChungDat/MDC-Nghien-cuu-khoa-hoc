import streamlit as st
from utils import load_data, inject_custom_css, render_text, render_user_text

config = load_data("config.json")

st.set_page_config(page_title=config["display"]["scene_2_title"], layout="centered")

data = load_data(config["script"]["scene_2"])
inject_custom_css()

DELAY = config["display"]["delay"]

# Initialize session state for tracking progress
if 's2_path' not in st.session_state:
    st.session_state.s2_path = None
if 's2_ex1' not in st.session_state:
    st.session_state.s2_ex1 = None
if 's2_ex2_done' not in st.session_state:
    st.session_state.s2_ex2_done = False

render_text(data['greet'])

# Stage 1: Choose main problem path (A, B, or C)
if st.session_state.s2_path is None:
    # Stacking vertically as the text can be somewhat long
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
    
    # Render user's choice
    render_user_text(problem_data['request'])
    
    # Render response to the chosen path
    render_text(problem_data['response'], delay=DELAY, key=f's2_path_{path}_res')
    
    # Render Exercise 1 prompt
    render_text(problem_data['exercise']['1']['response'], delay=DELAY, key=f's2_path_{path}_ex1_prompt')
    
    # Stage 2: Choose specific issue in Exercise 1
    if st.session_state.s2_ex1 is None:
        # These answers are quite long paragraphs, so stacking vertically is best
        if st.button(problem_data['exercise']['1']['answer_1'], use_container_width=True):
            st.session_state.s2_ex1 = '1'
            st.rerun()
        if st.button(problem_data['exercise']['1']['answer_2'], use_container_width=True):
            st.session_state.s2_ex1 = '2'
            st.rerun()
        if st.button(problem_data['exercise']['1']['answer_3'], use_container_width=True):
            st.session_state.s2_ex1 = '3'
            st.rerun()
            
    # Stage 3: Render corresponding advice from Exercise 2 and Exercise 3
    if st.session_state.s2_ex1 is not None:
        choice = st.session_state.s2_ex1
        
        # Render user's choice for Exercise 1
        render_user_text(problem_data['exercise']['1'][f'answer_{choice}'])
        
        # Exercise 2 logic
        render_text(problem_data['exercise']['2']['response'], delay=DELAY, key=f's2_ex2_{choice}_res')
        render_text(problem_data['exercise']['2'][f'answer_{choice}'], delay=DELAY, key=f's2_ex2_{choice}_ans')
        
        if not st.session_state.s2_ex2_done:
            if st.button("Tiếp tục", use_container_width=True):
                st.session_state.s2_ex2_done = True
                st.rerun()
                
        if st.session_state.s2_ex2_done:
            # Exercise 3 logic
            ex3_resp = problem_data['exercise']['3']['response']
            # Ignore rendering if it is explicitly marked as "CHƯA CÓ KỊCH BẢN"
            if ex3_resp and ex3_resp.strip() != "CHƯA CÓ KỊCH BẢN":
                render_text(ex3_resp, delay=DELAY, key=f's2_ex3_{choice}_res')
                
            render_text(problem_data['exercise']['3'][f'answer_{choice}'], delay=DELAY, key=f's2_ex3_{choice}_ans')
