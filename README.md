# 📚 Manwha Scraper - Educational Purpose Only

> **⚠️ DISCLAIMER**: This tool is provided **ONLY FOR EDUCATIONAL PURPOSES** to demonstrate web scraping concepts and techniques. Users are solely responsible for how they use this tool.

---

## 🚫 WHAT NOT TO DO WITH THIS SCRIPT

### **DO NOT:**

1. **❌ Violate Copyright Laws**
   - Do NOT use this to download copyrighted manwha and redistribute them
   - Do NOT bypass paywalls or access paid content without permission
   - Do NOT use downloaded content for commercial purposes

2. **❌ Violate Website Terms of Service**
   - Most manwha websites explicitly forbid scraping in their ToS
   - Do NOT scrape if the website says "no automated access"
   - Do NOT ignore robots.txt files

3. **❌ Overload Servers**
   - Do NOT remove or reduce the delays between requests
   - Do NOT run multiple instances of this scraper simultaneously
   - Do NOT scrape during peak hours to avoid affecting service availability
   - Always include respectful delays (the script already has `time.sleep()`)

4. **❌ Distribute Scraped Content**
   - Do NOT upload downloaded manwha to other websites
   - Do NOT share the scraped content publicly
   - Do NOT create mirrors of copyrighted content

5. **❌ Remove Attribution**
   - Do NOT remove creator/author information
   - Always respect the original creators' rights
   - Keep metadata intact

6. **❌ Bypass Security or Protection**
   - Do NOT attempt to crack CAPTCHAs
   - Do NOT bypass login systems to access restricted content
   - Do NOT circumvent DRM or other protective measures

---

## ✅ ACCEPTABLE USES

This tool is intended for:

- **Learning web scraping techniques** - Understanding BeautifulSoup and requests
- **Studying HTML/CSS selectors** - Learning how to parse web content
- **Personal use with permission** - Downloading content you have rights to
- **Testing on your own websites** - Scraping your own HTML files
- **Educational demonstrations** - Teaching programming concepts

### Valid Examples:

- ✅ Scraping a free, public domain manwha with permission
- ✅ Downloading chapters from a website that allows it
- ✅ Learning how web scraping works on test websites
- ✅ Scraping your own content for archival purposes

---

## 📋 Legal Considerations

- **Copyright Notice**: Most manwha are protected by copyright. Always check the copyright status.
- **Terms of Service**: Many websites prohibit automated access. Reading the ToS is YOUR responsibility.
- **Local Laws**: Web scraping legality varies by jurisdiction. Check your local laws.
- **Fair Use**: This is NOT protected by fair use in most jurisdictions for bulk downloading.

> **The authors of this tool are NOT responsible for how you use it. You use it at your own risk.**

---

## 🛠️ Installation & Setup

### Requirements

- Python 3.7+
- pip (Python package manager)

### Installation Steps

1. **Clone or download this repository**

   ```bash
   git clone <repository-url>
   cd manwha-scraper
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   - Navigate to `http://localhost:8501`

---

## 📁 Project Structure

```

manwha-scraper/
├── app.py                    # Main Streamlit application
├── src/
│   └── scraper.py           # Scraper class and logic
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── manwha_collection/      # Downloaded content (auto-created)
    └── Series_Name/
        ├── Chapter_001/
        │   ├── page_001.jpg
        │   ├── page_002.jpg
        │   └── ...
        ├── Chapter_002/
        └── metadata.json
```

---

## 🔧 How to Use

### Step 1: Customize CSS Selectors

The script uses CSS selectors to find chapters and images. These vary by website.

**To customize:**

1. Open the target manwha website in your browser
2. Right-click → "Inspect" (or press F12)
3. Find a chapter link or image element
4. Copy its selector (class name, id, tag, etc.)
5. Update the selectors in `src/scraper.py`:

```python
# Line in scrape_chapters()
chapter_links = soup.select('a[href*="chapter"]')  # ← Change this

# Line in scrape_chapter_images()
img_elements = soup.select('img[src]')  # ← And this
```

### Step 2: Run the GUI

```bash
streamlit run app.py
```

### Step 3: Fill in the Form

1. **Series Name**: Enter the series name (e.g., "Solo_Leveling")
2. **Base URL**: Paste the URL to the series (e.g., "https://webtoon.com/series/...")
3. **Chapters**:
   - **Range**: Download chapters 1-50
   - **Specific**: Download only chapters 1, 5, 10
4. Click **"Begin Download"**

### Step 4: Wait for Completion

- The app will show progress in real-time
- Downloaded chapters appear in `manwha_collection/Series_Name/`

---

## 📊 Example Directory Structure After Download

```
manwha_collection/
└── Solo_Leveling/
    ├── Chapter_001/
    │   ├── page_001.jpg
    │   ├── page_002.jpg
    │   ├── page_003.jpg
    │   └── ...
    ├── Chapter_002/
    │   ├── page_001.jpg
    │   ├── page_002.jpg
    │   └── ...
    └── metadata.json
```

---

## 🐛 Troubleshooting

### "No chapters found"

- The CSS selectors are incorrect
- Use DevTools to inspect and update the selectors
- Check if the website structure changed

### "No images found for chapter X"

- Image selectors are incorrect
- The website may use JavaScript to load images dynamically
- Try updating the image selector

### "Connection timeout"

- The website may be blocking requests
- Check if the URL is correct
- Try again later (website may be temporarily down)

### "Permission denied" error

- You may not have write access to the directory
- Try running with administrator privileges
- Or save to a different directory

---

## 📝 Customization Guide

### Modifying Request Headers

If the website blocks requests, you can modify the User-Agent in `src/scraper.py`:

```python
self.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...'
}
```

### Adding Delays

To be more respectful to servers, increase delays in `src/scraper.py`:

```python
time.sleep(1)  # Change to time.sleep(2) or higher
```

### Changing Download Directory

Edit `app.py` to change the base directory:

```python
base_dir = "my_manwha_folder"  # Instead of "manwha_collection"
```

---

## 🔐 Privacy & Security

- **No Data Collection**: This tool does not collect or send your data anywhere
- **Local Storage**: All downloaded content is stored locally on your device
- **No Authentication**: The tool does not store passwords or credentials

---

## 📚 Educational Resources

Learn more about web scraping:

- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Library Guide](https://requests.readthedocs.io/)
- [CSS Selectors Tutorial](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors)
- [Web Scraping Ethical Guidelines](https://en.wikipedia.org/wiki/Web_scraping#Ethics)

---

## 📞 Support & Questions

If you encounter issues:

1. Check this README first
2. Review the error message carefully
3. Test CSS selectors with DevTools
4. Check if the website's structure changed

---

## 📄 License

This project is provided "AS IS" without any warranties. Users assume full responsibility for their use of this tool.

---

## ⚖️ Final Legal Notice

> **BY USING THIS TOOL, YOU AGREE THAT:**

> 1. You understand and accept all legal risks
> 2. You are responsible for complying with local laws
> 3. You will not use this for illegal purposes
> 4. You will respect copyright and website ToS
> 5. The authors are not liable for your actions

**This tool is strictly for educational purposes only. Use it responsibly and ethically.**
