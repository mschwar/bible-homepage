import json
import os

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_QUOTES_PATH = os.path.join(PROJECT_ROOT, 'data', 'quotes_bible.json')

# --- Curated List of Bible Verses ---
# Add or remove verses here.
# The structure is a list of dictionaries, each with "text" and "source".
verses = [
    {
        "text": "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.",
        "source": "John 3:16"
    },
    {
        "text": "I can do all this through him who gives me strength.",
        "source": "Philippians 4:13"
    },
    {
        "text": "The Lord is my shepherd, I lack nothing.",
        "source": "Psalm 23:1"
    },
    {
        "text": "Trust in the Lord with all your heart and lean not on your own understanding; in all your ways submit to him, and he will make your paths straight.",
        "source": "Proverbs 3:5-6"
    },
    {
        "text": "For I know the plans I have for you,” declares the Lord, “plans to prosper you and not to harm you, plans to give you hope and a future.",
        "source": "Jeremiah 29:11"
    },
    {
        "text": "Be still, and know that I am God.",
        "source": "Psalm 46:10"
    },
    {
        "text": "The fruit of the Spirit is love, joy, peace, forbearance, kindness, goodness, faithfulness, gentleness and self-control.",
        "source": "Galatians 5:22-23"
    },
    {
        "text": "And we know that in all things God works for the good of those who love him, who have been called according to his purpose.",
        "source": "Romans 8:28"
    },
    {
        "text": "Your word is a lamp for my feet, a light on my path.",
        "source": "Psalm 119:105"
    },
    {
        "text": "Come to me, all you who are weary and burdened, and I will give you rest.",
        "source": "Matthew 11:28"
    },
    {
        "text": "Love is patient, love is kind. It does not envy, it does not boast, it is not proud.",
        "source": "1 Corinthians 13:4"
    },
    {
        "text": "So do not fear, for I am with you; do not be dismayed, for I am your God. I will strengthen you and help you; I will uphold you with my righteous right hand.",
        "source": "Isaiah 41:10"
    },
    {
        "text": "Have I not commanded you? Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go.",
        "source": "Joshua 1:9"
    }
    # Add more of your favorite verses here...
]

def save_quotes_to_json(quotes, filepath):
    """Saves the list of quotes to a JSON file."""
    if not quotes:
        print("No quotes to save.")
        return
    try:
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(quotes, f, indent=2, ensure_ascii=False)
        print(f"Verses successfully saved to: {filepath} ({len(quotes)} verses)")
    except IOError as e:
        print(f"Error saving verses to {filepath}: {e}")

if __name__ == "__main__":
    print("Generating Bible verses JSON file...")
    save_quotes_to_json(verses, OUTPUT_QUOTES_PATH)