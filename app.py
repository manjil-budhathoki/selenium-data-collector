import streamlit as st
import os
import time
from src.scraper import ManwhaScraper

st.set_page_config(page_title="Manwha Scraper", layout="wide")

# ==================== STREAMLIT GUI ====================

st.title("🖼️ Manwha Scraper")
st.markdown("Download and organize manwha chapters for offline reading")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    series_name = st.text_input(
        "Series Name",
        placeholder="e.g., Solo_Leveling",
        help="Folder name for storing the series"
    )
    
    base_url = st.text_input(
        "Base URL",
        placeholder="https://example.com/series/my-series",
        help="URL of the manwha series main page"
    )
    
    st.divider()
    st.subheader("📚 Chapter Selection")
    
    chapter_mode = st.radio(
        "Select chapters:",
        ["Range (Chapter A to B)", "Specific Chapters"]
    )
    
    if chapter_mode == "Range (Chapter A to B)":
        col1, col2 = st.columns(2)
        with col1:
            start_chapter = st.number_input(
                "From Chapter",
                min_value=1,
                value=1
            )
        with col2:
            end_chapter = st.number_input(
                "To Chapter",
                min_value=1,
                value=10
            )
        
        chapters_to_download = list(range(start_chapter, end_chapter + 1))
    
    else:
        chapters_input = st.text_input(
            "Chapter Numbers",
            placeholder="1, 2, 5, 10",
            help="Comma-separated chapter numbers"
        )
        
        if chapters_input:
            try:
                chapters_to_download = [int(x.strip()) for x in chapters_input.split(',')]
            except ValueError:
                st.error("Invalid input! Use comma-separated numbers")
                chapters_to_download = []
        else:
            chapters_to_download = []
    
    st.divider()
    
    # Display configuration summary
    st.subheader("📋 Summary")
    if series_name:
        st.info(f"Series: **{series_name}**")
    if base_url:
        st.info(f"URL: `{base_url}`")
    if chapters_to_download:
        st.info(f"Chapters: **{chapters_to_download}**")


# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🚀 Start Scraping")
    
    # Validation
    if st.button("Begin Download", type="primary", use_container_width=True):
        if not series_name:
            st.error("❌ Please enter a Series Name")
        elif not base_url:
            st.error("❌ Please enter a Base URL")
        elif not chapters_to_download:
            st.error("❌ Please select chapters to download")
        else:
            progress_placeholder = st.empty()
            
            try:
                scraper = ManwhaScraper(series_name)
                progress_placeholder.info(f"Starting download for: **{series_name}**")
                scraper.scrape_all(base_url, chapters_to_download, progress_placeholder)
                
                # Show download location
                st.success(f"📁 Files saved to: `{scraper.series_dir}`")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")

with col2:
    st.subheader("ℹ️ Info")
    st.markdown("""
    **How to use:**
    1. Enter series name
    2. Paste series URL
    3. Select chapters
    4. Click download
    
    **Note:** You may need to customize CSS selectors for the target website.
    
    📖 See README.md for important information
    """)

st.divider()

# Display downloaded series
st.subheader("📚 Downloaded Series")

base_dir = "manwha_collection"
if os.path.exists(base_dir):
    series_list = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    
    if series_list:
        for series in series_list:
            series_path = os.path.join(base_dir, series)
            chapters = [d for d in os.listdir(series_path) if d.startswith("Chapter_")]
            
            with st.expander(f"📖 {series} ({len(chapters)} chapters)"):
                st.markdown(f"**Location:** `{series_path}`")
                
                if chapters:
                    # Count pages per chapter
                    chapter_info = []
                    for chapter in sorted(chapters):
                        chapter_path = os.path.join(series_path, chapter)
                        pages = [f for f in os.listdir(chapter_path) if f.endswith('.jpg')]
                        chapter_info.append(f"{chapter}: {len(pages)} pages")
                    
                    st.write("\n".join(chapter_info))
    else:
        st.info("No downloaded series yet. Start by entering details and clicking 'Begin Download'!")
else:
    st.info("No downloads yet. Create your first download to get started!")