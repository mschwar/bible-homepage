# bible-homepage

# Biblical Daily Verse Homepage

A minimalist personal homepage that displays a daily Bible verse each time you open your browser. It is designed to support scriptural reflection and a centered start to your day.

## Purpose

To create a peaceful digital threshold — a homepage that offers a moment for the soul with a daily verse from the Holy Bible.

## Live Demo

You can view and use the live version here:
[https://mschwar.github.io/bible-homepage/]
*(Note: Replace with your actual GitHub Pages URL after deploying.)*

## Key Features

-   **Daily Bible Verse:** Displays one verse from a curated collection each day.
-   **Curated Verse List:** Includes a Python script (`scripts/generate_bible_verses.py`) to easily manage and generate the list of verses used by the site.
-   **Client-Side Logic:** Uses JavaScript for:
    -   Fetching the locally stored verses.
    -   Selecting one verse deterministically based on the day of the year.
    -   Displaying today's and yesterday's verse.
-   **Clean and Focused Design:** Minimalist layout with an emphasis on the scripture.
-   **Light/Dark Mode:** Includes a theme toggle for comfortable viewing day or night.
-   **Lightweight and Fast:** Designed for quick loading.

## How It Works

1.  **Verse Preparation (Developer Task):**
    *   The developer edits the Python list of verses within `scripts/generate_bible_verses.py`.
    *   Running this script (`python scripts/generate_bible_verses.py`) generates the `data/quotes_bible.json` file. This file is then committed to the repository.
2.  **Homepage Display (User Browser):**
    *   When `index.html` is loaded, `js/script.js` executes.
    *   It fetches the verse data from `data/quotes_bible.json`.
    *   It selects one verse based on the current day of the year.
    *   The selected verse and its reference are then displayed.
    *   Buttons allow the user to also view the verse from the previous day.

## Setup and Usage

**For End-Users (Viewing & Setting as Homepage):**

1.  Visit the live demo link above.
2.  To set it as your browser’s homepage, follow the standard procedure for your browser (e.g., Chrome, Firefox, Safari, Edge) and use the live demo URL.

**For Developers (Running Locally or Modifying):**

1.  **Clone or download** the repository.
2.  **Python Environment (for updating verses):**
    *   Ensure Python 3 is installed.
    *   To add, remove, or change verses, edit the `verses` list in `scripts/generate_bible_verses.py`.
    *   Then, run the script from the `scripts` directory:
        ```bash
        python generate_bible_verses.py
        ```
    *   This will update `data/quotes_bible.json`.
3.  **Viewing Locally:** Open `index.html` in any web browser.
4.  **Committing Changes:** If you update the generated `quotes_bible.json`, commit both the script and the JSON file to your repository.

## Customization

-   **Adding More Verses:** The primary way to customize is to edit `scripts/generate_bible_verses.py` and re-run it. This gives you full control over the verses displayed.
-   **Styling:** Modify `css/style.css` to change the appearance.

## Acknowledgements

This project was adapted from the "Bahá’í Daily Homepage" and is inspired by a desire for a simple, reflective online starting point.

> *“Your word is a lamp for my feet, a light on my path.”*
> — Psalm 119:105
