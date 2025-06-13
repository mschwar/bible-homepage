// js/script.js

// --- GLOBAL CONFIG & STATE ---
const MAX_WORDS = 75; // Using the filter from the new script
let ALL_QUOTES = [];
let FILTERED_QUOTES = [];
let currentQuoteObjectForToday = null;
let currentQuoteObjectForYesterday = null;

// --- THEME TOGGLE ---
function setupThemeToggle() {
    const themeToggleButton = document.getElementById('theme-toggle-button');
    const currentTheme = localStorage.getItem('theme');
    document.body.classList.add(currentTheme || 'light-mode');

    if (themeToggleButton) {
        themeToggleButton.addEventListener('click', () => {
            const isDarkMode = document.body.classList.toggle('dark-mode');
            document.body.classList.toggle('light-mode', !isDarkMode);
            localStorage.setItem('theme', isDarkMode ? 'dark-mode' : 'light-mode');
        });
    }
}

// --- QUOTE & DATE LOGIC ---
async function fetchQuotes(fileName = 'data/quotes_bible.json') {
    try {
        const response = await fetch(fileName);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error("Could not fetch verses:", error);
        return [];
    }
}

function filterQuotesByLength(quotesArray, maxWords) {
    return quotesArray.filter(q => q.text.split(/\s+/).length <= maxWords);
}

function getDayOfYear(date = new Date()) {
    const start = new Date(date.getFullYear(), 0, 0);
    const diff = (date - start) + ((start.getTimezoneOffset() - date.getTimezoneOffset()) * 60 * 1000);
    const oneDay = 1000 * 60 * 60 * 24;
    return Math.floor(diff / oneDay);
}

function getQuoteByDay(quotesArray, dayOfYear) {
    if (!quotesArray || quotesArray.length === 0) return null;
    const index = dayOfYear % quotesArray.length;
    return quotesArray[index];
}

function displayQuote(quoteObject, type = "today") {
    const textElId = type === "today" ? 'quote-text' : 'quote-text-yesterday';
    const authorElId = type === "today" ? 'quote-author' : 'quote-author-yesterday';

    const quoteTextElement = document.getElementById(textElId);
    const quoteAuthorElement = document.getElementById(authorElId);

    if (type === 'today') currentQuoteObjectForToday = quoteObject;
    else currentQuoteObjectForYesterday = quoteObject;

    if (quoteTextElement && quoteAuthorElement) {
        if (quoteObject && quoteObject.text) {
            quoteTextElement.textContent = quoteObject.text;
            // Use the 'source' field (e.g., "John 3:16") for the attribution line
            quoteAuthorElement.textContent = quoteObject.source || 'Unknown Reference';
        } else {
            quoteTextElement.textContent = "No verse available for this day.";
            quoteAuthorElement.textContent = "";
        }
    } else {
        console.error(`Error displaying verse: One or more elements not found for type "${type}"`);
    }
}

function displayGregorianDate(date = new Date(), elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = date.toLocaleDateString(undefined, {
            weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
        });
    }
}

// --- INITIALIZATION & PAGE SETUP ---
async function initializePage() {
    ALL_QUOTES = await fetchQuotes();
    if (!Array.isArray(ALL_QUOTES) || ALL_QUOTES.length === 0) {
        displayQuote(null, "today");
        return;
    }
    // Apply the word count filter from the new script's logic
    FILTERED_QUOTES = filterQuotesByLength(ALL_QUOTES, MAX_WORDS);
    console.log(`Loaded ${ALL_QUOTES.length} verses, using ${FILTERED_QUOTES.length} after filtering.`);

    // --- Populate Today's Content ---
    const todayDateObj = new Date();
    const dayOfYearToday = getDayOfYear(todayDateObj);
    const todaysQuote = getQuoteByDay(FILTERED_QUOTES, dayOfYearToday);
    displayQuote(todaysQuote, "today");
    displayGregorianDate(todayDateObj, "gregorianDatePanel");
}

// --- EVENT HANDLING ---
function showYesterdaySection() {
    if (FILTERED_QUOTES.length === 0) return;

    const yesterdaySection = document.getElementById('yesterday-jumbotron-display');
    if (!yesterdaySection) return;

    // --- Populate Yesterday's Content ---
    const today = new Date();
    const yesterdayDateObj = new Date(today);
    yesterdayDateObj.setDate(today.getDate() - 1);

    const dayOfYearYesterday = getDayOfYear(yesterdayDateObj);
    const yesterdaysQuote = getQuoteByDay(FILTERED_QUOTES, dayOfYearYesterday);

    displayQuote(yesterdaysQuote, "yesterday");
    displayGregorianDate(yesterdayDateObj, "gregorianDateYesterday");

    const wasHidden = yesterdaySection.style.display === 'none';
    if (wasHidden) {
        yesterdaySection.style.display = 'flex';
        setTimeout(() => {
            yesterdaySection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 50);
    } else {
        yesterdaySection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    document.getElementById('yesterday-button')?.classList.add('button-active');
    document.getElementById('today-button')?.classList.remove('button-active');
}

function showTodaySection() {
    document.getElementById('main-jumbotron').scrollIntoView({ behavior: 'smooth' });
    const yesterdaySection = document.getElementById('yesterday-jumbotron-display');
    if (yesterdaySection) {
        yesterdaySection.style.display = 'none';
    }
    document.getElementById('today-button')?.classList.add('button-active');
    document.getElementById('yesterday-button')?.classList.remove('button-active');
}

function copyQuoteToClipboard(quoteObj) {
    if (quoteObj && quoteObj.text) {
        let textToCopy = `${quoteObj.text}\n— ${quoteObj.source}`;
        navigator.clipboard.writeText(textToCopy.trim()).then(() => {
            alert("Verse copied to clipboard!");
        }).catch(err => console.error('Failed to copy text: ', err));
    }
}

function setupEventListeners() {
    document.getElementById('today-button')?.addEventListener('click', (e) => {
        e.preventDefault();
        showTodaySection();
    });
    document.getElementById('yesterday-button')?.addEventListener('click', (e) => {
        e.preventDefault();
        showYesterdaySection();
    });
    document.getElementById('scroll-down-arrow')?.addEventListener('click', (e) => {
        e.preventDefault();
        document.querySelector(e.currentTarget.getAttribute('href')).scrollIntoView({ behavior: 'smooth' });
    });
    document.getElementById('quote-text')?.addEventListener('click', () => copyQuoteToClipboard(currentQuoteObjectForToday));
    document.getElementById('quote-text-yesterday')?.addEventListener('click', () => copyQuoteToClipboard(currentQuoteObjectForYesterday));
}

// --- DOM Ready ---
document.addEventListener('DOMContentLoaded', async () => {
    setupThemeToggle();
    await initializePage();
    setupEventListeners();
});