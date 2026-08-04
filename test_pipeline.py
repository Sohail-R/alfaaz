from scraper import scrape_poem
from translator import translate_word, translate_line
from database import init_db, save_word, get_all_words

# Setup
init_db()

# Step 1 — scrape a poem
url = "https://www.rekhta.org/nazms/ye-maatam-e-vaqt-kii-ghadii-hai-faiz-ahmad-faiz-nazms"
poem = scrape_poem(url)

# Step 2 — grab the first line and its words
first_line = poem["lines"][0]
words = first_line.split()

print(f"First line: {first_line}")
print(f"Line meaning: {translate_line(first_line)}")
print()

# Step 3 — translate and save each word
for word in words:
    translation = translate_word(word)
    if translation:
        save_word(word, translation, poem["title"], first_line)

# Step 4 — confirm they're in the database
print("\n=== Saved Words ===")
for row in get_all_words():
    print(f"{row[1]} → {row[2]} | from: {row[3]}")