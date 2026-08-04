import sqlite3

DB_NAME = "vocab.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS vocab (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            urdu_word           TEXT UNIQUE,
            english_translation TEXT,
            source_poem         TEXT,
            context_line        TEXT,
            date_added          TEXT DEFAULT (date('now')),
            times_reviewed      INTEGER DEFAULT 0,
            times_correct       INTEGER DEFAULT 0
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS poems (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            title      TEXT,
            poet       TEXT,
            url        TEXT UNIQUE,
            line_count INTEGER,
            date_read  TEXT DEFAULT (date('now'))
        )
    """)
    conn.commit()
    conn.close()


def save_word(urdu_word, english_translation, source_poem, context_line):
    conn = sqlite3.connect(DB_NAME)
    try:
        conn.execute("""
            INSERT OR IGNORE INTO vocab (urdu_word, english_translation, source_poem, context_line)
            VALUES (?, ?, ?, ?)
        """, (urdu_word, english_translation, source_poem, context_line))
        conn.commit()
    except Exception as e:
        print(f"Error saving word: {e}")
    finally:
        conn.close()


def get_all_words():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("""
        SELECT id, urdu_word, english_translation, source_poem, context_line, date_added
        FROM vocab ORDER BY date_added DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_word(urdu_word):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * FROM vocab WHERE urdu_word = ?", (urdu_word,))
    row = cursor.fetchone()
    conn.close()
    return row


def update_review(urdu_word, was_correct):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        UPDATE vocab
        SET times_reviewed = times_reviewed + 1,
            times_correct  = times_correct + ?
        WHERE urdu_word = ?
    """, (1 if was_correct else 0, urdu_word))
    conn.commit()
    conn.close()


def get_smart_deck():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("""
        SELECT urdu_word, english_translation,
               CASE
                   WHEN times_reviewed = 0 THEN 0.0
                   ELSE CAST(times_correct AS FLOAT) / times_reviewed
               END AS accuracy,
               context_line
        FROM vocab
        ORDER BY accuracy ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def save_poem_history(title, poet, url, line_count):
    conn = sqlite3.connect(DB_NAME)
    try:
        conn.execute("""
            INSERT OR REPLACE INTO poems (title, poet, url, line_count, date_read)
            VALUES (?, ?, ?, ?, date('now'))
        """, (title, poet, url, line_count))
        conn.commit()
    except Exception as e:
        print(f"Error saving poem history: {e}")
    finally:
        conn.close()


def get_poem_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("""
        SELECT title, poet, url, line_count, date_read
        FROM poems ORDER BY date_read DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows