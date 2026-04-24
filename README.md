# selenium-data-collector
 
A modular web data collection framework built on Selenium and BeautifulSoup. Handles JavaScript-rendered pages, anti-detection, structured exports, and multi-target scraping — with first-class support for manwha and web novel platforms.
 
---
 
## Why this exists
 
Most public scraping tools break on modern sites because they rely on static HTML. This framework uses Selenium with headless Chrome to render JavaScript, simulate real user behavior, and collect structured data at scale — the same stack used in production data pipelines.
 
The default collectors target manwha and web novel platforms, but the architecture is designed to be extended to any site.
 
---
