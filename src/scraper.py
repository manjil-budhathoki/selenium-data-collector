import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import json
import streamlit as st


class ManwhaScraper:
    """
    A web scraper for downloading manwha chapters for offline reading.
    
    This class handles:
    - Scraping chapter lists from manwha websites
    - Extracting image URLs from chapters
    - Downloading and organizing images locally
    - Creating metadata files
    
    ⚠️ EDUCATIONAL PURPOSE ONLY
    See README.md for usage guidelines and legal disclaimers.
    """
    
    def __init__(self, base_series_name, base_dir="manwha_collection"):
        """
        Initialize the scraper.
        
        Args:
            base_series_name (str): Name of the series (used for folder)
            base_dir (str): Base directory for storing downloaded content
        """
        self.base_dir = base_dir
        self.series_name = base_series_name
        self.series_dir = os.path.join(base_dir, base_series_name)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self._setup_directories()
    
    def _setup_directories(self):
        """Create directory structure for storing series"""
        os.makedirs(self.series_dir, exist_ok=True)
    
    def scrape_chapters(self, base_url):
        """
        Scrape chapter list from the series page.
        
        ⚠️ IMPORTANT: You need to customize the CSS selectors based on the target website.
        Use browser DevTools (F12) to inspect the HTML and find the correct selectors.
        
        Args:
            base_url (str): URL of the manwha series main page
            
        Returns:
            list: List of dictionaries with 'name' and 'url' keys
        """
        try:
            response = requests.get(base_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # ============================================
            # CUSTOMIZE THESE SELECTORS FOR YOUR TARGET SITE
            # ============================================
            # Example selectors (adjust based on actual website):
            # soup.select('a[href*="chapter"]')
            # soup.select('.chapter-link')
            # soup.select('div.chapter > a')
            # Open DevTools (F12), inspect chapter links, and update below
            
            chapters = []
            chapter_links = soup.select('a[href*="chapter"]')  # ← CUSTOMIZE THIS
            
            for link in chapter_links:
                chapter_url = urljoin(base_url, link.get('href'))
                chapter_name = link.get_text(strip=True)
                chapters.append({
                    'name': chapter_name,
                    'url': chapter_url
                })
            
            return chapters
        
        except Exception as e:
            st.error(f"Error scraping chapters: {e}")
            return []
    
    def scrape_chapter_images(self, chapter_url, chapter_num):
        """
        Scrape all image URLs from a specific chapter.
        
        ⚠️ IMPORTANT: You need to customize the CSS selectors based on the target website.
        
        Args:
            chapter_url (str): URL of the specific chapter
            chapter_num (int): Chapter number (for reference)
            
        Returns:
            list: List of image URLs
        """
        try:
            response = requests.get(chapter_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # ============================================
            # CUSTOMIZE THIS SELECTOR FOR YOUR TARGET SITE
            # ============================================
            # Example selectors:
            # soup.select('img[src]')
            # soup.select('img.chapter-image')
            # soup.select('div.reader img')
            # Open DevTools, inspect images, and update below
            
            images = []
            img_elements = soup.select('img[src]')  # ← CUSTOMIZE THIS
            
            for img in img_elements:
                img_url = img.get('src')
                if img_url and ('http' in img_url or img_url.startswith('/')):
                    img_url = urljoin(chapter_url, img_url)
                    images.append(img_url)
            
            return images
        
        except Exception as e:
            st.error(f"Error scraping chapter images: {e}")
            return []
    
    def download_image(self, img_url, save_path, progress_placeholder):
        """
        Download a single image from a URL.
        
        Args:
            img_url (str): URL of the image
            save_path (str): Local path to save the image
            progress_placeholder: Streamlit placeholder for progress updates
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            response = requests.get(img_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            return True
        except Exception as e:
            progress_placeholder.warning(f"Error downloading image: {e}")
            return False
    
    def download_chapter(self, chapter_url, chapter_num, chapter_name, progress_placeholder):
        """
        Download all images for a specific chapter.
        
        Args:
            chapter_url (str): URL of the chapter
            chapter_num (int): Chapter number
            chapter_name (str): Name of the chapter
            progress_placeholder: Streamlit placeholder for updates
            
        Returns:
            int: Number of successfully downloaded pages
        """
        chapter_dir = os.path.join(self.series_dir, f"Chapter_{chapter_num:03d}")
        os.makedirs(chapter_dir, exist_ok=True)
        
        progress_placeholder.info(f"Scraping Chapter {chapter_num}: {chapter_name}...")
        images = self.scrape_chapter_images(chapter_url, chapter_num)
        
        if not images:
            progress_placeholder.warning(f"No images found for chapter {chapter_num}")
            return 0
        
        downloaded = 0
        for page_num, img_url in enumerate(images, 1):
            filename = f"page_{page_num:03d}.jpg"
            filepath = os.path.join(chapter_dir, filename)
            
            # Skip if already downloaded
            if os.path.exists(filepath):
                progress_placeholder.info(f"  Page {page_num} already exists, skipping...")
                downloaded += 1
                continue
            
            if self.download_image(img_url, filepath, progress_placeholder):
                progress_placeholder.info(f"  Downloaded page {page_num}/{len(images)}")
                downloaded += 1
                time.sleep(0.5)  # Be respectful to the server
            else:
                progress_placeholder.warning(f"  Failed to download page {page_num}")
        
        return downloaded
    
    def scrape_all(self, base_url, chapters_to_download, progress_placeholder):
        """
        Download all specified chapters.
        
        Args:
            base_url (str): URL of the series main page
            chapters_to_download (list): List of chapter numbers to download
            progress_placeholder: Streamlit placeholder for progress updates
        """
        all_chapters = self.scrape_chapters(base_url)
        
        if not all_chapters:
            st.error("No chapters found!")
            return
        
        progress_placeholder.info(f"Found {len(all_chapters)} chapters total")
        
        for chapter_num in chapters_to_download:
            if chapter_num <= len(all_chapters):
                chapter = all_chapters[chapter_num - 1]
                self.download_chapter(
                    chapter['url'],
                    chapter_num,
                    chapter['name'],
                    progress_placeholder
                )
                time.sleep(1)  # Delay between chapters
            else:
                progress_placeholder.warning(
                    f"Chapter {chapter_num} not found (only {len(all_chapters)} chapters available)"
                )
        
        self.create_metadata(all_chapters)
        progress_placeholder.success("✅ Scraping complete!")
    
    def create_metadata(self, chapters):
        """
        Save chapter metadata to a JSON file.
        
        Args:
            chapters (list): List of chapter dictionaries
        """
        metadata = {
            'series': self.series_name,
            'total_chapters': len(chapters),
            'chapters': chapters
        }
        metadata_path = os.path.join(self.series_dir, 'metadata.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)