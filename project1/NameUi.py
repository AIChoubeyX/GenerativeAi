import streamlit as st
from core import generate_movie_review_output, DEFAULT_POINTS_TO_COVER

# Page Config
st.set_page_config(
    page_title="Movie Review Chat",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 Movie Information Extraction Assistant")
st.markdown("---")

# Sidebar for Settings
with st.sidebar:
    st.header("⚙️ Settings")
    custom_points = st.checkbox("Customize points?", value=False)
    
    if custom_points:
        st.subheader("Edit Points to Cover:")
        points_input = st.text_area(
            "Enter points (one per line):",
            value="\n".join(DEFAULT_POINTS_TO_COVER),
            height=150
        )
        points_list = [p.strip() for p in points_input.split("\n") if p.strip()]
    else:
        points_list = DEFAULT_POINTS_TO_COVER

# Main Chat Interface
st.subheader("📝 Paste a Movie Paragraph")

movie_paragraph = st.text_area(
    "Movie paragraph:",
    placeholder="Paste any movie description here...",
    height=150,
    key="movie_input"
)

# Button to Process
col1, col2, col3 = st.columns(3)

with col1:
    submit_button = st.button("🔍 Extract Information", key="submit", use_container_width=True)

with col2:
    clear_button = st.button("🗑️ Clear", key="clear", use_container_width=True)

with col3:
    st.write("")  # Placeholder for alignment

if clear_button:
    st.rerun()

# Process and Display Results
if submit_button:
    if not movie_paragraph.strip():
        st.error("❌ Please enter a movie paragraph!")
    else:
        st.markdown("---")
        st.subheader("📊 Results")
        
        with st.spinner("Processing... 🤖"):
            try:
                result = generate_movie_review_output(movie_paragraph, points_list)
                
                # Display output in an organized way
                st.success("✅ Extraction Complete!")
                
                # Output Container
                output_container = st.container(border=True)
                with output_container:
                    st.markdown("### Movie Information & Summary")
                    st.markdown(result)
                
                # Copy to clipboard button
                st.download_button(
                    label="📥 Download Result as Text",
                    data=result,
                    file_name="movie_review.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    """
    **How to use:**
    1. Paste a movie paragraph in the text area
    2. (Optional) Customize points in sidebar
    3. Click "Extract Information"
    4. View structured output
    
    **Purpose:** Extracts movie details and generates a clean summary
    """
)
