#!/usr/bin/env python3
"""autenflo: plain HTML site generator.
Chalane ke liye:  python3 build_site.py   (output: ./autenflo-site/)
Shehron ki list cities.json me hai. Naya shehar jodna ho to wahan ek entry badhao aur dobara chalao.
"""
import json, os, re, shutil, urllib.parse as U
from html import escape as E

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'autenflo-site')
R = lambda n: open(os.path.join(HERE, n), encoding='utf-8').read()
data = json.load(open(os.path.join(HERE, 'cities.json'), encoding='utf-8'))
states, cities = data['states'], data['cities']
SITE = 'https://autenflo.com'
TODAY = '2026-11-10'
AI = '<b class="aih">AI</b>'
WA = lambda t: 'https://wa.me/918849031907?text=' + U.quote(t)
WI = '<svg class="wi" viewBox="0 0 24 24" aria-hidden="true"><use href="#wa"></use></svg>'
SPRITE, BG, LEARN = R('sprite.html'), R('bg.html'), R('learn.svg')
STATE_NAME = {'bihar': 'Bihar', 'uttar-pradesh': 'Uttar Pradesh', 'jharkhand': 'Jharkhand'}

def write(path, s):
    p = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(s)

LINKS = [('/#aapka', 'Businesses'), ('/#plans', 'Pricing'), ('/cities/', 'Cities'), ('/blog/', 'Blog'), ('/ai-training/', 'AI Training')]
HEADER = ('<header><div class="wrap"><a href="/" aria-label="autenflo home"><img src="/logo.png" alt="autenflo"></a><nav>'
          + ''.join(f'<a class="ul" href="{h}">{t}</a>' for h, t in LINKS)
          + f'<a class="btn wab mag" href="{WA("Namaste autenflo, mujhe apne business ko AI ki power chahiye")}">{WI}WhatsApp</a></nav>'
          '<details class="mnav"><summary aria-label="Menu"><span></span><span></span><span></span></summary><div class="mp">'
          + ''.join(f'<a href="{h}">{t}</a>' for h, t in LINKS) + '</div></details></div></header>')
def _footer():
    wa = WA("Namaste autenflo, mujhe apne business ko AI ki power chahiye")
    top = {}
    for c in cities: top.setdefault(c['state'], []).append(c)
    cols = ''
    for k in states:
        cols += f'<div class="fc"><h4>{STATE_NAME[k]}</h4><ul>' + ''.join(f'<li><a href="/{k}/{c["slug"]}/">{E(c["name"])}</a></li>' for c in top[k][:6]) + f'<li><a class="all" href="/{k}/">Sabhi cities dekhein →</a></li></ul></div>'
    return ('<footer class="ft"><div class="wrap">'
      '<div class="fcta glass"><div><h3>Apne business ko AI ki power dein.</h3><p>15 minute ki free baat. Koi pitch nahi, koi dabaav nahi.</p></div>'
      f'<a class="btn wab mag" href="{wa}">{WI}WhatsApp par baat karein</a></div>'
      '<div class="fgrid">'
      '<div class="fb0"><img src="/logo.png" alt="autenflo"><p>autenflo aapke business ko AI ki power deta hai: enquiry ka reply, follow-up, marketing aur payment, sab WhatsApp par, 24x7.</p>'
      f'<div class="fct"><a class="ul" href="mailto:hello@autenflo.com">hello@autenflo.com</a><a class="ul" href="{wa}">WhatsApp: +91 88490 31907</a></div></div>'
      '<div class="fc"><h4>Quick links</h4><ul><li><a href="/">Home</a></li><li><a href="/#aapka">Businesses</a></li><li><a href="/#plans">Pricing</a></li><li><a href="/#results">Results</a></li><li><a href="/#faq">FAQ</a></li><li><a href="/#sampark">Contact</a></li></ul></div>'
      '<div class="fc"><h4>Explore</h4><ul><li><a href="/blog/">Blog</a></li><li><a href="/ai-training/">AI Training for Institutions</a></li><li><a href="/cities/">Sabhi Cities</a></li></ul></div>'
      + cols + '</div>'
      '<div class="fbot"><p>© <span id="yr">2026</span> autenflo. Sabhi adhikar surakshit.</p><p>Bihar · Uttar Pradesh · Jharkhand ke businesses ke liye ❤️ se banaya</p><a class="ul" href="#top">Upar jaayein ↑</a></div>'
      '</div></footer>')
