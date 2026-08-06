import requests
from bs4 import BeautifulSoup
import time
#from playwright.sync_api import sync_playwright
from html import unescape

HEADERS = {
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://www.rekhta.org/",
}

def fetch_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    try:
        session = requests.Session()
        session.get("https://www.rekhta.org", headers=headers)
        time.sleep(1)
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

    
    '''with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(url, wait_until="domcontentloaded")  # wait until page fully loads
            time.sleep(2)
            html = page.content()
            return html
            
        except Exception as e:
            print(f"Error fetching page: {e}")
            return None
            
        finally:
            browser.close()
            '''

    

def parse_poem(html, url):
    soup = BeautifulSoup(html, "html.parser")

    # --- Title ---
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else "Unknown Title"

    # --- Poet ---
    # Extract from title which is "poem name - Poet Name"
    poet = "Unknown Poet"
    if " - " in title:
        poet = title.split(" - ")[-1].strip()
        title = title.split(" - ")[0].strip()

    # --- Poem body div ---
    poem_body = soup.find("div", class_="poemPageContentBody")
    if not poem_body:
        print("Could not find poem body")
        return None

    # --- The poem is stored in a data-html attribute on an input tag ---
    input_tag = poem_body.find("input", attrs={"data-html": True})
    if not input_tag:
        print("Could not find data-html input tag")
        return None

    # Decode the HTML stored in the attribute
    encoded_html = input_tag["data-html"]
    decoded_html = unescape(encoded_html)
    inner_soup = BeautifulSoup(decoded_html, "html.parser")

    # --- Extract lines from <p> tags ---
    lines = []
    for p in inner_soup.find_all("p"):
        line = " ".join(span.get_text(strip=True) for span in p.find_all("span"))
        if line:
            lines.append(line)

    return {
        "title": title,
        "poet": poet,
        "lines": lines,
        "url": url
    }



def debug_html(url):
    html = fetch_page(url)
    if not html:
        return
    soup = BeautifulSoup(html, "html.parser")

    # Find the poem body and print its inner HTML
    poem_body = soup.find("div", class_="poemPageContentBody")
    if poem_body:
        print(poem_body.prettify()[:5000])
    else:
        print("poemPageContentBody not found")


def scrape_poem(url):
    # Force Urdu script
    if "?" not in url:
        url = url + "?lang=ur"
    
    print(f"Scraping: {url}")
    html = fetch_page(url)
    if not html:
        return None

    poem = parse_poem(html, url)
    if not poem or not poem["lines"]:
        print("Warning: No lines found.")
        return None

    print(f"Found: '{poem['title']}' by {poem['poet']} — {len(poem['lines'])} lines")
    return poem

def scrape_multiple(urls):
    poems = []
    
    for i, url in enumerate(urls):
        poem = scrape_poem(url)
        
        if poem:
            poems.append(poem)
        
        # Don't scrape the last URL, no need to wait after it
        if i < len(urls) - 1:
            time.sleep(1.5)  # wait 1.5 seconds between requests
    
    print(f"\nDone. Scraped {len(poems)}/{len(urls)} poems successfully.")
    return poems

if __name__ == "__main__":
    url = "https://www.rekhta.org/nazms/ye-maatam-e-vaqt-kii-ghadii-hai-faiz-ahmad-faiz-nazms"
    poem = scrape_poem(url)
    
    if poem:
        print(f"\n{poem['title']} — {poem['poet']}\n")
        for line in poem["lines"]:
            print(line)