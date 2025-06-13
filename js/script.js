// js/script.js – cleaned & minimal

/* ---------------- CONFIG --------------- */
const QUOTE_FILE = 'data/quotes_bible.json';
const MAX_WORDS = 75;

/* ---------------- THEME ---------------- */
const toggleBtn = document.getElementById('theme-toggle-button');
const stored = localStorage.getItem('theme');
document.body.classList.add(stored || 'light-mode');
toggleBtn.onclick = () => {
  document.body.classList.toggle('dark-mode');
  document.body.classList.toggle('light-mode');
  localStorage.setItem('theme',
    document.body.classList.contains('dark-mode') ? 'dark-mode' : 'light-mode');
};

/* ------------- QUOTE HELPERS ----------- */
const dayOfYear = d => Math.floor((d - new Date(d.getFullYear(),0,0))/8.64e7);
const countWords = t => t.trim().split(/\s+/).length;

async function loadQuotes(){
  const res = await fetch(QUOTE_FILE); return res.ok ? res.json() : [];
}

function pick(list, idx){return list[idx % list.length];}

/* ------------- RENDERERS --------------- */
function renderQuote(obj,suffix=''){
  document.getElementById(`quote-text${suffix}`).textContent = obj.text;
  document.getElementById(`quote-author${suffix}`).textContent = obj.source;
}
function renderDate(d,id){
  document.getElementById(id).textContent = d.toLocaleDateString(
    undefined,{weekday:'long',year:'numeric',month:'long',day:'numeric'});
}

/* ------------- MAIN -------------------- */
let qToday, qYest;

(async ()=>{
  const all = (await loadQuotes()).filter(q=>countWords(q.text)<=MAX_WORDS);
  const now = new Date(), yest = new Date(now);
  yest.setDate(now.getDate()-1);
  qToday = pick(all, dayOfYear(now));
  qYest  = pick(all, dayOfYear(yest));
  renderQuote(qToday);
  renderQuote(qYest,'-yesterday');
  renderDate(now,'gregorianDatePanel');
})();

/* ------------- EVENTS ------------------ */
document.getElementById('scroll-down-arrow')
        .addEventListener('click', e=>{
          e.preventDefault();
          document.querySelector('.panel-date')
                  .scrollIntoView({behavior:'smooth'});
        });

document.getElementById('yesterday-button')
        .addEventListener('click',e=>{
          e.preventDefault();
          const sec=document.getElementById('yesterday-jumbotron-display');
          sec.style.display='flex';
          sec.scrollIntoView({behavior:'smooth'});
        });

document.getElementById('yesterday-arrow')
        .addEventListener('click',e=>{
          e.preventDefault();
          document.getElementById('quote-source-full-yesterday')
                  .classList.toggle('visible');
        });

document.getElementById('quote-text')
        .onclick = ()=>navigator.clipboard.writeText(`${qToday.text}\n— ${qToday.source}`);
document.getElementById('quote-text-yesterday')
        .onclick = ()=>navigator.clipboard.writeText(`${qYest.text}\n— ${qYest.source}`);