FOOTER = _footer()
FAB = f'<a class="fab" href="{WA("Namaste autenflo, mujhe apne business ko AI ki power chahiye")}" aria-label="WhatsApp par baat karein">{WI}</a>'

def page(path, title, desc, main, jsonld=(), extra_js=(), og='website'):
    url = SITE + '/' + path.replace('index.html', '').lstrip('/')
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jsonld)
    js = ''.join(f'<script src="{s}"></script>' for s in ('/assets/site.js', *extra_js))
    html = (f'<!doctype html>\n<html lang="hi-IN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{E(title)}</title><meta name="description" content="{E(desc, quote=True)}"><link rel="canonical" href="{url}"><link rel="icon" href="/logo.png">'
            f'<meta name="theme-color" content="#8a62d6"><meta property="og:type" content="{og}"><meta property="og:site_name" content="autenflo"><meta property="og:title" content="{E(title, quote=True)}">'
            f'<meta property="og:description" content="{E(desc, quote=True)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/logo.png">'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Mukta:wght@400;600;700&family=Outfit:wght@200..900&display=swap" rel="stylesheet">'
            f'<link rel="stylesheet" href="/assets/style.css">{ld}<noscript><style>#pre{{display:none}}</style></noscript>'
            '<script async src="https://www.googletagmanager.com/gtag/js?id=G-6012ZHG9SS"></script>'
            "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-6012ZHG9SS');</script></head>\n"
            f'<body>{SPRITE}<div id="pre"><img src="/logo.png" alt="autenflo"><i></i></div><div class="pbar"></div>{BG}'
            '<a class="ann" href="/#plans">🎁 Bihar ke Startups ke liye: har plan ke saath <b>FREE Branding Consulting</b> →</a>'
            f'{HEADER}\n{main}\n{FOOTER}{FAB}{js}</body></html>')
    depth = path.count('/')
    pre = '../' * depth
    def _rel(m):
        t = m.group(2)
        if t.startswith('//'): return m.group(0)
        if t == '/': t = 'index.html'
        elif t.startswith('/#'): t = 'index.html' + t[1:]
        else:
            t = t[1:]
            hs = t.split('#', 1)
            if hs[0].endswith('/'): hs[0] += 'index.html'
            t = '#'.join(hs)
        return f'{m.group(1)}"{pre}{t}"'
    html = re.sub(r'((?:href|src)=)"(/[^"]*)"', _rel, html)
    write(path, html)
    return url

def hero_art(a, b, label):
    return (f'<svg class="art" viewBox="0 0 800 360" role="img" aria-label="{label}" style="--a:{a};--b:{b}" xmlns="http://www.w3.org/2000/svg">'
        '<rect class="fa" width="800" height="360" rx="28" opacity=".14"/><rect class="fb" width="800" height="200" rx="28" opacity=".1"/><circle class="fb" cx="690" cy="60" r="40" opacity=".5"/>'
        '<rect x="90" y="36" width="190" height="288" rx="30" fill="#17202A" opacity=".88"/><rect x="102" y="56" width="166" height="248" rx="18" fill="#fff"/>'
        '<rect class="fb" x="116" y="80" width="104" height="30" rx="15" opacity=".35"/><rect class="fa" x="150" y="124" width="108" height="30" rx="15"/>'
        '<rect class="fb" x="116" y="168" width="88" height="30" rx="15" opacity=".35"/><rect class="fa" x="134" y="212" width="124" height="30" rx="15"/>'
        '<rect class="fb" x="116" y="256" width="70" height="28" rx="14" opacity=".35"/>'
        '<path class="sb" fill="none" stroke-width="5" stroke-dasharray="3 10" stroke-linecap="round" d="M284 180h60M452 180h60"/>'
        '<rect class="fa" x="344" y="124" width="108" height="108" rx="28"/><text x="398" y="200" text-anchor="middle" font-family="Outfit,sans-serif" font-weight="800" font-size="46" fill="#fff">AI</text>'
        '<rect x="512" y="40" width="200" height="110" rx="20" fill="#fff"/><rect class="fb" x="528" y="58" width="60" height="12" rx="6" opacity=".6"/>'
        '<g class="fa"><rect x="530" y="108" width="24" height="26" rx="5" opacity=".5"/><rect x="566" y="94" width="24" height="40" rx="5" opacity=".7"/><rect x="602" y="80" width="24" height="54" rx="5"/><rect x="638" y="68" width="24" height="66" rx="5"/></g>'
        '<rect x="512" y="176" width="200" height="130" rx="20" fill="#fff"/><rect class="fb" x="528" y="194" width="70" height="12" rx="6" opacity=".6"/>'
        '<g fill="none" stroke="#17202A" stroke-width="2" opacity=".18"><path d="M528 226h168M528 250h168M528 274h168"/></g>'
        '<circle class="fa" cx="546" cy="226" r="7"/><circle class="fb" cx="546" cy="250" r="7"/><circle class="fa" cx="546" cy="274" r="7" opacity=".6"/>'
        '<rect class="fa" x="566" y="222" width="90" height="8" rx="4" opacity=".4"/><rect class="fb" x="566" y="246" width="116" height="8" rx="4" opacity=".4"/><rect class="fa" x="566" y="270" width="72" height="8" rx="4" opacity=".4"/>'
        '<g class="fg"><path d="M330 60l5 12 12 5-12 5-5 12-5-12-12-5 12-5Z"/><path d="M470 300l4 9 9 4-9 4-4 9-4-9-9-4 9-4Z"/></g>'
        '<rect class="fa" y="320" width="800" height="40" opacity=".18"/></svg>')

