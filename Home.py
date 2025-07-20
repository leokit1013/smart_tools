import streamlit as st

st.set_page_config(page_title="Smart Career Tools", layout="wide")

st.markdown(
    """
    <style>
        .title {
            font-size: 3em;
            text-align: center;
            font-weight: bold;
            margin-bottom: 0;
        }
        .subtitle {
            text-align: center;
            font-size: 1.3em;
            color: #555;
        }
        .tool-card {
            background-color: #f8f9fa;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            transition: transform 0.2s ease-in-out;
        }
        .tool-card:hover {
            transform: scale(1.03);
            box-shadow: 0 6px 16px rgba(0,0,0,0.08);
        }
        .tool-title {
            font-size: 1.2em;
            font-weight: 600;
            margin-top: 15px;
        }
        .tool-desc {
            font-size: 0.95em;
            color: #555;
            margin-bottom: 15px;
        }
        .tool-button {
            background-color: #ff4b4b;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 0.95em;
            cursor: pointer;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='title'>🚀 Welcome to Smart Career Tools</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Your personalized suite for career growth and productivity</div>", unsafe_allow_html=True)

st.write("")  # spacing

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div style='text-align: center; font-size: 50px;'>📝</div>", unsafe_allow_html=True)
    st.markdown("<div class='tool-title'>Resume Builder & Enhancer</div>", unsafe_allow_html=True)
    st.markdown("<div class='tool-desc'>Craft professional resumes that stand out using AI-enhanced insights.</div>", unsafe_allow_html=True)
    st.page_link("pages/1_Resume_Builder_Enhancer.py", label="Open Tool", icon="➡️")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div style='text-align: center; font-size: 50px;'>📊</div>", unsafe_allow_html=True)
    st.markdown("<div class='tool-title'>Dashboard Generator</div>", unsafe_allow_html=True)
    st.markdown("<div class='tool-desc'>Visualize your data effortlessly using customizable dashboards.</div>", unsafe_allow_html=True)
    st.page_link("pages/2_Dashboard_Generator.py", label="Open Tool", icon="➡️")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div style='text-align: center; font-size: 50px;'>📄</div>", unsafe_allow_html=True)
    st.markdown("<div class='tool-title'>Document Summarizer</div>", unsafe_allow_html=True)
    st.markdown("<div class='tool-desc'>Summarize reports, resumes, or articles quickly with Gemini AI.</div>", unsafe_allow_html=True)
    st.page_link("pages/3_Document_Summarizer.py", label="Open Tool", icon="➡️")
    st.markdown("</div>", unsafe_allow_html=True)



st.markdown("""
<style>
#about-button {
    position: fixed;
    bottom: 20px;
    left: 20px;
    background-color: #ff4b4b;
    color: white;
    border: none;
    border-radius: 25px;
    padding: 10px 20px;
    font-size: 14px;
    cursor: pointer;
    z-index: 1000;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    text-decoration: none;
}
</style>

<a id="about-button" href="/About" target="_self">ℹ️ About</a>
""", unsafe_allow_html=True)

