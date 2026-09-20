// LinkedIn Web Session Harvester for Chrome / Browser Tools
// Execute inside the active tab console or via browser javascript_tool
(async () => {
  const list = document.querySelector('.scaffold-layout__list > div, .jobs-search-results-list, ul.scaffold-layout__list-container') || document.querySelector('.scaffold-layout__list');
  const EXCL = /\b(senior|sr\.?|staff|principal|lead|head|director|vp|chief|architect|intern|internship|werkstudent|manager|expert opportunity|graduate)\b/i;
  const NOISE = /data engineer|cloud data|electrical|mechanical|automotive|mv\/hv|plc|inverter|siemens|\.net|\bjava\b|c#|c\+\+|golang|manufacturing|test engineer|qa test|recruit|agenzia|sap\b|salesforce|servicenow|embedded|firmware|hardware|network|security|sysadmin|infrastructure|platform operations|devops|sre\b|payload|satellite|adp\b|barsel|agency|business development|quality engineer|process engineer|hydraulic|constructie|pharma|e-mobility|space earth/i;
  const LANG = /ing[eé]nieur|ingeniero|in[zż]ynier|d[eé]veloppeur|entwickler|testeur|sviluppatore|programmatore|\bm\/w\/d\b|\bw\/m\/d\b|\bh\/f\b|\bf\/h\b|\bf\/m\b|\bd\/f\/m\b|[Α-ω]|praktik|stagiaire|alternance|:in\b/i;

  const cards = {};
  const collect = () => {
    document.querySelectorAll('li[data-occludable-job-id], .job-card-container[data-job-id]').forEach(li => {
      const id = li.getAttribute('data-occludable-job-id') || li.getAttribute('data-job-id');
      if (!id) return;
      const t = (li.querySelector('.job-card-list__title, .job-card-container__link strong, a.job-card-container__link')?.innerText || '').split('\n')[0].trim();
      if (!t) {
        cards[id] = cards[id] || null;
        return;
      }
      const co = (li.querySelector('.artdeco-entity-lockup__subtitle, .job-card-container__primary-description, .job-card-container__company-name')?.innerText || '').trim();
      const loc = (li.querySelector('.job-card-container__metadata-item, .artdeco-entity-lockup__caption')?.innerText || '').trim();
      cards[id] = { t, co, loc, ea: /Easy Apply/.test(li.innerText) };
    });
  };

  if (list) list.scrollTop = 0;
  collect();

  for (let i = 0; i < 10; i++) {
    if (list) {
      list.scrollTop += 500;
    } else {
      window.scrollBy(0, 500);
    }
    await new Promise(r => setTimeout(r, 450));
    collect();
  }

  const out = [];
  let dropped = 0, blank = 0;
  for (const [id, c] of Object.entries(cards)) {
    if (!c) {
      blank++;
      continue;
    }
    if (EXCL.test(c.t) || NOISE.test(c.t + ' ' + c.co) || LANG.test(c.t)) {
      dropped++;
      continue;
    }
    out.push({
      id,
      title: c.t,
      company: c.co,
      location: c.loc,
      easy_apply: c.ea,
      url: `https://www.linkedin.com/jobs/view/${id}/`
    });
  }

  return { total: Object.keys(cards).length, blank, dropped, jobs: out };
})();
