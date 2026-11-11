// autenflo blog admin: login + users + drafts + publish (GitHub par commit)
// Netlify env variables: GITHUB_TOKEN, GITHUB_REPO, SESSION_SECRET, SETUP_KEY
// Optional: GITHUB_BRANCH (default main), GITHUB_BASE (site subfolder), SITE_URL
import crypto from 'node:crypto';

const E = process.env;
const SITE = () => (E.SITE_URL || 'https://autenflo.com').replace(/\/$/, '');
const CATS = ['AI', 'Marketing', 'Sales', 'Finance', 'Business Tips'];
const LAYOUTS = ['classic', 'cover', 'magazine', 'minimal'];
const json = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { 'content-type': 'application/json' } });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ---------- storage (Netlify Blobs) ----------
const store = async () => globalThis.__AUT_STORE || (await import('@netlify/blobs')).getStore({ name: 'autenflo-admin', consistency: 'strong' });
const getUsers = async () => (await (await store()).get('users', { type: 'json' })) || [];
const putUsers = async (u) => (await store()).setJSON('users', u);
const getDrafts = async () => (await (await store()).get('drafts', { type: 'json' })) || {};
const putDrafts = async (d) => (await store()).setJSON('drafts', d);

// ---------- auth ----------
const b64u = (s) => Buffer.from(s).toString('base64url');
const mac = (b) => crypto.createHmac('sha256', E.SESSION_SECRET || '').update(b).digest('base64url');
const sign = (p) => { const b = b64u(JSON.stringify(p)); return b + '.' + mac(b); };
function verify(t) {
  try {
    const [b, s] = String(t).split('.'); const e = mac(b);
    if (!s || s.length !== e.length || !crypto.timingSafeEqual(Buffer.from(s), Buffer.from(e))) return null;
    const p = JSON.parse(Buffer.from(b, 'base64url').toString()); return p.exp > Date.now() ? p : null;
  } catch { return null; }
}
const hashPw = (pw, salt) => crypto.scryptSync(pw, salt, 64).toString('hex');
const mkUser = (u, pw) => { const salt = crypto.randomBytes(16).toString('hex'); return { u, salt, hash: hashPw(pw, salt), created: new Date().toISOString() }; };
const okPw = (usr, pw) => { const a = Buffer.from(hashPw(pw, usr.salt)), b = Buffer.from(usr.hash); return a.length === b.length && crypto.timingSafeEqual(a, b); };
const token = (u) => sign({ u, exp: Date.now() + 7 * 24 * 3600 * 1000 });
const validUser = (u) => /^[a-zA-Z0-9._-]{3,30}$/.test(u || '');

// ---------- GitHub ----------
const BASE = () => { const b = (E.GITHUB_BASE || '').trim(); return b && !b.endsWith('/') ? b + '/' : b; };
const BR = () => E.GITHUB_BRANCH || 'main';
const gh = (p, o = {}) => fetch('https://api.github.com/repos/' + E.GITHUB_REPO + p, { ...o, headers: { Authorization: 'Bearer ' + E.GITHUB_TOKEN, Accept: 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'autenflo-admin', ...(o.headers || {}) } });
async function J(r) { if (!r.ok) { let e = {}; try { e = await r.json(); } catch {} throw new Error('GitHub: ' + (e.message || r.status)); } return r.json(); }
async function getRaw(p) {
  const r = await gh('/contents/' + encodeURI(BASE() + p) + '?ref=' + BR(), { headers: { Accept: 'application/vnd.github.raw+json' } });
  if (r.status === 404) return null; if (!r.ok) throw new Error('GitHub: ' + r.status); return r.text();
}
async function commit(files, images, msg) {
  const ref = await J(await gh('/git/ref/heads/' + BR())), parent = ref.object.sha, pc = await J(await gh('/git/commits/' + parent)), tree = [];
  for (const f of files) tree.push(f.content === null ? { path: BASE() + f.path, mode: '100644', type: 'blob', sha: null } : { path: BASE() + f.path, mode: '100644', type: 'blob', content: f.content });
  for (const im of images) { const b = await J(await gh('/git/blobs', { method: 'POST', body: JSON.stringify({ content: im.b64, encoding: 'base64' }) })); tree.push({ path: BASE() + im.path, mode: '100644', type: 'blob', sha: b.sha }); }
  const t = await J(await gh('/git/trees', { method: 'POST', body: JSON.stringify({ base_tree: pc.tree.sha, tree }) }));
  const c = await J(await gh('/git/commits', { method: 'POST', body: JSON.stringify({ message: msg, tree: t.sha, parents: [parent] }) }));
  await J(await gh('/git/refs/heads/' + BR(), { method: 'PATCH', body: JSON.stringify({ sha: c.sha }) }));
}

