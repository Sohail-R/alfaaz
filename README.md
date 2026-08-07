# Alfaaz — الفاظ
This is my passion project for learning Urdu vocabulary, derived from poetry shared on rekhta.org.

Live at https://alfaaz-production.up.railway.app/

## Features:
Nastaliq Script: Alfaaz uses the authentic native Urdu Nastaliq script read from right to left.
Flashcards: Test your vocabulary with the word bank of words you've saved.
Line by Line Translation: Every line in Urdu has its corresponding English translation.
Transliteration: For those who can't read the Urdu script but want to know how the words sound.
Site-wide Roman Toggle: Switches the rest of the site to the Roman script for easier reading
Reading History: Tracks every poem you've read, no need to re-paste.

## How It Works:
1. Paste the URL of a Rekhta Poem, for example: https://www.rekhta.org/ghazals/aae-kuchh-abr-kuchh-sharaab-aae-faiz-ahmad-faiz-ghazals?lang=ur
2. The scraper fetches the poem and displays it in the Urdu Nastaliq script. Use transliteration or translation tools if preferred.
3. Click on any word you don't know or want to add to your word bank!
4. Test yourself with flashcards; words you get wrong will appear first.
5. Poems you've previously read are saved for you to come back to later.

## Tech Stack:
| Layer | Technology |
| Backend | Python, Flask |
| Scraping | Requests, BeautifulSoup, Playwright |
| Translation | deep-translator (Google Translate) |
| Database | SQLite |
| Frontend | Vanilla HTML, CSS, JavaScript |
| Fonts | Noto Nastaliq Urdu, Cormorant Garamond |
| Deployment | Railway |


## Project Structure:
alfaaz/
├── app.py # Flask routes
├── scraper.py # Rekhta poem scraper
├── translator.py # Translation and transliteration
├── database.py # SQLite operations
├── flashcards.py # Flashcard session logic
├── templates/ # HTML templates
└── static/ # CSS and JS


## Notes:

- Vocab data is stored locally in SQLite — words reset on each server redeploy
- Poem content is scraped live from Rekhta on each load
- Built as a personal learning tool and CS portfolio project

---



