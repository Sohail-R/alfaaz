import random
from database import get_smart_deck, update_review

def run_session():
    deck = get_smart_deck()
    
    if not deck:
        print("No words in your deck yet! Scrape some poems first.")
        return
    
    print(f"\n🃏 Starting flashcard session — {len(deck)} words")
    print("Type the English translation. Press Enter to skip.\n")
    
    correct = 0
    wrong = 0
    skipped = 0
    
    for urdu_word, translation, accuracy in deck:
        print(f"  {urdu_word}")
        guess = input("  → ").strip().lower()
        
        if guess == "":
            print(f"  Skipped — answer was: {translation}\n")
            skipped += 1
            continue
        
        # Check if guess appears anywhere in the translation
        # e.g. "sky" should match "The sky"
        if guess in translation.lower():
            print(f"  ✓ Correct!\n")
            correct += 1
            update_review(urdu_word, was_correct=True)
        else:
            print(f"  ✗ Answer was: {translation}\n")
            wrong += 1
            update_review(urdu_word, was_correct=False)
    
    # Session summary
    total = correct + wrong + skipped
    print("=" * 30)
    print(f"Session complete!")
    print(f"✓ Correct:  {correct}/{total}")
    print(f"✗ Wrong:    {wrong}/{total}")
    print(f"  Skipped:  {skipped}/{total}")
    if total > 0:
        pct = round((correct / total) * 100)
        print(f"  Accuracy: {pct}%")
    print("=" * 30)


def show_deck():
    deck = get_smart_deck()
    
    if not deck:
        print("No words saved yet.")
        return
    
    print(f"\n{'Urdu':<20} {'Translation':<25} {'Accuracy'}")
    print("-" * 55)
    
    for urdu_word, translation, accuracy in deck:
        if accuracy == 0.0:
            acc_str = "never reviewed"
        else:
            acc_str = f"{round(accuracy * 100)}%"
        print(f"{urdu_word:<20} {translation:<25} {acc_str}")


# --- Test it ---
if __name__ == "__main__":
    print("1. Run flashcard session")
    print("2. Show full deck")
    choice = input("\nChoose: ").strip()
    
    if choice == "1":
        run_session()
    elif choice == "2":
        show_deck()
    else:
        print("Invalid choice")