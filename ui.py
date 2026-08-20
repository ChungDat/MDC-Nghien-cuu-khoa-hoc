"""
ui.py — Tiện ích giao diện Streamlit: chèn CSS và hiển thị bóng chat.
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
/* Hỗ trợ chế độ sáng (light mode) */
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
    Triển khai chia sẻ để hiển thị bóng chat có hiệu ứng hoạt ảnh.

    Tham số:
        text: Nội dung HTML/markdown hiển thị trong bóng chat.
        extra_class: Lớp CSS bổ sung (ví dụ: 'chat-bubble-user').
        delay: Thời gian chờ hoạt ảnh tính bằng giây; chỉ áp dụng lần đầu tiên key xuất hiện.
        key: Khóa session-state duy nhất đảm bảo hoạt ảnh chỉ chạy một lần.
    """
    anim_delay = 0.0
    if delay > 0 and key:
        if key not in st.session_state:
            st.session_state[key] = True
            anim_delay = delay

    # Bubble có key (bot): chỉ thêm fade-in khi xuất hiện lần đầu (anim_delay > 0)
    #   → tránh replay animation khi Streamlit rerun
    # Bubble không có key (user): luôn thêm fade-in vì chúng chỉ xuất hiện sau hành động người dùng
    if key is None:
        should_animate = True
        anim_delay = delay  # giữ nguyên delay được truyền vào (thường = 0)
    else:
        should_animate = anim_delay > 0

    style = f"animation-delay: {anim_delay}s;" if anim_delay > 0 else ""
    fade_class = "fade-in " if should_animate else ""
    classes = f"{fade_class}chat-bubble {extra_class}".strip()
    st.markdown(
        f'<div class="chat-container"><div class="{classes}" style="{style}">{text}</div></div>',
        unsafe_allow_html=True,
    )


def render_text(text: str, delay: float = 0, key: str | None = None):
    """Hiển thị bóng chat của bot/người dẫn truyện."""
    _render_bubble(text, extra_class="", delay=delay, key=key)


def render_user_text(text: str, delay: float = 0, key: str | None = None):
    """Hiển thị bóng chat phía người dùng (căn phải, màu xanh)."""
    _render_bubble(text, extra_class="chat-bubble-user", delay=delay, key=key)
