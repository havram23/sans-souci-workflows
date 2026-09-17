'use strict';
const themeButton = document.querySelector('[data-theme-toggle]');
themeButton?.addEventListener('click', () => {
  const light = document.documentElement.dataset.theme !== 'light';
  document.documentElement.dataset.theme = light ? 'light' : 'dark';
  themeButton.setAttribute('aria-pressed', String(light));
  themeButton.textContent = light ? 'Dunkles Design' : 'Helles Design';
});
const search = document.querySelector('#search');
if (search) {
  const format = document.querySelector('#format');
  const chips = [...document.querySelectorAll('[data-category]')];
  const cards = [...document.querySelectorAll('[data-starter]')];
  const params = new URLSearchParams(location.search);
  let category = chips.some(button => button.dataset.category === params.get('category')) ? params.get('category') : '';
  search.value = (params.get('q') || '').slice(0, 150);
  format.value = ['Python','n8n'].includes(params.get('format')) ? params.get('format') : '';
  const apply = () => {
    const terms = search.value.trim().toLocaleLowerCase('de').split(/\s+/).filter(Boolean);
    let visible = 0;
    for (const card of cards) {
      const match = (!category || card.dataset.group === category) && (!format.value || card.dataset.format === format.value) && terms.every(term => card.dataset.search.includes(term));
      card.hidden = !match;
      if (match) visible++;
    }
    for (const chip of chips) chip.setAttribute('aria-pressed', String(chip.dataset.category === category));
    document.querySelector('#result-count').textContent = `${visible} von ${cards.length} Startern`;
    document.querySelector('#empty').hidden = visible !== 0;
    const next = new URL(location.href);
    for (const [key,value] of [['q',search.value],['format',format.value],['category',category]]) {
      if (value) next.searchParams.set(key,value); else next.searchParams.delete(key);
    }
    history.replaceState(null,'',next);
  };
  search.addEventListener('input',apply);
  format.addEventListener('change',apply);
  chips.forEach(chip => chip.addEventListener('click',()=>{category=chip.dataset.category;apply();}));
  document.querySelector('#reset').addEventListener('click',()=>{search.value='';format.value='';category='';apply();search.focus();});
  apply();
}
for (const button of document.querySelectorAll('[data-copy]')) button.addEventListener('click', async () => {
  const text = document.getElementById(button.dataset.copy).textContent;
  const status = button.parentElement.querySelector('[role=status]');
  try { await navigator.clipboard.writeText(text); status.textContent='Befehl kopiert. Im Projektordner ausführen.'; }
  catch { status.textContent='Bitte den Befehl markieren und manuell kopieren.'; }
});