PROBLEMS = [
    ('💬', 'Enquiry ka reply late jata hai', 'WhatsApp, call aur Instagram ki har enquiry ka turant reply, 24x7.'),
    ('🔥', 'Hot leads ka follow-up chhoot jata hai', '1, 3 aur 7 din par auto follow-up, aur hot lead par seedha alert.'),
    ('📣', 'Marketing aur social media regular nahi', 'Posts, posters aur videos ka calendar, aur Instagram, Facebook, YouTube par auto-post.'),
    ('🧾', 'Payment aur hisaab bikhra rehta hai', 'Payment reminder, bill ki photo se entry aur invoice.'),
    ('⚙️', 'Manual kaam me time jata hai', 'Order, sheet, task aur report ka roz ka kaam AI se.'),
]
STEPS = [('Aap WhatsApp par baat karte ho', 'Business, team aur roz ke kaam ke baare me batate ho.'), ('Hum setup karte hain', 'WhatsApp agent, follow-up, content calendar aur reminders, sab online.'), ('AI kaam karta hai, aap deal close karte ho', 'Har mahine ek simple report aur zaroorat par tuning.')]
BIZ = ['Coaching & Tuition', 'Clinics & Hospitals', 'Real Estate', 'Garments & Jewellery', 'Mobile & Electronics', 'Hardware & Building Material', 'Car, Bike & Service Centre', 'Restaurants, Sweets & Catering', 'Travel, Tours & Hotels', 'Wholesalers & Distributors', 'Salons, Gyms & Wellness', 'CA, Insurance & Legal', 'Makhana, Litchi & Local Brands', 'Schools & Institutes']
PLANS = [
    ('Launch', 'For Startups', '9,999', '2,999', ['🌐 Free Website Revamp', f'🎓 3 Days {AI} Training to Staff @ ₹999', '📱 Free Social Media Starter Package']),
    ('Accelerate', 'For Growing Businesses', '19,999', '5,999', ['🌐 Free Website', f'🎓 Free {AI} Training to Staff', '📱 Free Social Media Package']),
    ('Titan', 'For Established Businesses', '29,999', '9,999', ['🌐 Free Website', f'🎓 Free {AI} Training to Staff', '📱 Free Social Media Package']),
]