// ---------- html helpers ----------
const esc = (t) => String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const escA = (t) => esc(t).replace(/"/g, '&quot;');
const OK = { h2: [], h3: [], h4: [], p: [], br: [], b: [], strong: [], i: [], em: [], u: [], ul: [], ol: [], li: [], blockquote: [], hr: [], code: [], pre: [], span: [], div: [], a: ['href', 'target', 'rel'], img: ['src', 'alt'] };
export function clean(html, allowData) {
  html = String(html || '').replace(/<!--[\s\S]*?-->/g, '').replace(/<(script|style|iframe|object|embed|form)[\s\S]*?<\/\1>/gi, '');
  return html.replace(/<\/?([a-zA-Z0-9]+)([^>]*)>/g, (m, tag, attrs) => {
    tag = tag.toLowerCase(); if (!(tag in OK)) return ''; if (m[1] === '/') return '</' + tag + '>';
    let out = '';
    (attrs.match(/([a-zA-Z-]+)\s*=\s*("[^"]*"|'[^']*')/g) || []).forEach((a) => {
      const mm = a.match(/([a-zA-Z-]+)\s*=\s*(?:"([^"]*)"|'([^']*)')/); const n = mm[1].toLowerCase(); const v = (mm[2] !== undefined ? mm[2] : mm[3]).trim();
      if (!OK[tag].includes(n)) return;
      if ((n === 'href' || n === 'src') && !(/^(https?:\/\/|\/|#|mailto:|tel:)/i.test(v) || (allowData && n === 'src' && /^data:image\//i.test(v)))) return;
      out += ' ' + n + '="' + v.replace(/"/g, '&quot;') + '"';
    });
    if (tag === 'a' && /target="_blank"/.test(out) && !/rel=/.test(out)) out += ' rel="noopener"';
    return '<' + tag + out + '>';
  });
}
const ART = { AI: ['#3b7fd4', '#8a62d6', '<g stroke="#fff" stroke-width="3" opacity=".7"><path d="M120 110L200 70L280 120L200 160ZM200 70V160M120 110L280 120"/></g><g fill="#fff"><circle cx="120" cy="110" r="10"/><circle cx="200" cy="70" r="12"/><circle cx="280" cy="120" r="10"/><circle cx="200" cy="160" r="10"/></g><rect x="160" y="100" width="80" height="44" rx="12" fill="#17202A" opacity=".75"/><text x="200" y="131" text-anchor="middle" font-family="Outfit,sans-serif" font-weight="800" font-size="24" fill="#fff">AI</text>'],
  Marketing: ['#d6568b', '#f2b84b', '<path fill="#fff" d="M120 100v40l90 36V64Z"/><path fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" d="M230 96c26 10 26 54 0 64M250 80c42 18 42 82 0 100"/><rect x="128" y="146" width="22" height="46" rx="6" fill="#fff" opacity=".7"/>'],
  Sales: ['#2f9a7c', '#3b7fd4', '<g fill="#fff"><rect x="110" y="140" width="34" height="50" rx="6" opacity=".6"/><rect x="160" y="110" width="34" height="80" rx="6" opacity=".75"/><rect x="210" y="80" width="34" height="110" rx="6"/></g><path fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" d="M260 120l30-40M262 78h30v30"/>'],
  Finance: ['#f28c28', '#8a62d6', '<g fill="#f2b84b" stroke="#fff" stroke-width="5"><circle cx="150" cy="150" r="38"/><circle cx="215" cy="125" r="38"/><circle cx="270" cy="160" r="30"/></g><path fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" d="M200 108h30M200 124h30M206 108c26 0 26 22 0 22l22 24"/>'],
  'Business Tips': ['#8a62d6', '#2f9a7c', '<path fill="#f2b84b" d="M200 56a42 42 0 0 0-22 78v22h44v-22a42 42 0 0 0-22-78Z"/><rect x="180" y="162" width="40" height="10" rx="5" fill="#fff"/><rect x="186" y="178" width="28" height="10" rx="5" fill="#fff" opacity=".8"/><g stroke="#fff" stroke-width="6" stroke-linecap="round"><path d="M120 100l-22-8M280 100l22-8M200 30v-14"/></g>'] };
const art = (c) => { const a = ART[c] || ART.AI; return '<svg viewBox="0 0 400 220" role="img" aria-label="' + escA(c) + '" xmlns="http://www.w3.org/2000/svg"><rect width="400" height="220" fill="' + a[0] + '"/><circle cx="350" cy="30" r="90" fill="' + a[1] + '" opacity=".45"/><circle cx="30" cy="210" r="70" fill="' + a[1] + '" opacity=".3"/>' + a[2] + '</svg>'; };
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const dlabel = (d) => { const x = new Date(d + 'T00:00:00'); return x.getDate() + ' ' + MONTHS[x.getMonth()] + ' ' + x.getFullYear(); };
const WI = '<svg class="wi" viewBox="0 0 24 24" aria-hidden="true"><use href="#wa"></use></svg>';
const waUrl = (t) => 'https://wa.me/918849031907?text=' + encodeURIComponent(t);
const ldTag = (o) => '<script type="application/ld+json">' + JSON.stringify(o).replace(/</g, '\\u003c') + '</script>';
const media = (p) => (p.cover ? '<img src="' + escA(p.cover) + '" alt="' + escA(p.coverAlt || p.title) + '">' : art(p.cat));

export function setHead(h, o) {
  const rp = (re, v) => { h = h.replace(re, (m, a) => a + v); };
  h = h.replace(/<title>[\s\S]*?<\/title>/, '<title>' + esc(o.title) + '</title>');
  rp(/(<meta name="description" content=")[^"]*/, escA(o.desc)); rp(/(<link rel="canonical" href=")[^"]*/, o.url);
  rp(/(<meta property="og:title" content=")[^"]*/, escA(o.title)); rp(/(<meta property="og:description" content=")[^"]*/, escA(o.desc));
  rp(/(<meta property="og:url" content=")[^"]*/, o.url); rp(/(<meta property="og:type" content=")[^"]*/, o.type); rp(/(<meta property="og:image" content=")[^"]*/, o.image);
  h = h.replace(/<script type="application\/ld\+json">[\s\S]*?<\/script>/g, '').replace(/<link rel="stylesheet" href="\/assets\/blog-layouts\.css">/g, '').replace(/<meta name="twitter:[^>]*>/g, '');
  const tw = '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="' + escA(o.title) + '"><meta name="twitter:description" content="' + escA(o.desc) + '"><meta name="twitter:image" content="' + escA(o.image) + '">';
  return h.replace('</head>', '<link rel="stylesheet" href="/assets/blog-layouts.css">' + tw + o.ld.map(ldTag).join('') + '</head>');
}
export function postMain(p) {
  const meta = '<p class="meta">' + esc(p.cat) + ' · ' + dlabel(p.date) + (p.author ? ' · ' + esc(p.author) : '') + '</p>', h1 = '<h1 class="h1s">' + esc(p.title) + '</h1>', sub = '<p class="sub">' + esc(p.desc) + '</p>';
  let head;
  if (p.layout === 'cover') head = '<div class="pl-cover">' + media(p) + '</div><div class="pl-head center">' + meta + h1 + sub + '</div>';
  else if (p.layout === 'minimal') head = '<div class="pl-head center">' + meta + h1 + sub + '</div>';
  else if (p.layout === 'magazine') head = '<div class="pl-head mag">' + meta + h1 + '</div><div class="pl-cover wide">' + media(p) + '</div><p class="lead-box">' + esc(p.desc) + '</p>';
  else head = '<div class="post-head"><div>' + meta + h1 + sub + '</div><div class="post-art">' + media(p) + '</div></div>';
  const cta = p.cta === false ? '' : '<div class="glass fin2"><div><h2>Apne business me <b class="aih">AI</b> lagayein.</h2><p class="sub">WhatsApp par 15 minute baat karke dekhiye aapke liye kya sahi rahega.</p></div><a class="btn wab mag" href="' + waUrl('Namaste autenflo, maine aapka blog padha. Mujhe apne business ko AI ki power chahiye.') + '">' + WI + 'WhatsApp par baat karein</a></div>';
  return '<main id="top" class="sec lay-' + p.layout + '"><div class="wrap"><p class="crumbs"><a href="/">Home</a> / <a href="/blog/">Blog</a></p>\n<article>' + head + '\n<div class="prose' + (p.layout === 'magazine' ? ' mag' : '') + '">\n' + p.html + '\n</div></article>\n' + cta + '</div></main>';
}
export function indexMain(ps) {
  const cards = ps.map((p) => '<a class="bc glass" href="/blog/' + p.slug + '.html">' + media(p) + '<div><p class="meta">' + esc(p.cat) + ' · ' + dlabel(p.date) + '</p><h3>' + esc(p.title) + '</h3><p>' + esc(p.desc) + '</p></div></a>').join('\n');
  return '<main id="top" class="sec"><div class="wrap"><p class="crumbs"><a href="/">Home</a> / Blog</p><span class="eyebrow">Blog</span><h1 class="h1s">Business ki baatein, <b class="aih">AI</b> ke saath.</h1><p class="sub">Practical articles: enquiry, follow-up, marketing aur payment ke aasaan tareeke.</p>\n<div class="bgrid">\n' + cards + '\n</div></div></main>';
}
export function buildSitemap(xml, ps, site) {
  xml = xml.replace(/<url>[\s\S]*?<\/url>/g, (m) => (/\/blog\/[^<]+<\/loc>/.test(m) ? '' : m));
  if (ps.length) xml = xml.replace('<loc>' + site + '/blog/</loc><lastmod>', '<loc>' + site + '/blog/</loc><lastmod>' + ps[0].date + '</lastmod><x>').replace(/<x>[^<]*<\/lastmod>/, '');
  return xml.replace('</urlset>', ps.map((p) => '<url><loc>' + site + '/blog/' + p.slug + '.html</loc><lastmod>' + p.date + '</lastmod></url>').join('') + '</urlset>');
}
function norm(b, allowData) {
  const p = { slug: String(b.slug || '').trim(), title: String(b.title || '').trim(), desc: String(b.desc || '').trim(), cat: CATS.includes(b.cat) ? b.cat : 'AI',
    date: /^\d{4}-\d{2}-\d{2}$/.test(b.date) ? b.date : new Date().toISOString().slice(0, 10), html: clean(b.html, allowData), cover: String(b.cover || ''), coverAlt: String(b.coverAlt || '').slice(0, 200),
    layout: LAYOUTS.includes(b.layout) ? b.layout : 'classic', cta: b.cta !== false, author: String(b.author || 'autenflo').slice(0, 60), seoTitle: String(b.seoTitle || '').slice(0, 120) };
  if (!allowData) {
    if (!/^[a-z0-9-]{1,80}$/.test(p.slug)) throw new Error('Slug me sirf a-z, 0-9 aur - chalega.');
    if (!p.title || !p.desc || !p.html.trim()) throw new Error('Title, meta description aur article, sab bharna zaroori hai.');
    if (/src\s*=\s*["']data:/i.test(String(b.html || '')) || p.cover.startsWith('data:')) throw new Error('Image abhi upload nahi hui. Dobara Publish dabaiye.');
    if (p.cover && !/^\/blog\/images\/[a-z0-9._-]+$/i.test(p.cover)) throw new Error('Cover image ka path galat hai.');
  }
  return p;
}
const pageTitle = (p) => p.seoTitle || p.title + ' | autenflo';
function postPage(head, tail, p, S) {
  const url = S + '/blog/' + p.slug + '.html', img = p.cover ? S + p.cover : S + '/logo.png';
  return setHead(head, { title: pageTitle(p), desc: p.desc, url, type: 'article', image: img, ld: [
    { '@context': 'https://schema.org', '@type': 'BlogPosting', headline: p.title, description: p.desc, image: img, datePublished: p.date, dateModified: new Date().toISOString().slice(0, 10), mainEntityOfPage: url, author: { '@type': 'Organization', name: p.author || 'autenflo' }, publisher: { '@type': 'Organization', name: 'autenflo', logo: { '@type': 'ImageObject', url: S + '/logo.png' } } },
    { '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement: [{ '@type': 'ListItem', position: 1, name: 'Home', item: S + '/' }, { '@type': 'ListItem', position: 2, name: 'Blog', item: S + '/blog/' }, { '@type': 'ListItem', position: 3, name: p.title, item: url }] }] }) + postMain(p) + tail;
}
const indexPage = (head, tail, ps, S) => setHead(head, { title: 'autenflo Blog | Business, AI, marketing aur social media', desc: 'Chhote aur beech wale business ke liye AI, marketing, sales aur payment ke practical tareeke.', url: S + '/blog/', type: 'website', image: S + '/logo.png', ld: [{ '@context': 'https://schema.org', '@type': 'Blog', name: 'autenflo Blog', url: S + '/blog/' }] }) + indexMain(ps) + tail;
const splitShell = (s) => { const i = s.indexOf('<main'), j = s.indexOf('</main>') + 7; if (i < 0 || j < 7) throw new Error('blog/index.html me <main> nahi mila.'); return [s.slice(0, i), s.slice(j)]; };
const loadPosts = async () => { const t = await getRaw('blog/posts.json'); const a = t ? JSON.parse(t) : []; return a.sort((x, y) => y.date.localeCompare(x.date)); };
const summ = (p) => ({ slug: p.slug, title: p.title, cat: p.cat, date: p.date, cover: p.cover || '' });
const okImages = (imgs) => (imgs || []).filter((i) => /^blog\/images\/[a-z0-9._-]+$/i.test(i.path) && typeof i.b64 === 'string' && i.b64.length < 4_000_000);

// ---------- actions ----------
const missing = () => ['GITHUB_TOKEN', 'GITHUB_REPO', 'SESSION_SECRET', 'SETUP_KEY'].filter((k) => !E[k]);
export async function act(a, b, user) {
  const S = SITE();
  if (a === 'status') { const u = await getUsers(); return { setup: u.length === 0, missing: missing() }; }
  if (a === 'setup') {
    const u = await getUsers(); if (u.length) throw new Error('Account pehle se bana hua hai.');
    if (!E.SETUP_KEY || b.key !== E.SETUP_KEY) throw new Error('Setup key galat hai.');
    if (!validUser(b.username) || String(b.password || '').length < 8) throw new Error('Username 3+ characters aur password kam se kam 8 characters ka rakhiye.');
    await putUsers([mkUser(b.username, b.password)]); return { token: token(b.username), user: b.username };
  }
  if (a === 'login') {
    const usr = (await getUsers()).find((x) => x.u.toLowerCase() === String(b.username || '').toLowerCase());
    if (!usr || !okPw(usr, String(b.password || ''))) { await sleep(900); throw new Error('Username ya password galat hai.'); }
    return { token: token(usr.u), user: usr.u };
  }
  if (!user) { const e = new Error('Login zaroori hai.'); e.status = 401; throw e; }
  if (a === 'me') return { user };
  if (a === 'users') return { users: (await getUsers()).map((x) => ({ u: x.u, created: x.created })) };
  if (a === 'adduser') {
    const us = await getUsers(); if (!validUser(b.username) || String(b.password || '').length < 8) throw new Error('Username 3+ characters aur password kam se kam 8 characters ka rakhiye.');
    if (us.some((x) => x.u.toLowerCase() === b.username.toLowerCase())) throw new Error('Ye username pehle se hai.');
    us.push(mkUser(b.username, b.password)); await putUsers(us); return { ok: true };
  }
  if (a === 'deluser') { const us = await getUsers(); if (b.username === user) throw new Error('Apna account khud delete nahi ho sakta.'); await putUsers(us.filter((x) => x.u !== b.username)); return { ok: true }; }
  if (a === 'passwd') {
    const us = await getUsers(), me = us.find((x) => x.u === user); if (!okPw(me, String(b.old || ''))) throw new Error('Purana password galat hai.');
    if (String(b.password || '').length < 8) throw new Error('Naya password kam se kam 8 characters ka rakhiye.'); Object.assign(me, mkUser(user, b.password)); await putUsers(us); return { ok: true };
  }
  if (missing().length) throw new Error('Netlify me ye settings baaki hain: ' + missing().join(', '));
  if (a === 'list') { const [ps, d] = await Promise.all([loadPosts(), getDrafts()]); return { posts: ps.map(summ), drafts: Object.values(d).map((x) => ({ ...summ(x), slug: x.slug || '', title: x.title || '' })) }; }
  if (a === 'get') {
    if (b.kind === 'draft') { const d = await getDrafts(); if (!d[b.slug]) throw new Error('Draft nahi mila.'); return { post: d[b.slug] }; }
    const p = (await loadPosts()).find((x) => x.slug === b.slug); if (!p) throw new Error('Post nahi mila.'); return { post: p };
  }
  if (a === 'savedraft') {
    const p = b.post || {}; const key = (p.slug || '').trim() || 'draft-' + Date.now(); const d = await getDrafts();
    d[key] = { ...p, slug: key, savedBy: user, savedAt: new Date().toISOString() }; await putDrafts(d); return { slug: key };
  }
  if (a === 'deldraft') { const d = await getDrafts(); delete d[b.slug]; await putDrafts(d); return { ok: true }; }
  if (a === 'preview') {
    const p = norm(b.post || {}, true); p.slug = p.slug || 'preview'; const shell = await getRaw('blog/index.html'); if (!shell) throw new Error('blog/index.html repo me nahi mila.');
    const [head, tail] = splitShell(shell); return { html: postPage(head, tail, p, S).replace('<head>', '<head><base href="' + S + '/">') };
  }
  if (a === 'publish') {
    const p = norm(b.post || {}, false), ps = await loadPosts(), isNew = !ps.some((x) => x.slug === p.slug);
    if (isNew && b.isNew === false) throw new Error('Ye post pehle se nahi mila.'); if (isNew === false && b.isNew === true) throw new Error('Is slug ka post pehle se hai. Slug badliye.');
    const shell = await getRaw('blog/index.html'); if (!shell) throw new Error('blog/index.html repo me nahi mila.'); const [head, tail] = splitShell(shell);
    const np = ps.filter((x) => x.slug !== p.slug).concat([p]).sort((x, y) => y.date.localeCompare(x.date));
    const sm = await getRaw('sitemap.xml'), files = [{ path: 'blog/' + p.slug + '.html', content: postPage(head, tail, p, S) }, { path: 'blog/index.html', content: indexPage(head, tail, np, S) }, { path: 'blog/posts.json', content: JSON.stringify(np, null, 1) }];
    if (sm) files.push({ path: 'sitemap.xml', content: buildSitemap(sm, np, S) });
    await commit(files, okImages(b.images), 'Blog: ' + (isNew ? 'publish ' : 'update ') + p.title + ' (' + user + ')');
    const d = await getDrafts(); if (d[p.slug] || b.draftKey) { delete d[p.slug]; if (b.draftKey) delete d[b.draftKey]; await putDrafts(d); }
    return { ok: true, url: S + '/blog/' + p.slug + '.html' };
  }
  if (a === 'delete') {
    const ps = await loadPosts(), np = ps.filter((x) => x.slug !== b.slug); const shell = await getRaw('blog/index.html'), [head, tail] = splitShell(shell), sm = await getRaw('sitemap.xml');
    const files = [{ path: 'blog/' + b.slug + '.html', content: null }, { path: 'blog/index.html', content: indexPage(head, tail, np, S) }, { path: 'blog/posts.json', content: JSON.stringify(np, null, 1) }];
    if (sm) files.push({ path: 'sitemap.xml', content: buildSitemap(sm, np, S) }); await commit(files, [], 'Blog: delete ' + b.slug + ' (' + user + ')'); return { ok: true };
  }
  throw new Error('Unknown action');
}

export default async (req) => {
  if (req.method !== 'POST') return json({ error: 'POST only' }, 405);
  try {
    const body = await req.json(); const auth = (req.headers.get('authorization') || '').replace(/^Bearer\s+/i, ''); const p = auth ? verify(auth) : null;
    return json(await act(body.action, body, p && p.u));
  } catch (e) { return json({ error: e.message || 'Error' }, e.status || 400); }
};
export const config = { path: '/api/admin' };
