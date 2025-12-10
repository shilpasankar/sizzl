import streamlit as st

st.set_page_config(
    page_title="SizzlClub · Community",
    page_icon="💬",
    layout="wide"
)

# -------------- STYLES --------------
st.markdown(
    """
    <style>
    .sizzl-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF4D6D, #FF8E6E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .sizzl-subtitle {
        font-size: 1rem;
        color: #f5f5f5cc;
        margin-bottom: 1rem;
    }
    .coming-card {
        padding: 1.2rem 1.3rem;
        border-radius: 0.9rem;
        background-color: #121218;
        border: 1px dashed #ff4d6d66;
    }
    .roadmap-bullet {
        margin-bottom: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------- HEADER --------------
st.markdown('<div class="sizzl-title">💬 SizzlClub · Community</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sizzl-subtitle">A space for screaming about tropes, dropping recs, and gently judging fictional men.</div>',
    unsafe_allow_html=True
)

st.markdown("---")

col_left, col_right = st.columns([2, 1], gap="large")

with col_left:
    st.markdown("### Coming soon ✨")
    st.markdown(
        """
        This will become the heart of SizzlClub — a low-pressure, cozy space to:
        
        - Start discussion threads about specific books  
        - Ask for recs based on vibes / tropes / spice levels  
        - Share “I can’t believe they did THAT” moments  
        - Build little sub-communities (dark romance, fantasy, contemporary, etc.)
        """
    )

    st.markdown("")
    st.markdown("### Planned features")
    st.markdown(
        """
        - 🧵 **Threads** — topic-based discussions with simple comment chains  
        - ❤️ **Book-linked posts** — create a thread directly from a Book Finder result  
        - 🗳️ **Vibe polls** — “How spicy was this actually?”  
        - 🌶️ **Spice meters** — community-voted spice levels for each title  
        """
    )

    st.markdown("")
    st.info(
        "Right now this page is a placeholder while the backend is being figured out. "
        "You can still use **Book Finder** to discover books and imagine the chaos that will land here soon."
    )

with col_right:
    st.markdown("### What you can do *today* on SizzlClub")
    st.write(
        "- Use **Book Finder** to discover books you haven’t seen before.\n"
        "- Keep a little note of titles you want to scream about.\n"
        "- Think about what kind of community you’d personally enjoy: cozy book club? chaotic meme zone? serious trope analysis?"
    )

    st.markdown("### Want to help shape this?")
    st.write(
        "You could add a tiny feedback form later, or just keep this as a personal playground. "
        "For now, this page simply says: more is coming. 💖"
    )

st.markdown("---")
st.caption("SizzlClub Community · work in progress, but the vibes are already here.")
