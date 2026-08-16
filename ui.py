"""
ui.py — Streamlit UI utilities: CSS injection and chat bubble renderers.
"""
import streamlit as st


def inject_custom_css():
    st.markdown("""
<style>
@keyframes floatUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
.fade-in {
    animation: floatUp 0.8s ease-out both;
}
.chat-container {
    display: flex;
    flex-direction: column;
    width: 100%;
}
.chat-bubble {
    background-color: #2b2b2b;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 15px;
    color: #ffffff;
    font-size: 16px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    max-width: 85%;
    align-self: flex-start;
    white-space: pre-wrap;
}
.chat-bubble-user {
    background-color: #007bff;
    color: white;
    align-self: flex-end;
}
/* Light mode support */
@media (prefers-color-scheme: light) {
    .chat-bubble {
        background-color: #f1f1f1;
        color: #333333;
    }
    .chat-bubble-user {
        background-color: #007bff;
        color: white;
    }
}
</style>
""", unsafe_allow_html=True)


def _render_bubble(text: str, extra_class: str = "", delay: float = 0, key: str | None = None):
    """
    Shared implementation for rendering an animated chat bubble.

    Parameters:
        text: HTML/markdown content to display inside the bubble.
        extra_class: Additional CSS class(es) to append (e.g. 'chat-bubble-user').
        delay: Animation delay in seconds; only applied the first time this key is seen.
        key: Unique session-state key used to ensure the animation fires only once.
    """
    anim_delay = 0.0
    if delay > 0 and key:
        if key not in st.session_state:
            st.session_state[key] = True
            anim_delay = delay

    style = f"animation-delay: {anim_delay}s;" if anim_delay > 0 else ""
    classes = f"fade-in chat-bubble {extra_class}".strip()
    st.markdown(
        f'<div class="chat-container"><div class="{classes}" style="{style}">{text}</div></div>',
        unsafe_allow_html=True,
    )

    if anim_delay > 0:
        st.markdown(f"""
        <style>
        div.stButton {{
            animation: floatUp 0.8s ease-out both !important;
            animation-delay: {anim_delay}s !important;
        }}
        </style>
        """, unsafe_allow_html=True)


def render_text(text: str, delay: float = 0, key: str | None = None):
    """Render a bot/narrator chat bubble."""
    _render_bubble(text, extra_class="", delay=delay, key=key)


def render_user_text(text: str, delay: float = 0, key: str | None = None):
    """Render a user-side chat bubble (right-aligned, blue)."""
    _render_bubble(text, extra_class="chat-bubble-user", delay=delay, key=key)