def faq_list(n):
    return [
        (f'autenflo {n} ke business ke liye kya karta hai?', f'autenflo {n} ke business ko AI ki power deta hai: enquiry ka turant reply, hot leads ka follow-up, marketing aur social media posts aur videos, payment reminder aur hisaab me madad. Ye sab WhatsApp par chalta hai, 24x7.'),
        (f'Kya {n} me setup ke liye office aana padta hai?', 'Nahi. Poora setup online hota hai. Aap WhatsApp par baat shuru karte ho, baaki kaam hum sambhalte hain.'),
        ('Shuruaat kitne se hoti hai?', 'Launch plan ki one-time installation ₹9,999 aur monthly charge ₹2,999 se shuru hota hai. WhatsApp API platform, Meta aur AI usage ka kharcha aapke apne account se jata hai.'),
        ('Kya customer se Hindi me baat hoti hai?', 'Haan, Hindi me aur zaroorat par English me. Jahan insaan ki zaroorat ho, wahan baat seedha aap ya aapke staff tak pahunch jaati hai.'),
    ]

def city_page(c):
    n, st = c['name'], c['state']; s = states[st]; sn = STATE_NAME[st]
    url = f'{SITE}/{st}/{c["slug"]}/'
    msg = WA(f'Namaste autenflo, main {n} se hu. Mujhe apne business ko AI ki power chahiye.')
    near = [x for x in cities if x['state'] == st and x['slug'] != c['slug']][:4]
    faq = faq_list(n)
    offer = ('<div class="offer glass"><span class="gi">🎁</span><div><b>Bihar ke Startups ke liye khaas offer</b><p>Har plan ke saath <strong>FREE Branding Consulting</strong>: aapka brand, positioning aur pehchaan, shuru se sahi.</p></div></div>' if st == 'bihar' else '')
    prob = ''.join(f'<article class="glass bz"><span class="em">{e}</span><h3>{t}</h3><p class="fx1">{d}</p></article>' for e, t, d in PROBLEMS)
    steps = ''.join(f'<div class="st on"><span class="dot">{i}</span><div><h3>{h}</h3><p>{p}</p></div></div>' for i, (h, p) in enumerate(STEPS, 1))
    plans = ''.join('<article class="glass pad pl"><h3>%s</h3><p class="for">%s</p><p><small>One-time installation</small><br><strong>₹%s</strong></p><p><small>Har mahine</small><br><strong>₹%s</strong></p><ul class="fr">%s</ul></article>' % (a, b, c1, d, ''.join(f'<li>{x}</li>' for x in fr)) for a, b, c1, d, fr in PLANS)
    main = f'''<main id="top"><section class="chero"><div class="wrap"><p class="crumbs"><a href="/">Home</a> / <a href="/cities/">Shehar</a> / <a href="/{st}/">{sn}</a> / {n}</p><div class="chg"><div><span class="eyebrow">{n} · {sn}</span><h1 class="h1s">{n} ke business ko {AI} ki power.</h1><p class="lead">{n} ke business ke liye: enquiry ka reply, hot leads ka follow-up, marketing aur social media posts aur videos, payment reminder aur hisaab. Sab {AI} se, 24x7.</p><div class="cta"><a class="btn wab mag" href="{msg}">{WI}{n} ke liye baat karein</a><a class="btn ghost mag" href="#plans">Pricing dekhein</a></div></div>{hero_art(s['a'], s['b'], 'autenflo AI ka business setup')}</div></div></section>
<section class="sec"><div class="wrap"><span class="eyebrow">Sach bataiye</span><h2 class="wide">Har business me paanch jagah paisa chupchap leak hota hai.</h2><div class="g3">{prob}</div></div></section>
<section class="sec"><div class="wrap"><span class="eyebrow">Kaise shuru hota hai</span><h2>Teen kadam. Phir {AI} kaam sambhalta hai.</h2><div class="tl">{steps}<div class="line"><i style="transform:none"></i></div></div></div></section>
<section class="sec" id="plans"><div class="wrap"><span class="eyebrow">Pricing</span><h2 class="wide">Ek baar installation, phir chhota monthly charge.</h2>{offer}<div class="g3">{plans}</div><p class="note c">WhatsApp API platform (WATI, Interakt jaise), Meta ke message charges aur AI usage ka kharcha aapke apne account se jata hai. <a class="ul" href="/#plans">Poori details dekhein</a></p></div></section>
<section class="sec"><div class="wrap"><span class="eyebrow">Kiske liye</span><h2 class="wide">Har tarah ke business ke liye.</h2><div class="chips">{''.join(f'<span>{b}</span>' for b in BIZ)}</div></div></section>
<section class="sec fq"><div class="wrap"><span class="eyebrow">Mann me jo sawal hain</span><h2>Pehle ye jaan lijiye</h2>{''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq)}</div></section>
<section class="sec"><div class="wrap"><div class="glass fin2"><div><h2>{n} ke apne business me {AI} lagayein.</h2><p class="sub">WhatsApp par batayiye aapka business kya hai, hum bataenge shuruaat kahan se karein.</p></div><a class="btn wab mag" href="{msg}">{WI}WhatsApp par abhi baat karein</a></div><h3 class="mt2">{sn} ke aur shehar</h3><div class="cgrid">{''.join(f'<a class="cc glass" href="/{x["state"]}/{x["slug"]}/"><div><h3>{x["name"]}</h3><p>Business ke liye AI ki power</p></div></a>' for x in near)}</div></div></section></main>'''
    ld = [{'@context': 'https://schema.org', '@type': 'WebPage', 'name': f'{n} ke business ke liye AI | autenflo', 'url': url},
          {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
              {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'}, {'@type': 'ListItem', 'position': 2, 'name': sn, 'item': f'{SITE}/{st}/'}, {'@type': 'ListItem', 'position': 3, 'name': n, 'item': url}]},
          {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]}]
    page(f'{st}/{c["slug"]}/index.html', f'{n} ke business ke liye AI ki power | autenflo',
         f'{n} ke business ke liye autenflo: enquiry ka reply, hot leads ka follow-up, marketing, social media aur payment reminder, sab AI se. Installation ₹9,999 se.', main, ld)
    return url

from city_data import CITY

def city_page(c):
    n, st = c['name'], c['state']; s = states[st]; sn = STATE_NAME[st]; d = CITY[c['slug']]
    url = f'{SITE}/{st}/{c["slug"]}/'
    msg = WA(f'Namaste autenflo, main {n} se hu. Mujhe apne business ko AI ki power chahiye.')
    near = [x for x in cities if x['state'] == st and x['slug'] != c['slug']][:4]
    faq = [d['faq'], faq_list(n)[2]]
    t1, t2 = d['biz'][0][0], d['biz'][1][0]
    offer = ('<div class="offer glass"><span class="gi">🎁</span><div><b>Bihar ke Startups ke liye khaas offer</b><p>Har plan ke saath <strong>FREE Branding Consulting</strong>.</p></div></div>' if st == 'bihar' else '')
    cards = ''.join(f'<article class="glass bz"><span class="em">{e}</span><h3>{E(t)}</h3><p class="fx1"><b>Problem:</b> {E(l)}</p><p class="fx1"><b>autenflo:</b> {E(f)}</p></article>' for (t, l, f), e in zip(d['biz'], ('🏪', '📲', '🧾')))
    chat = f'<div class="chat"><div class="cb c">{E(d["chat"][0])}</div><div class="cb b">{E(d["chat"][1])}</div></div>'
    areas = ''.join(f'<span>{E(a)}</span>' for a in d['areas'])
    main = f"""<main id="top"><section class="chero"><div class="wrap"><p class="crumbs"><a href="/">Home</a> / <a href="/cities/">Shehar</a> / <a href="/{st}/">{sn}</a> / {n}</p><div class="chg"><div><span class="eyebrow">{n} · {sn}</span><h1 class="h1s">{n} ke business ko {AI} ki power.</h1><p class="lead">{E(d['hook'])}</p><div class="cta"><a class="btn wab mag" href="{msg}">{WI}{n} ke liye baat karein</a><a class="btn ghost mag" href="#plans">Pricing dekhein</a></div></div>{hero_art(s['a'], s['b'], 'autenflo AI ka business setup')}</div></div></section>
<section class="sec"><div class="wrap"><span class="eyebrow">{n} ke business</span><h2 class="wide">{n} me paisa yahan leak hota hai.</h2><div class="g3">{cards}</div></div></section>
<section class="sec"><div class="wrap"><span class="eyebrow">{n} ka business calendar</span><h2 class="wide">Kab {AI} ON karna sabse zyada kaam aata hai.</h2><p class="sub">{E(d['season'])}</p><h3 class="mt2">{n} me ek asli WhatsApp baatcheet</h3>{chat}</div></section>
<section class="sec"><div class="wrap"><span class="eyebrow">Hum kahan kaam karte hain</span><h2 class="wide">{n} ke in ilaakon ke business ke liye.</h2><div class="chips">{areas}</div></div></section>
<section class="sec" id="plans"><div class="wrap">{offer}<div class="glass fin2"><div><h2>Launch plan ₹9,999 se, monthly ₹2,999.</h2><p class="sub">WhatsApp API, Meta aur AI usage ka kharcha aapke apne account se jata hai. <a class="ul" href="/#plans">Poori pricing dekhein</a></p></div><a class="btn wab mag" href="{msg}">{WI}WhatsApp par abhi baat karein</a></div></div></section>
<section class="sec fq"><div class="wrap"><span class="eyebrow">Mann me jo sawal hain</span><h2>Pehle ye jaan lijiye</h2>{''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq)}</div></section>
<section class="sec"><div class="wrap"><h3 class="mt2">{sn} ke aur shehar</h3><div class="cgrid">{''.join(f'<a class="cc glass" href="/{x["state"]}/{x["slug"]}/"><div><h3>{x["name"]}</h3><p>{E(CITY[x["slug"]]["biz"][0][0])}</p></div></a>' for x in near)}</div></div></section></main>"""
    ld = [{'@context': 'https://schema.org', '@type': 'WebPage', 'name': f'{n} me {t1} aur {t2} ke liye AI | autenflo', 'url': url},
          {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
              {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'}, {'@type': 'ListItem', 'position': 2, 'name': sn, 'item': f'{SITE}/{st}/'}, {'@type': 'ListItem', 'position': 3, 'name': n, 'item': url}]},
          {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]}]
    page(f'{st}/{c["slug"]}/index.html', f'{n} me {t1} aur {t2} ke liye AI WhatsApp automation | autenflo',
         f'{n}: {d["hook"]} {t1}, {t2} aur dusre business ke liye autenflo. Installation ₹9,999 se.', main, ld)
    return url

def hub_page(st):
    s = states[st]; sn = STATE_NAME[st]; lst = [x for x in cities if x['state'] == st]
    grid = ''.join(f'<a class="cc glass" href="/{x["state"]}/{x["slug"]}/"><div><h3>{x["name"]}</h3><p>Business ke liye AI ki power</p></div></a>' for x in lst)
    main = f'''<main id="top"><section class="chero"><div class="wrap"><p class="crumbs"><a href="/">Home</a> / <a href="/cities/">Shehar</a> / {sn}</p><div class="chg"><div><span class="eyebrow">{sn}</span><h1 class="h1s">{sn} ke business ko {AI} ki power.</h1><p class="lead">{sn} ke {len(lst)} bade shehron me autenflo ka {AI} setup: enquiry ka reply, follow-up, marketing aur payment reminder.</p></div>{hero_art(s['a'], s['b'], 'autenflo AI')}</div><div class="cgrid">{grid}</div></div></section></main>'''
    return page(f'{st}/index.html', f'{sn} ke shehron me business ke liye AI | autenflo', f'{sn} ke {len(lst)} bade shehron ke business ke liye autenflo ka AI setup.', main)

def cities_index():
    blocks = ''.join(f'<div class="wrap stsec"><h2><a href="/{k}/">{STATE_NAME[k]}</a></h2><div class="cgrid">' + ''.join(f'<a class="cc glass" href="/{x["state"]}/{x["slug"]}/"><div><h3>{x["name"]}</h3><p>Business ke liye AI ki power</p></div></a>' for x in cities if x['state'] == k) + '</div></div>' for k in states)
    main = f'<main id="top" class="sec"><div class="wrap"><p class="crumbs"><a href="/">Home</a> / Shehar</p><span class="eyebrow">Aapka shehar</span><h1 class="h1s">Aapka shehar. Aapka business. {AI} ki power.</h1><p class="sub">Bihar, Purvanchal aur Jharkhand ke shehron me autenflo ka {AI} setup. Apna shehar chuniye.</p></div>{blocks}</main>'
    return page('cities/index.html', 'Bihar, Purvanchal aur Jharkhand ke 21 shehron me business ke liye AI | autenflo', 'Bihar, Lucknow se Purvanchal aur Jharkhand ke 21 shehron me business ke liye autenflo ka AI setup.', main)

# ---------- blog ----------
BLOG_ART = ('<svg viewBox="0 0 400 220" role="img" aria-label="AI" xmlns="http://www.w3.org/2000/svg"><rect width="400" height="220" fill="#3b7fd4"/><circle cx="350" cy="30" r="90" fill="#8a62d6" opacity=".45"/><circle cx="30" cy="210" r="70" fill="#8a62d6" opacity=".3"/>'
            '<g stroke="#fff" stroke-width="3" opacity=".7"><path d="M120 110L200 70L280 120L200 160ZM200 70V160M120 110L280 120"/></g><g fill="#fff"><circle cx="120" cy="110" r="10"/><circle cx="200" cy="70" r="12"/><circle cx="280" cy="120" r="10"/><circle cx="200" cy="160" r="10"/></g>'
            '<rect x="160" y="100" width="80" height="44" rx="12" fill="#17202A" opacity=".75"/><text x="200" y="131" text-anchor="middle" font-family="Outfit,sans-serif" font-weight="800" font-size="24" fill="#fff">AI</text></svg>')
POST = {'slug': 'whatsapp-par-60-second-me-reply', 'title': 'WhatsApp par customer ko 60 second me reply kaise dein', 'cat': 'AI', 'date': '2026-11-10', 'dlabel': '10 November 2026',
        'desc': 'Enquiry aate hi reply dene se order kyun badhte hain, aur chhote business ye kaam bina naya staff rakhe kaise kar sakte hain.'}

def blog_pages():
    p = POST
    body = f'''<p>Jo customer pehle reply paata hai, wahi aksar order bhi de deta hai. Phir bhi zyada tar business me enquiry ka reply tab jata hai jab staff ko yaad aata hai.</p>
<h2>Reply late hone ki 3 wajah</h2>
<ol><li>Enquiry WhatsApp, call aur Instagram par bikhri hoti hai.</li><li>Wahi sawal roz poochhe jaate hain: price, timing, address.</li><li>Raat ko aur chhutti ke din koi reply dene wala nahi hota.</li></ol>
<h2>Ye kaam aap kaise sambhal sakte hain</h2>
<ul><li>Sabse zyada poochhe jaane wale 10 sawal aur unke jawab ek jagah likh lijiye.</li><li>Har enquiry ko ek sheet me darj kijiye, taaki koi chhoote nahi.</li><li><b>Hot leads</b> ko alag mark kijiye aur unka follow-up 1, 3 aur 7 din par rakhiye.</li><li>Jo kaam roz dohrata hai, use {AI} se karwaiye aur sirf zaroori baat apne paas rakhiye.</li></ul>
<blockquote>Har bhoola hua follow-up, ek bika hua order hai.</blockquote>
<p>Apne business me ye kahan se shuru karein, ye jaanne ke liye WhatsApp par hamse 15 minute baat kar sakte hain.</p>'''
    url = f'{SITE}/blog/{p["slug"]}.html'
    main = f'''<main id="top" class="sec"><div class="wrap"><p class="crumbs"><a href="/">Home</a> / <a href="/blog/">Blog</a></p>
<!-- ✏️ NAYA ARTICLE: is file ko copy karke naya naam do, phir title, description, date, category aur niche ka content badlo -->
<article><div class="post-head"><div><p class="meta">{p['cat']} · {p['dlabel']}</p><h1 class="h1s">{E(p['title'])}</h1><p class="sub">{E(p['desc'])}</p></div><div class="post-art">{BLOG_ART}</div></div>
<div class="prose">
<!-- ✏️ ARTICLE KI BODY YAHAN SE -->
{body}
<!-- ✏️ ARTICLE KI BODY YAHAN TAK -->
</div></article>
<div class="glass fin2"><div><h2>Apne business me {AI} lagayein.</h2><p class="sub">WhatsApp par 15 minute baat karke dekhiye aapke liye kya sahi rahega.</p></div><a class="btn wab mag" href="{WA('Namaste autenflo, maine aapka blog padha. Mujhe apne business ko AI ki power chahiye.')}">{WI}WhatsApp par baat karein</a></div></div></main>'''
    ld = [{'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': p['title'], 'description': p['desc'], 'datePublished': p['date'], 'mainEntityOfPage': url,
           'author': {'@type': 'Organization', 'name': 'autenflo'}, 'publisher': {'@type': 'Organization', 'name': 'autenflo', 'logo': {'@type': 'ImageObject', 'url': SITE + '/logo.png'}}}]
    page(f'blog/{p["slug"]}.html', f'{p["title"]} | autenflo', p['desc'], main, ld, og='article')
    card = f'<a class="bc glass" href="/blog/{p["slug"]}.html">{BLOG_ART}<div><p class="meta">{p["cat"]} · {p["dlabel"]}</p><h3>{E(p["title"])}</h3><p>{E(p["desc"])}</p></div></a>'
    main = f'''<main id="top" class="sec"><div class="wrap"><p class="crumbs"><a href="/">Home</a> / Blog</p><span class="eyebrow">Blog</span><h1 class="h1s">Business ki baatein, {AI} ke saath.</h1><p class="sub">Practical articles: enquiry, follow-up, marketing aur payment ke aasaan tareeke.</p>
<div class="bgrid">
<!-- ✏️ NAYA ARTICLE JODNE PAR: niche wala card copy karke upar (sabse pehle) paste karo aur uska link, title aur description badlo -->
{card}
</div></div></main>'''
    page('blog/index.html', 'autenflo Blog | Business, AI, marketing aur social media', 'Chhote aur beech wale business ke liye AI, marketing, sales aur payment ke practical tareeke.', main)
    return [url, SITE + '/blog/']

# ---------- home + training ----------
def home_training():
    home = R('home.html').replace('<div class="glass tz">', '<div class="glass tz"><div class="tzart">' + LEARN + '</div>')
    ld = [{'@context': 'https://schema.org', '@type': 'Organization', 'name': 'autenflo', 'url': SITE, 'logo': SITE + '/logo.png'}, {'@context': 'https://schema.org', '@type': 'WebSite', 'name': 'autenflo', 'url': SITE}]
    page('index.html', 'autenflo | Business aapka. AI ki power.', 'autenflo aapke business ko AI ki power deta hai: enquiry ka reply, hot leads ka follow-up, marketing, social media posts aur videos, payment reminder aur hisaab. Ek baar installation, phir chhota monthly charge.', home, ld, ('/assets/home.js',))
    tr = R('training.html').replace('<div class="hv">', '<div class="hv"><div class="tart">' + LEARN + '</div>')
    page('ai-training/index.html', 'AI Training for Schools, Colleges, ITIs and Institutions | autenflo', 'Daily 1 ghante ki live online AI class: Schools ₹6,999, Colleges ₹9,999, Others ₹8,999 per month. Workplaces, ITIs, private aur govt institutions ke liye.', tr,
         [{'@context': 'https://schema.org', '@type': 'Service', 'name': 'AI Training for Schools, Colleges and Institutions', 'provider': {'@type': 'Organization', 'name': 'autenflo', 'url': SITE}}])
    return [SITE + '/', SITE + '/ai-training/']

if __name__ == '__main__':
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT + '/assets')
    write('assets/style.css', R('global.css') + '\n' + R('extra.css') + '\n.chat{display:flex;flex-direction:column;gap:10px;max-width:480px}.cb{padding:12px 16px;border-radius:18px;font-weight:600;max-width:88%}.cb.c{background:#fff;color:#17202A;align-self:flex-start}.cb.b{background:#dcf8c6;color:#17202A;align-self:flex-end}\n.em{font-size:1.8rem;display:block;margin-bottom:8px}.fr{list-style:none;padding:0;margin:14px 0 0}.fr li{margin:6px 0;font-weight:600}.cc div{padding:22px 24px}\n')
    write('assets/site.js', 'function hidePre(){var p=document.getElementById("pre");if(p)p.style.display="none"}addEventListener("load",hidePre);setTimeout(hidePre,2500);var y=document.getElementById("yr");if(y)y.textContent=new Date().getFullYear();')
    write('assets/home.js', R('home.js'))
    urls = home_training() + blog_pages() + [cities_index()] + [hub_page(k) for k in states] + [city_page(c) for c in cities]
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>' for u in urls) + '</urlset>')
    write('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
    write('README.txt', 'logo.png naam se apna logo is folder ke root me (index.html ke saath) daalo.\n')
    print(len(urls), 'pages')
