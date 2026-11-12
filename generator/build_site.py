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
TODAY = '2026-11-12'
AI = '<b class="aih">AI</b>'
WA = lambda t: 'https://wa.me/918849031907?text=' + U.quote(t)
WI = '<svg class="wi" viewBox="0 0 24 24" aria-hidden="true"><use href="#wa"></use></svg>'
SPRITE, BG, LEARN = R('sprite.html'), R('bg.html'), R('learn.svg')
STATE_NAME = {'bihar': 'Bihar', 'uttar-pradesh': 'Uttar Pradesh', 'jharkhand': 'Jharkhand'}

# ---------- URL registry (SEO slugs): sirf yahin badlo, links/sitemap/canonical/redirects sab apne aap ----------
KW = 'ai-whatsapp-automation'
U_HOME = '/'
U_CITIES = f'/{KW}-bihar-up-jharkhand/'
U_TRAIN = '/ai-training-for-schools-and-colleges/'
U_ABOUT = '/about-autenflo/'
U_PRIVACY = '/privacy-policy/'
U_TERMS = '/terms-of-service/'
U_BLOG = '/blog/'
def u_state(st): return f'/{KW}-{st}/'
def u_city(slug): return f'/{KW}-{slug}/'
POST_SLUG = {
 'missed-enquiry-check-khud-kaise-karein': 'missed-whatsapp-enquiry-kaise-check-karein-7-din',
 'follow-up-1-3-7-din-ka-rule': 'customer-follow-up-1-3-7-din-rule-templates',
 'whatsapp-par-60-second-me-reply': 'whatsapp-par-customer-ko-60-second-me-reply-kaise-dein',
}
def u_post(old): return f'/blog/{POST_SLUG[old]}/'
def fp(url): return 'index.html' if url == '/' else url.strip('/') + '/index.html'

def crumbs_html(items):
    parts = [f'<a href="{u}">{E(n)}</a>' for n, u in items[:-1]] + [f'<span aria-current="page">{E(items[-1][0])}</span>']
    return '<p class="crumbs">' + ' / '.join(parts) + '</p>'
def crumbs_ld(items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i, 'name': n, 'item': SITE + u} for i, (n, u) in enumerate(items, 1)]}
ORG = {'@type': 'Organization', 'name': 'autenflo', 'url': SITE}

def write(path, s):
    p = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(s)

LINKS = [('/#aapka', 'Businesses'), ('/#plans', 'Pricing'), (U_CITIES, 'Cities'), (U_BLOG, 'Blog'), (U_ABOUT, 'About')]
HEADER = ('<header><div class="wrap"><a href="/" aria-label="autenflo home"><img src="/logo.png" alt="autenflo"></a><nav>'
          + ''.join(f'<a class="ul" href="{h}">{t}</a>' for h, t in LINKS)
          + f'<a class="btn wab mag" href="{WA("Namaste autenflo, mujhe free missed-enquiry check chahiye")}">{WI}WhatsApp</a></nav>'
          '<details class="mnav"><summary aria-label="Menu"><span></span><span></span><span></span></summary><div class="mp">'
          + ''.join(f'<a href="{h}">{t}</a>' for h, t in LINKS) + '</div></details></div></header>')
def _footer():
    wa = WA("Namaste autenflo, mujhe free missed-enquiry check chahiye")
    top = {}
    for c in cities: top.setdefault(c['state'], []).append(c)
    cols = ''
    for k in states:
        cols += f'<div class="fc"><h4>{STATE_NAME[k]}</h4><ul>' + ''.join(f'<li><a href="{u_city(c["slug"])}">{E(c["name"])}</a></li>' for c in top[k][:6]) + f'<li><a class="all" href="{u_state(k)}">Sabhi cities dekhein →</a></li></ul></div>'
    return ('<footer class="ft"><div class="wrap">'
      '<div class="fcta glass"><div><h3>Apne business ka free missed-enquiry check karwayein.</h3><p>15 minute. Pichhli 7 din ki enquiries gin kar batate hain kitni late ya miss hui. Koi pitch nahi, koi dabaav nahi.</p></div>'
      f'<a class="btn wab mag" href="{wa}">{WI}WhatsApp par baat karein</a></div>'
      '<div class="fgrid">'
      '<div class="fb0"><img src="/logo.png" alt="autenflo"><p>autenflo aapke business ka AI back-office hai: enquiry ka reply, follow-up, payment reminder aur marketing, sab WhatsApp par, 24x7. Patna, Bihar.</p>'
      f'<div class="fct"><a class="ul" href="mailto:hello@autenflo.com">hello@autenflo.com</a><a class="ul" href="{wa}">WhatsApp: +91 88490 31907</a></div></div>'
      '<div class="fc"><h4>Quick links</h4><ul><li><a href="/">Home</a></li><li><a href="/#aapka">Businesses</a></li><li><a href="/#plans">Pricing</a></li><li><a href="/#results">Hamara tareeka</a></li><li><a href="/#faq">FAQ</a></li><li><a href="/#sampark">Contact</a></li></ul></div>'
      f'<div class="fc"><h4>Explore</h4><ul><li><a href="{U_BLOG}">Blog</a></li><li><a href="{U_TRAIN}">AI Training for Institutions</a></li><li><a href="{U_CITIES}">Sabhi Cities</a></li><li><a href="{U_ABOUT}">About</a></li><li><a href="{U_PRIVACY}">Privacy Policy</a></li><li><a href="{U_TERMS}">Terms</a></li></ul></div>'
      + cols + '</div>'
      '<div class="fbot"><p>© <span id="yr">2026</span> autenflo. Sabhi adhikar surakshit.</p><p>Bihar · Uttar Pradesh · Jharkhand ke businesses ke liye ❤️ se banaya</p><a class="ul" href="#top">Upar jaayein ↑</a></div>'
      '</div></footer>')
FOOTER = _footer()
FAB = f'<a class="fab" href="{WA("Namaste autenflo, mujhe free missed-enquiry check chahiye")}" aria-label="WhatsApp par baat karein">{WI}</a>'

NOINDEX = set()

# ---------- SEO: title <= 60, description <= 155 characters ----------
# slug: (title me shehar ka naam, 2 chhote keyword, local line)
CITY_SEO = {
 'patna': ('Patna', 'Coaching, Clinics', 'Coaching, clinics, real estate: raat 11 baje bhi har enquiry ka reply.'),
 'muzaffarpur': ('Muzaffarpur', 'Litchi, Wholesale', 'Litchi season ke bulk order, rate aur dispatch ka kaam khud chale.'),
 'gaya': ('Gaya', 'Hotels, Travel', 'Pitru Paksha me hotel aur travel ki bheed ek saath sambhalen.'),
 'purnia': ('Purnia', 'Makhana, Clinics', 'Makhana traders aur clinics: gaon se aayi enquiry ka turant reply.'),
 'bhagalpur': ('Bhagalpur', 'Silk, Clinics', 'Silk wholesale ke order, rate, dispatch aur payment ka hisaab.'),
 'arrah': ('Arrah', 'Retail, Coaching', 'Retail dukaan aur coaching: lead ka reply aur follow-up, bina extra staff.'),
 'bihar-sharif': ('Bihar Sharif', 'Hardware, Coaching', 'Hardware dukaan aur coaching: quotation, payment aur stock ka kaam.'),
 'darbhanga': ('Darbhanga', 'Makhana, Clinics', 'Makhana traders aur clinics: order, appointment aur payment ka kaam.'),
 'lucknow': ('Lucknow', 'Clinics, Restaurants', 'Clinics, restaurants, events: jo pehle reply kare, customer usi ka.'),
 'varanasi': ('Varanasi', 'Hotels, Saree', 'Hotel, tours aur saree wholesale: enquiry se order tak, ek jagah.'),
 'prayagraj': ('Prayagraj', 'Coaching, Hotels', 'Exam coaching, hostel aur mela season ke hotel ka poora kaam.'),
 'gorakhpur': ('Gorakhpur', 'Clinics, Hotels', 'Clinics aur hotels: door se aaye customer ko turant reply.'),
 'ayodhya': ('Ayodhya', 'Hotels, Travel', 'Hotel, homestay aur cab: yatri boom me har enquiry sambhalen.'),
 'mirzapur': ('Mirzapur', 'Carpet, Hardware', 'Carpet aur hardware vyapari: catalogue, rate, dispatch aur payment.'),
 'jaunpur': ('Jaunpur', 'Coaching, Garments', 'Coaching admission aur garment dukaan: reply se payment tak.'),
 'azamgarh': ('Azamgarh', 'Coaching, Jewellery', 'Coaching aur jewellery dukaan: parents aur customers ko turant jawab.'),
 'ranchi': ('Ranchi', 'Real Estate, Clinics', 'Real estate aur clinics: leads ka reply, follow-up aur appointment.'),
 'jamshedpur': ('Jamshedpur', 'Vendors, Auto Service', 'Vendors aur auto service: quotation, payment aur follow-up ka kaam.'),
 'dhanbad': ('Dhanbad', 'Vendors, Clinics', 'Coal-belt ke vendors aur clinics: quotation aur payment follow-up.'),
 'bokaro': ('Bokaro', 'Steel Vendors, Schools', 'Steel vendors aur schools: quotation, admission aur payment ka kaam.'),
 'deoghar': ('Deoghar', 'Hotels, Sweets', 'Shravani Mela me hotel aur parcel orders ki bheed ek saath sambhalen.'),
}
BLOG_SEO_TITLES = {
 'whatsapp-par-60-second-me-reply': 'WhatsApp par 60 Second me Reply Kaise Dein | autenflo',
 'follow-up-1-3-7-din-ka-rule': 'Customer Follow-up ka 1-3-7 Din Rule + Templates | autenflo',
 'missed-enquiry-check-khud-kaise-karein': 'Missed WhatsApp Enquiry Kaise Ginein (7 Din) | autenflo',
}

def city_seo(slug):
    n, tags, local = CITY_SEO[slug]
    t1 = tags.split(', ')[0]
    for t in (f'AI & WhatsApp Automation in {n} | {t1} | autenflo', f'AI & WhatsApp Automation in {n} | autenflo'):
        if len(t) <= 60: break
    full, short = f'AI + WhatsApp automation, {n}: sales, marketing, operations, finance.', f'AI + WhatsApp automation, {n}: sales, marketing, finance.'
    for pre, tail in ((full, 'Setup ₹9,999 se.'), (short, 'Setup ₹9,999 se.'), (full, '₹9,999 se.'), (short, '₹9,999 se.')):
        d = f'{pre} {local} {tail}'
        if len(d) <= 155: break
    return t, d


# ---------- city page H1: home style ("... ka poora kaam, / AI ke saath. ..."), har shehar ka apna ----------
CITY_H1 = {
 'patna': 'Patna me enquiry aati hai har waqt. Jawab bhi do, har waqt',
 'muzaffarpur': 'Muzaffarpur ke trader ke liye, enquiry se dispatch tak',
 'gaya': 'Gaya ke hotel aur dharamshala ke liye AI booking assistant',
 'purnia': 'Purnia ke vyapari ke liye AI jo kabhi chhutti nahi leta',
 'bhagalpur': 'Bhagalpur ke silk dukandaar ke liye: rate, catalogue, dispatch',
 'arrah': 'Arrah me dukaan chalao, enquiry AI sambhale',
 'bihar-sharif': 'Bihar Sharif me chhota business, bada system',
 'darbhanga': 'Darbhanga ke makhana aur medical business ke liye AI',
 'lucknow': 'Lucknow ka business ab customer ko nahi rukata',
 'varanasi': 'Varanasi ke yatri aur khareedar, dono ko turant jawab',
 'prayagraj': 'Prayagraj ke coaching aur hotel ke liye AI assistant',
 'gorakhpur': 'Gorakhpur ke hospital, dukaan aur coaching ke liye 24x7 reply',
 'ayodhya': 'Ayodhya ke hotel aur dukaan: booking aur enquiry, 24x7',
 'mirzapur': 'Mirzapur ke exporter ke liye: buyer ko turant jawab',
 'jaunpur': 'Jaunpur ke coaching aur dukandaar ke liye 24x7 assistant',
 'azamgarh': 'Azamgarh ke school aur coaching ke liye: enquiry se admission tak',
 'ranchi': 'Ranchi ke clinic, coaching aur dukaan ke liye AI',
 'jamshedpur': 'Jamshedpur ke chhote udyog ke liye AI jo hisaab aur reminder dekhe',
 'dhanbad': 'Dhanbad ke dukandaar aur clinic ke liye: har customer ko jawab',
 'bokaro': 'Bokaro ke dukandaar aur coaching ke liye 24x7 reply',
 'deoghar': 'Deoghar ke hotel aur peda dukaan ke liye AI assistant',
}
HUB_H1 = {
 'bihar': 'Patna se Purnia tak: har enquiry ka turant jawab.',
 'uttar-pradesh': 'Lucknow se Gorakhpur tak: enquiry se payment tak, sab AI se.',
 'jharkhand': 'Ranchi se Dhanbad tak: reply, follow-up, hisaab, sab AI se.',
}
def aih(t): return re.sub(r'\bAI\b', AI, E(t))
def city_h1(slug): return aih(CITY_H1[slug])

def page(path, title, desc, main, jsonld=(), extra_js=(), og='website', noindex=False, crumbs=None, image=None):
    if noindex: NOINDEX.add(path)
    url = SITE + '/' + path.replace('index.html', '').lstrip('/')
    jl = list(jsonld) + ([crumbs_ld(crumbs)] if crumbs else [])
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jl)
    js = ''.join(f'<script src="{s}"></script>' for s in ('/assets/site.js', *extra_js))
    rb = '<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    img = image or SITE + '/og.png'
    html = (f'<!doctype html>\n<html lang="hi-Latn"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'{rb}<title>{E(title)}</title><meta name="description" content="{E(desc, quote=True)}"><link rel="canonical" href="{url}"><link rel="icon" href="/logo.png">'
            f'<meta name="theme-color" content="#8a62d6"><meta property="og:type" content="{og}"><meta property="og:site_name" content="autenflo"><meta property="og:title" content="{E(title, quote=True)}">'
            f'<meta property="og:description" content="{E(desc, quote=True)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{img}"><meta property="og:locale" content="hi_IN"><meta name="twitter:card" content="summary_large_image">'
            f'<meta name="twitter:title" content="{E(title, quote=True)}"><meta name="twitter:description" content="{E(desc, quote=True)}"><meta name="twitter:image" content="{img}">'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Mukta:wght@400;600;700&family=Outfit:wght@200..900&display=swap" rel="stylesheet">'
            f'<link rel="stylesheet" href="/assets/style.css">{ld}<noscript><style>#pre{{display:none}}</style></noscript>'
            '<script async src="https://www.googletagmanager.com/gtag/js?id=G-6012ZHG9SS"></script>'
            "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-6012ZHG9SS');</script></head>\n"
            f'<body>{SPRITE}<div id="pre"><img src="/logo.png" alt="autenflo"><i></i></div><div class="pbar"></div>{BG}'
            '<a class="ann" href="/#plans">🎁 Startups ke liye khaas offer: har plan ke saath <b>FREE Branding Consulting</b> →</a>'
            f'{HEADER}\n{main}\n{FOOTER}{FAB}{js}</body></html>')
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

# Home page ka poora pricing block (plans, comparison, service table, monthly charge). Home me badlo, city pages me apne aap aa jata hai.
_H = R('home.html')
PRICING = _H[_H.index('<p class="sub">Ek baar installation'):_H.index('</div></section><section class="sec" id="results"')]

# autenflo ke saare solutions (home page ke "Wahi paanch problem areas" section se), sirf WhatsApp nahi
SOLUTIONS = [
    ('📈 Sales', 'Har lead ko 60 second me reply. Phir 1, 3 aur 7 din par follow-up, khud.',
     ['Har enquiry ek jagah, ek bhi nahi chhooti', 'Quotation aur catalogue turant bhejta hai', 'Hot lead par aapko seedha alert']),
    ('📣 Marketing & Social Media (add-on)', 'Poore mahine ke posts, reels aur videos ek baar me. Hindi captions, design aur auto-posting.',
     ['Posts, posters aur Hindi captions aapke business ke andaaz me', 'Reels aur videos: idea, script aur editing, schedule ke saath', 'Instagram, Facebook aur YouTube par auto-post, plus report ki kya chala']),
    ('📦 Operations', 'Order aate hi sheet me. Stock kam hote hi alert. Kaam seedha sahi insaan ke paas.',
     ['Order apne aap sheet me', 'Stock khatam hone se pehle alert', 'Kaam staff ko auto assign, status track']),
    ('💬 Customer service', f'24x7 reply, Hindi me, aapke andaaz me. Jo {AI} na sambhaal paye, wo seedha aapko.',
     [f'WhatsApp {AI} agent, 24x7', 'Hindi voice agent calls uthata hai', 'Zaroori baat par turant aapko forward']),
    ('🧾 Finance', 'Reminder tameez se, khud. Bill ki photo se entry. Har shaam aaj ka hisaab.',
     ['Due date par polite payment reminder', 'Bill ki photo se entry aur GST data', 'Roz shaam kamai aur baaki ka summary']),
    ('🎓 Training', f'Schools, Colleges aur Institutions ke liye {AI} Training.',
     ['Daily 1 ghante ki live online class', 'Schools, colleges, ITIs, workplaces aur private/govt institutions ke liye', 'Schools ₹6,999, Colleges ₹9,999, Others ₹8,999 per month']),
]

def faq_list(n):
    return [
        (f'autenflo {n} ke business ke liye kya karta hai?', f'autenflo {n} ke business ko AI ki power deta hai: enquiry ka turant reply, hot leads ka follow-up, marketing aur social media posts aur videos, payment reminder aur hisaab me madad. Ye sab WhatsApp par chalta hai, 24x7.'),
        (f'Kya {n} me setup ke liye office aana padta hai?', 'Nahi. Poora setup online hota hai. Aap WhatsApp par baat shuru karte ho, baaki kaam hum sambhalte hain.'),
        ('Shuruaat kitne se hoti hai?', 'Launch plan ki one-time installation ₹9,999 aur monthly charge ₹2,999 se shuru hota hai. WhatsApp API platform, Meta aur AI usage ka kharcha aapke apne account se jata hai.'),
        ('Kya customer se Hindi me baat hoti hai?', 'Haan, Hindi me aur zaroorat par English me. Jahan insaan ki zaroorat ho, wahan baat seedha aap ya aapke staff tak pahunch jaati hai.'),
    ]

from city_data import CITY

def city_page(c):
    n, st = c['name'], c['state']; s = states[st]; sn = STATE_NAME[st]; d = CITY[c['slug']]
    url = SITE + u_city(c['slug'])
    CR = [('Home', '/'), ('Cities', U_CITIES), (sn, u_state(st)), (n, u_city(c['slug']))]
    msg = WA(f'Namaste autenflo, main {n} se hu. Mujhe apne business ko AI ki power chahiye.')
    near = [x for x in cities if x['state'] == st and x['slug'] != c['slug']][:4]
    faq = [d['faq'], faq_list(n)[2]]
    pricing = PRICING.replace('text=Namaste%20autenflo%2C%20mujhe%20', 'text=' + U.quote(f'Namaste autenflo, main {n} se hu. Mujhe '))
    sol = ''.join(f'<article class="glass bz"><span class="tg2">{t}</span><h3>{h}</h3><ul class="sl">' + ''.join(f'<li>{x}</li>' for x in li) + '</ul>' + ('<p style="margin-top:14px"><a class="ul" href="' + U_TRAIN + '">Plans dekhein →</a></p>' if t.startswith('🎓') else '') + '</article>' for t, h, li in SOLUTIONS)
    t1, t2 = d['biz'][0][0], d['biz'][1][0]
    offer = ('<div class="offer glass"><span class="gi">🎁</span><div><b>Startups ke liye khaas offer</b><p>Har plan ke saath <strong>FREE Branding Consulting</strong>.</p></div></div>' if st == 'bihar' else '')
    cards = ''.join(f'<article class="glass bz"><span class="em">{e}</span><h3>{E(t)}</h3><p class="fx1"><b>Problem:</b> {E(l)}</p><p class="fx1"><b>autenflo:</b> {E(f)}</p></article>' for (t, l, f), e in zip(d['biz'], ('🏪', '📲', '🧾')))
    chat = f'<div class="chat"><div class="cb c">{E(d["chat"][0])}</div><div class="cb b">{E(d["chat"][1])}</div></div>'
    areas = ''.join(f'<span>{E(a)}</span>' for a in d['areas'])
    main = f"""<main id="top"><section class="chero"><div class="wrap">{crumbs_html(CR)}<div class="chg"><div><span class="eyebrow">{n} · {sn}</span><h1 class="h1s">{city_h1(c["slug"])}</h1><p class="lead">{E(d['hook'])}</p><div class="cta"><a class="btn wab mag" href="{msg}">{WI}{n} ke liye baat karein</a><a class="btn ghost mag" href="#plans">Pricing dekhein</a></div></div>{hero_art(s['a'], s['b'], 'autenflo AI ka business setup')}</div></div></section>
<section class="sec"><div class="wrap"><span class="eyebrow">{n} ke business</span><h2 class="wide">{n} me paisa yahan leak hota hai.</h2><div class="g3">{cards}</div></div></section>
<section class="sec" id="solutions"><div class="wrap"><span class="eyebrow">Hamare solutions</span><h2 class="wide">Sirf WhatsApp nahi. {n} ke business ke poore kaam, ek jagah.</h2><p class="sub">WhatsApp {AI} agent sirf shuruaat hai. Sales, marketing, operations, customer service aur finance, sab hum sambhalte hain, aur institutions ke liye {AI} Training bhi.</p><div class="g3">{sol}</div></div></section>
<section class="sec"><div class="wrap"><span class="eyebrow">{n} ka business calendar</span><h2 class="wide">Kab {AI} ON karna sabse zyada kaam aata hai.</h2><p class="sub">{E(d['season'])}</p><h3 class="mt2">{n} me ek asli WhatsApp baatcheet</h3>{chat}</div></section>
<section class="sec"><div class="wrap"><span class="eyebrow">Hum kahan kaam karte hain</span><h2 class="wide">{n} ke in ilaakon ke business ke liye.</h2><div class="chips">{areas}</div></div></section>
<section class="sec" id="plans"><div class="wrap"><span class="eyebrow">Pricing · {n}</span><h2 class="wide">Employee ki salary ka sirf 12–15%. Kaam ek poori team jitna.</h2>{pricing}</div></section>
<section class="sec fq"><div class="wrap"><span class="eyebrow">Mann me jo sawal hain</span><h2>Pehle ye jaan lijiye</h2>{''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq)}</div></section>
<section class="sec"><div class="wrap"><div class="glass fin2"><div><h2>{n} ke apne business me {AI} lagayein.</h2><p class="sub">WhatsApp par batayiye aapka business kya hai, hum bataenge shuruaat kahan se karein.</p></div><a class="btn wab mag" href="{msg}">{WI}WhatsApp par abhi baat karein</a></div><h3 class="mt2">{sn} ke aur shehar</h3><div class="cgrid">{''.join(f'<a class="cc glass" href="{u_city(x["slug"])}"><div><h3>{x["name"]}</h3><p>{E(CITY[x["slug"]]["biz"][0][0])}</p></div></a>' for x in near)}</div></div></section></main>"""
    seo_t, seo_d = city_seo(c['slug'])
    ld = [{'@context': 'https://schema.org', '@type': 'WebPage', '@id': url, 'url': url, 'name': seo_t, 'description': seo_d, 'inLanguage': 'hi-Latn', 'isPartOf': {'@type': 'WebSite', 'name': 'autenflo', 'url': SITE}},
          {'@context': 'https://schema.org', '@type': 'Service', 'name': f'AI & WhatsApp automation in {n}', 'serviceType': 'AI business automation and WhatsApp automation', 'url': url,
           'description': seo_d, 'provider': ORG, 'areaServed': {'@type': 'City', 'name': n, 'containedInPlace': {'@type': 'State', 'name': sn}},
           'offers': {'@type': 'Offer', 'name': 'Launch plan: one-time installation', 'priceCurrency': 'INR', 'price': '9999', 'url': url + '#plans'}},
          {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]}]
    page(fp(u_city(c['slug'])), seo_t, seo_d, main, ld, crumbs=CR)
    return url

def hub_page(st):
    s = states[st]; sn = STATE_NAME[st]; lst = [x for x in cities if x['state'] == st]
    grid = ''.join(f'<a class="cc glass" href="{u_city(x["slug"])}"><div><h3>{x["name"]}</h3><p>Business ke liye AI ki power</p></div></a>' for x in lst)
    CR = [('Home', '/'), ('Cities', U_CITIES), (sn, u_state(st))]
    main = f'''<main id="top"><section class="chero"><div class="wrap">{crumbs_html(CR)}<div class="chg"><div><span class="eyebrow">{sn}</span><h1 class="h1s">{aih(HUB_H1[st])}</h1><p class="lead">{sn} ke {len(lst)} bade shehron me autenflo ka {AI} setup: enquiry ka reply, follow-up, marketing aur payment reminder.</p></div>{hero_art(s['a'], s['b'], 'autenflo AI')}</div><div class="cgrid">{grid}</div></div></section></main>'''
    t = f'AI & WhatsApp Automation in {states[st]["short"]} | autenflo'
    d = f'{states[st]["short"]} ke {len(lst)} shehron ({", ".join(x["name"] for x in lst[:3])} aur aage) me AI aur WhatsApp automation: sales, marketing, operations, finance. ₹9,999 se.'
    hu = SITE + u_state(st)
    ld = [{'@context': 'https://schema.org', '@type': 'CollectionPage', '@id': hu, 'url': hu, 'name': t, 'description': d, 'inLanguage': 'hi-Latn', 'isPartOf': {'@type': 'WebSite', 'name': 'autenflo', 'url': SITE},
           'mainEntity': {'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i, 'name': x['name'], 'url': SITE + u_city(x['slug'])} for i, x in enumerate(lst, 1)]}}]
    return page(fp(u_state(st)), t, d, main, ld, crumbs=CR)

def cities_index():
    CRI = [('Home', '/'), ('Cities', U_CITIES)]
    blocks = ''.join(f'<div class="wrap stsec"><h2><a href="{u_state(k)}">{STATE_NAME[k]}</a></h2><div class="cgrid">' + ''.join(f'<a class="cc glass" href="{u_city(x["slug"])}"><div><h3>{x["name"]}</h3><p>Business ke liye AI ki power</p></div></a>' for x in cities if x['state'] == k) + '</div></div>' for k in states)
    main = f'<main id="top" class="sec"><div class="wrap">{crumbs_html(CRI)}<span class="eyebrow">Aapka shehar</span><h1 class="h1s">{aih("Apna shehar chuniye, dekhiye AI aapke business me kya badlega.")}</h1><p class="sub">Bihar, Purvanchal aur Jharkhand ke shehron me autenflo ka {AI} setup. Apna shehar chuniye.</p></div>{blocks}</main>'
    t = 'AI & WhatsApp Automation in Bihar, UP, Jharkhand | autenflo'
    d = f'Bihar, Lucknow se Purvanchal aur Jharkhand ke {len(cities)} shehron me business ke liye AI aur WhatsApp automation: sales, marketing, operations, finance.'
    cu = SITE + U_CITIES
    ld = [{'@context': 'https://schema.org', '@type': 'CollectionPage', '@id': cu, 'url': cu, 'name': t, 'description': d, 'inLanguage': 'hi-Latn', 'isPartOf': {'@type': 'WebSite', 'name': 'autenflo', 'url': SITE},
           'mainEntity': {'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i, 'name': x['name'], 'url': SITE + u_city(x['slug'])} for i, x in enumerate(cities, 1)]}}]
    return page(fp(U_CITIES), t, d, main, ld, crumbs=CRI)

# ---------- blog ----------
BLOG_ART = ('<svg viewBox="0 0 400 220" role="img" aria-label="AI" xmlns="http://www.w3.org/2000/svg"><rect width="400" height="220" fill="#3b7fd4"/><circle cx="350" cy="30" r="90" fill="#8a62d6" opacity=".45"/><circle cx="30" cy="210" r="70" fill="#8a62d6" opacity=".3"/>'
            '<g stroke="#fff" stroke-width="3" opacity=".7"><path d="M120 110L200 70L280 120L200 160ZM200 70V160M120 110L280 120"/></g><g fill="#fff"><circle cx="120" cy="110" r="10"/><circle cx="200" cy="70" r="12"/><circle cx="280" cy="120" r="10"/><circle cx="200" cy="160" r="10"/></g>'
            '<rect x="160" y="100" width="80" height="44" rx="12" fill="#17202A" opacity=".75"/><text x="200" y="131" text-anchor="middle" font-family="Outfit,sans-serif" font-weight="800" font-size="24" fill="#fff">AI</text></svg>')
POSTS = [
 {'slug': 'missed-enquiry-check-khud-kaise-karein', 'title': '15 minute me pata karein kitni enquiry miss hui', 'cat': 'Sales', 'date': '2026-11-12', 'dlabel': '12 November 2026',
  'desc': '15 minute me apne WhatsApp ki enquiries gin kar dekhiye kitni late ya miss hui, aur us ka lagbhag rupaye me hisaab.',
  'body': """<p>Zyadatar owner ko lagta hai ki enquiry thodi hi miss hoti hai. Gin kar dekhne par aksar number badha nikalta hai. Ye check aap khud 15 minute me kar sakte hain.</p>
<h2>Kadam 1: pichhle 7 din ki list banaiye</h2>
<p>WhatsApp, Instagram aur call log se har enquiry ek sheet me likhiye: kab aayi, kisne bheji, kab reply gaya.</p>
<h2>Kadam 2: teen cheezein ginein</h2>
<ol><li>Kul kitni enquiry aayi.</li><li>Kitni ka reply 1 ghante ke baad gaya, ya gaya hi nahi.</li><li>Kitni ka follow-up kabhi hua hi nahi.</li></ol>
<h2>Kadam 3: rupaye me badliye</h2>
<p>Late ya miss enquiry ko, jitne % customer theek time par reply milne par ban jaate hain, us se multiply kijiye, phir ek customer ki average value se.</p>
<blockquote>Late enquiry x conversion % x ek customer ki value = lagbhag itne ka mauka gaya.</blockquote>
<p>Ye andaza hai, guarantee nahi. Par ye aapka apna data hai, aur isse saaf ho jata hai ki reply ki speed par kaam karna chahiye ya nahi.</p>
<p>Khud nahi karna chahte? Hamari taraf se ye check free hai.</p>"""},
 {'slug': 'follow-up-1-3-7-din-ka-rule', 'title': 'Ek baar poochhna kaafi nahi: follow-up ka 1-3-7 tareeka', 'cat': 'Sales', 'date': '2026-11-12', 'dlabel': '12 November 2026',
  'desc': 'Enquiry ke baad 1, 3 aur 7 din par kya bhejein, bina customer ko pareshan kiye. Teen chhote message templates ke saath.',
  'body': """<p>Bahut si enquiry isliye order nahi banti kyunki ek hi reply ke baad baat khatam ho jati hai. Customer busy tha, bhool gaya, ya doosre se bhi puch raha tha.</p>
<h2>Din 1: kaam ki yaad</h2>
<p>“Namaste [naam] ji, kal aapne [cheez] ke baare me poochha tha. Kuch aur jaankari chahiye to bataiye.”</p>
<h2>Din 3: ek kaam ki cheez</h2>
<p>“[Naam] ji, [rate / batch / slot] ki ek chhoti jaankari bhej raha hu. Aap chahein to kal [time] par baat kar lein?”</p>
<h2>Din 7: saaf aur izzat se aakhri message</h2>
<p>“[Naam] ji, agar abhi sahi samay nahi hai to koi baat nahi. Jab bhi zaroorat ho, yahin message kar dijiye.”</p>
<ul><li>Har message chhota rakhiye.</li><li>Jo mana kare, use dobara message mat bhejiye.</li><li>Sirf unhe message bhejiye jinhone khud aapko likha ho.</li></ul>
<p>Ye kaam roz haath se karna mushkil hota hai. Isiliye isse automate karna sabse pehla faayda deta hai.</p>"""},
 {'slug': 'whatsapp-par-60-second-me-reply', 'title': '60 second ka reply: customer rukta hai ya chala jaata hai', 'cat': 'AI', 'date': '2026-11-10', 'dlabel': '10 November 2026',
  'desc': 'Enquiry aate hi reply dene se order kyun badhte hain, aur chhote business ye kaam bina naya staff rakhe kaise kar sakte hain.',
  'body': """<p>Jo customer pehle reply paata hai, wahi aksar order bhi de deta hai. Phir bhi zyada tar business me enquiry ka reply tab jata hai jab staff ko yaad aata hai.</p>
<h2>Reply late hone ki 3 wajah</h2>
<ol><li>Enquiry WhatsApp, call aur Instagram par bikhri hoti hai.</li><li>Wahi sawal roz poochhe jaate hain: price, timing, address.</li><li>Raat ko aur chhutti ke din koi reply dene wala nahi hota.</li></ol>
<h2>Ye kaam aap kaise sambhal sakte hain</h2>
<ul><li>Sabse zyada poochhe jaane wale 10 sawal aur unke jawab ek jagah likh lijiye.</li><li>Har enquiry ko ek sheet me darj kijiye, taaki koi chhoote nahi.</li><li><b>Hot leads</b> ko alag mark kijiye aur unka follow-up 1, 3 aur 7 din par rakhiye.</li><li>Jo kaam roz dohrata hai, use AI se karwaiye aur sirf zaroori baat apne paas rakhiye.</li></ul>
<blockquote>Har bhoola hua follow-up, ek bika hua order hai.</blockquote>
<p>Apne business me ye kahan se shuru karein, ye jaanne ke liye WhatsApp par hamse 15 minute baat kar sakte hain.</p>"""},
]

def blog_pages():
    urls = [SITE + U_BLOG]
    CRB = [('Home', '/'), ('Blog', U_BLOG)]
    cards = ''
    for p in POSTS:
        url = SITE + u_post(p['slug']); urls.append(url)
        CR = [('Home', '/'), ('Blog', U_BLOG), (p['title'], u_post(p['slug']))]
        main = f'''<main id="top" class="sec"><div class="wrap">{crumbs_html(CR)}
<article><div class="post-head"><div><p class="meta">{p['cat']} · {p['dlabel']}</p><h1 class="h1s">{E(p['title'])}</h1><p class="sub">{E(p['desc'])}</p></div><div class="post-art">{BLOG_ART}</div></div>
<div class="prose">
{p['body']}
</div></article>
<div class="glass fin2"><div><h2>Apne business ka free missed-enquiry check.</h2><p class="sub">WhatsApp par 15 minute baat karke dekhiye aapke liye kya sahi rahega.</p></div><a class="btn wab mag" href="{WA('Namaste autenflo, maine aapka blog padha. Mujhe free missed-enquiry check chahiye.')}">{WI}WhatsApp par baat karein</a></div></div></main>'''
        seo_t = BLOG_SEO_TITLES.get(p['slug'], f'{p["title"]} | autenflo')
        ld = [{'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': p['title'], 'description': p['desc'], 'datePublished': p['date'], 'dateModified': p['date'], 'inLanguage': 'hi-Latn',
               'image': [SITE + '/og.png'], 'url': url, 'mainEntityOfPage': {'@type': 'WebPage', '@id': url}, 'author': ORG,
               'publisher': {'@type': 'Organization', 'name': 'autenflo', 'url': SITE, 'logo': {'@type': 'ImageObject', 'url': SITE + '/logo.png'}}}]
        page(fp(u_post(p['slug'])), seo_t, p['desc'], main, ld, og='article', crumbs=CR)
        cards += f'<a class="bc glass" href="{u_post(p["slug"])}">{BLOG_ART}<div><p class="meta">{p["cat"]} · {p["dlabel"]}</p><h3>{E(p["title"])}</h3><p>{E(p["desc"])}</p></div></a>'
    main = f'''<main id="top" class="sec"><div class="wrap">{crumbs_html(CRB)}<span class="eyebrow">Blog</span><h1 class="h1s">Leads, follow-up aur reply: seedhi bhasha me.</h1><p class="sub">Practical articles: enquiry, follow-up, marketing aur payment ke aasaan tareeke.</p>
<div class="bgrid">
<!-- ✏️ NAYA ARTICLE: POSTS list me ek entry jodo (sabse upar), phir build_site.py dobara chalao -->
{cards}
</div></div></main>'''
    bt, bd = 'Business, AI aur Marketing Tips | autenflo Blog', 'Chhote business ke liye AI, WhatsApp, sales, marketing aur payment ke practical tareeke, Hindi me. Message templates aur checklists ke saath.'
    bl = SITE + U_BLOG
    bld = [{'@context': 'https://schema.org', '@type': 'Blog', '@id': bl, 'url': bl, 'name': 'autenflo Blog', 'description': bd, 'inLanguage': 'hi-Latn', 'publisher': ORG,
            'blogPost': [{'@type': 'BlogPosting', 'headline': p['title'], 'url': SITE + u_post(p['slug']), 'datePublished': p['date']} for p in POSTS]}]
    page(fp(U_BLOG), bt, bd, main, bld, crumbs=CRB)
    return urls

# ---------- trust pages: about, privacy, terms ----------
def trust_pages():
    cta = f'<div class="glass fin2"><div><h2>Pehle free check, phir baat.</h2><p class="sub">15 minute me aapki pichhli 7 din ki enquiries gin kar batate hain.</p></div><a class="btn wab mag" href="{WA("Namaste autenflo, mujhe free missed-enquiry check chahiye")}">{WI}WhatsApp par baat karein</a></div>'
    def shell(slug, eyebrow, h1, sub, body, title, desc, typ='WebPage'):
        CRT = [('Home', '/'), (eyebrow, slug)]
        main = f'<main id="top" class="sec"><div class="wrap">{crumbs_html(CRT)}<span class="eyebrow">{eyebrow}</span><h1 class="h1s">{h1}</h1><p class="sub">{sub}</p><div class="prose">{body}</div>{cta}</div></main>'
        pu = SITE + slug
        ld = [{'@context': 'https://schema.org', '@type': typ, '@id': pu, 'url': pu, 'name': title, 'description': desc, 'inLanguage': 'hi-Latn', 'isPartOf': {'@type': 'WebSite', 'name': 'autenflo', 'url': SITE}}]
        if typ == 'AboutPage': ld[0]['about'] = ORG
        page(fp(slug), title, desc, main, ld, crumbs=CRT)
        return pu
    about = """<!-- ✏️ YAHAN FOUNDER KI PHOTO / 30 SECOND KA VIDEO, NAAM AUR KAHANI JODEIN. Trust ke liye ye sabse zaroori hai. -->
<h2>Hum kaun hain</h2>
<p>autenflo Patna, Bihar se chalta hai. Hum chhote aur beech ke business ke liye AI se WhatsApp ka reply, follow-up, payment reminder aur marketing ka kaam sambhalte hain, aur Hindi me, aapke saath baith kar setup karte hain.</p>
<h2>Hum kaise kaam karte hain</h2>
<ul><li><b>Pehle free check:</b> aapki pichhli 7 din ki enquiries gin kar batate hain kitni late ya miss hui.</li><li><b>Phir pehla kaam:</b> ek kaam, ek tay metric, end me result report.</li><li><b>Saaf kharcha:</b> hamari fees, WhatsApp platform aur Meta ka kharcha, sab pehle likh kar dete hain.</li><li><b>Likhit agreement:</b> kaam ka scope, data kiska hai, aur band kaise karna hai.</li></ul>
<h2>AI aur insaan</h2>
<p>Aapke customer ko pehle message me hi pata hota hai ki wo AI sahayak se baat kar raha hai. Wo insaan se baat maange to chat seedha aapko ya aapke staff ko jaati hai. Paisa, medical ya complaint jaise sawal AI khud nahi sambhalta.</p>
<h2>Aap kaise sampark karein</h2>
<p>Email: <a href="mailto:hello@autenflo.com">hello@autenflo.com</a><br>WhatsApp: <a href="https://wa.me/918849031907">+91 88490 31907</a><br>Shehar: Patna, Bihar<!-- ✏️ Poora address / registered business name / GST yahan jodein, jab ho --></p>"""
    privacy = """<!-- ⚠️ YE EK SHURUATI DRAFT HAI. Live karne se pehle apne vakeel/CA se India ke DPDP Act 2023 ke hisaab se zaroor confirm karwayein. -->
<p>Antim update: 12 November 2026</p>
<h2>Hum kya jaankari lete hain</h2>
<p>Website ke form me aap naam, WhatsApp number aur business ki jaankari dete hain. WhatsApp par aap jo message bhejte hain, wo bhi hum dekhte hain. Website par Google Analytics se anonymous visit data (kaun sa page, kitni der) liya jata hai.</p>
<h2>Hum ise kyun use karte hain</h2>
<p>Aapse baat karne, demo dikhane, service dene, aur website behtar karne ke liye. Hum aapki jaankari bechte nahi.</p>
<h2>Kin ke saath share hota hai</h2>
<p>Sirf un tools ke saath jo kaam ke liye zaroori hain: WhatsApp API provider aur Meta, AI aur automation tools, Google Analytics, aur website form ka hosting provider. Client ke customers ka data client ke agreement ke hisaab se hi handle hota hai.</p>
<h2>Kitne din rakhte hain</h2>
<p>Jab tak aapse baat ya service chal rahi hai, aur uske baad zaroori kaam (hisaab, agreement) ke liye jitna chahiye. Aap kabhi bhi jaankari hatane ko keh sakte hain.</p>
<h2>Aapke adhikar</h2>
<p>Aap apni jaankari dekhne, sudharne ya hatane ke liye <a href="mailto:hello@autenflo.com">hello@autenflo.com</a> par likh sakte hain.</p>
<h2>Cookies</h2>
<p>Hum analytics ke liye cookies use karte hain. Browser settings se aap ise rok sakte hain.</p>"""
    terms = """<!-- ⚠️ YE EK SHURUATI DRAFT HAI. Live karne se pehle vakeel se confirm karwayein, aur [ ] wale business-decision (notice period, refund) apne hisaab se tay karein. -->
<p>Antim update: 12 November 2026</p>
<h2>Hamari service</h2>
<p>autenflo WhatsApp par AI se reply, follow-up, reminder aur sambandhit kaam sambhalta hai, jaisa aapke plan ya agreement me likha ho. Naye kaam ya add-on alag se tay hote hain.</p>
<h2>Charges</h2>
<p>Ek baar ka installation aur monthly charge plan ke hisaab se. WhatsApp API platform, Meta ke message charges, AI/API usage aur domain jaise third-party kharche aapke apne account se jaate hain aur hamare charge me shamil nahi hain.</p>
<h2>AI aur uski seema</h2>
<p>AI kabhi-kabhi galat reply de sakta hai. Hum galat jawab ke rules aur insaan tak handover set karte hain aur replies par nazar rakhte hain, par poori guarantee nahi de sakte. Customer ko AI sahayak hone ki baat saaf dikhaai jaati hai.</p>
<h2>Aapki zimmedari</h2>
<p>Aap sahi jaankari (rate, offer, FAQ) dete hain, aur sirf un logon ko message bhejte hain jinhone sampark kiya ho ya jinki anumati ho. WhatsApp ke niyam todne par number ban ho sakta hai, jiske liye hum zimmedar nahi honge.</p>
<h2>Data</h2>
<p>Aapke business aur customers ka data aapka hai. Hum use sirf service dene ke liye use karte hain.</p>
<h2>Band karna</h2>
<p>Koi lamba contract nahi. Aap [30 din ke notice] par service band kar sakte hain. Us mahine tak ka monthly charge lagta hai. [Refund ka niyam yahan likhein.]</p>
<h2>Seema aur kanoon</h2>
<p>Hamari zimmedari us mahine ke monthly charge tak seemit rahegi. Ye shartein Bharat ke kanoon ke adheen hain. [Vivad ke liye adhikar-kshetra: Patna, Bihar.]</p>
<h2>Sampark</h2>
<p><a href="mailto:hello@autenflo.com">hello@autenflo.com</a></p>"""
    return [shell(U_ABOUT, 'About', aih('Hum kaun hain: Hindi me, aapke saath baith kar AI lagate hain.'), 'Seedhi baat: hum kya karte hain, kaise karte hain, aur kya nahi karte.', about, 'About autenflo | AI Back-office for Business, Patna, Bihar', 'autenflo Patna, Bihar se chalta hai: AI se sales, marketing, operations, finance aur WhatsApp customer service. Pehle free 15 minute ka check.', 'AboutPage'),
            shell(U_PRIVACY, 'Privacy', 'Privacy Policy: aapka data, saaf shabdon me', 'Aapki jaankari ka hum kya karte hain.', privacy, 'Privacy Policy | autenflo', 'autenflo kaun si jaankari leta hai, kyun, aur kin ke saath share karta hai.'),
            shell(U_TERMS, 'Terms', 'Terms: kya milta hai, kya nahi, aur band kaise karein', 'Service, charges, AI ki seema aur band karne ke niyam.', terms, 'Terms of Service | autenflo', 'autenflo ki service, charges, AI ki seema aur cancellation ke niyam.')]

# ---------- home + training ----------
def _faq_ld(html):
    out = []
    for q, a in re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', html, re.S):
        strip = lambda t: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', t)).strip()
        out.append({'@type': 'Question', 'name': strip(q), 'acceptedAnswer': {'@type': 'Answer', 'text': strip(a)}})
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': out} if out else None

def home_training():
    home = R('home.html').replace('<div class="glass tz">', '<div class="glass tz"><div class="tzart">' + LEARN + '</div>')
    org = {'@context': 'https://schema.org', '@type': 'Organization', '@id': SITE + '/#organization', 'name': 'autenflo', 'url': SITE, 'logo': SITE + '/logo.png', 'email': 'hello@autenflo.com',
           'description': 'AI se sales, marketing, operations, finance aur WhatsApp customer service: chhote aur beech ke business ke liye, Hindi me.',
           'address': {'@type': 'PostalAddress', 'addressLocality': 'Patna', 'addressRegion': 'Bihar', 'addressCountry': 'IN'},
           'contactPoint': [{'@type': 'ContactPoint', 'contactType': 'customer support', 'telephone': '+91-88490-31907', 'email': 'hello@autenflo.com', 'availableLanguage': ['Hindi', 'English']}],
           'areaServed': [{'@type': 'State', 'name': 'Bihar'}, {'@type': 'State', 'name': 'Uttar Pradesh'}, {'@type': 'State', 'name': 'Jharkhand'}]}
    site = {'@context': 'https://schema.org', '@type': 'WebSite', '@id': SITE + '/#website', 'name': 'autenflo', 'url': SITE, 'inLanguage': 'hi-Latn', 'publisher': {'@id': SITE + '/#organization'}}
    ld = [org, site] + ([f] if (f := _faq_ld(home)) else [])
    page('index.html', 'autenflo: AI & WhatsApp Automation for Bihar, UP, Jharkhand', 'Aapke business ka AI back-office: sales, marketing, operations aur finance, plus WhatsApp par 24x7 reply. Pehle free 15 minute ka missed-enquiry check.', home, ld, ('/assets/home.js',))
    CRT = [('Home', '/'), ('AI Training', U_TRAIN)]
    tr = R('training.html').replace('<div class="hv">', '<div class="hv"><div class="tart">' + LEARN + '</div>').replace('<div class="hl">', '<div class="hl">' + crumbs_html(CRT), 1)
    tu = SITE + U_TRAIN
    tld = [{'@context': 'https://schema.org', '@type': 'Service', 'name': 'AI Training for Schools, Colleges and Institutions', 'url': tu, 'serviceType': 'Live online AI training', 'provider': ORG,
            'areaServed': {'@type': 'Country', 'name': 'India'},
            'description': 'Daily 1 ghante ki live online AI class, Hindi me, schools, colleges, ITIs, workplaces aur institutions ke liye.',
            'offers': [{'@type': 'Offer', 'name': n, 'price': pr, 'priceCurrency': 'INR', 'description': 'per month', 'url': tu} for n, pr in (('Schools', '6999'), ('Colleges', '9999'), ('Others', '8999'))]}]
    page(fp(U_TRAIN), 'AI Training for Schools, Colleges & ITIs | autenflo', 'Daily 1 ghante ki live online AI class: Schools ₹6,999, Colleges ₹9,999, Others ₹8,999 per month. ITIs, workplaces aur institutions ke liye.', tr, tld, crumbs=CRT)
    return [SITE + '/', tu]

if __name__ == '__main__':
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT + '/assets')
    write('assets/style.css', R('global.css') + '\n' + R('extra.css') + '\n.chat{display:flex;flex-direction:column;gap:10px;max-width:480px}.cb{padding:12px 16px;border-radius:18px;font-weight:600;max-width:88%}.cb.c{background:#fff;color:#17202A;align-self:flex-start}.cb.b{background:#dcf8c6;color:#17202A;align-self:flex-end}\n.em{font-size:1.8rem;display:block;margin-bottom:8px}.fr{list-style:none;padding:0;margin:14px 0 0}.fr li{margin:6px 0;font-weight:600}.cc div{padding:22px 24px}.sl{list-style:none;padding:0;margin:14px 0 0;display:grid;gap:8px}.sl li{padding-left:24px;position:relative;font-weight:600;font-size:.95rem}.sl li::before{content:"✓";position:absolute;left:0;color:var(--gd);font-weight:800}\n')
    write('assets/site.js', 'function hidePre(){var p=document.getElementById("pre");if(p)p.style.display="none"}addEventListener("load",hidePre);setTimeout(hidePre,1200);var y=document.getElementById("yr");if(y)y.textContent=new Date().getFullYear();document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("a[href*=\'wa.me\']");if(a&&window.gtag)gtag("event","whatsapp_click",{page_path:location.pathname,link_text:(a.textContent||"").trim().slice(0,40)})});var f=document.querySelector("form[name=contact]");if(f)f.addEventListener("submit",function(){if(window.gtag)gtag("event","form_submit",{page_path:location.pathname})});')
    write('assets/home.js', R('home.js'))
    shutil.copy(os.path.join(HERE, 'og.png'), os.path.join(OUT, 'og.png'))
    urls = home_training() + blog_pages() + [cities_index()] + trust_pages() + [hub_page(k) for k in states] + [city_page(c) for c in cities]
    skip = {SITE + '/' + p.replace('index.html', '').lstrip('/') for p in NOINDEX}
    urls = [u for u in urls if u not in skip]
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>' for u in urls) + '</urlset>')
    write('robots.txt', f'User-agent: *\nAllow: /\nDisallow: /404.html\nSitemap: {SITE}/sitemap.xml\n')
    # 404 page
    nf = f'<main id="top" class="sec"><div class="wrap"><span class="eyebrow">404</span><h1 class="h1s">Ye page nahi mila.</h1><p class="sub">Link purana ho sakta hai. Home par jaayein ya apna shehar chuniye.</p><div class="cta"><a class="btn wab mag" href="/">Home par jaayein</a><a class="btn ghost mag" href="{U_CITIES}">Sabhi cities</a></div></div></main>'
    page('404.html', 'Page nahi mila | autenflo', 'Ye page nahi mila. autenflo ke home page ya cities page par jaayein.', nf, noindex=True)
    # ---- purane URL -> naye URL (301) ----
    OLD = [('/cities/', U_CITIES), ('/ai-training/', U_TRAIN), ('/about/', U_ABOUT), ('/privacy/', U_PRIVACY), ('/terms/', U_TERMS)]
    OLD += [(f'/{k}/', u_state(k)) for k in states] + [(f'/{c["state"]}/{c["slug"]}/', u_city(c['slug'])) for c in cities]
    OLDF = [(f'/blog/{o}.html', u_post(o)) for o in POST_SLUG]
    red = ['# 301 redirects: purane URL -> naye SEO URL (Netlify / Cloudflare Pages format)']
    for o, n in OLD: red += [f'{o} {n} 301', f'{o}index.html {n} 301']
    for o, n in OLDF: red += [f'{o} {n} 301', f'{o[:-5]} {n} 301']
    write('_redirects', '\n'.join(red) + '\n')
    ht = ['# 301 redirects (Apache). Agar aap Netlify/Cloudflare Pages par ho to ye file ignore hoti hai, _redirects kaam karti hai.', 'ErrorDocument 404 /404.html', 'Options -Indexes', '']
    for o, n in OLD: ht.append(f'RedirectMatch 301 ^{o}(index\\.html)?$ {n}')
    for o, n in OLDF: ht.append(f'RedirectMatch 301 ^{o.replace(".", chr(92) + ".")}$ {n}'); ht.append(f'RedirectMatch 301 ^{o[:-5]}/?$ {n}')
    write('.htaccess', '\n'.join(ht) + '\n')
    open(os.path.join(HERE, 'redirect-map.csv'), 'w', encoding='utf-8').write('old_url,new_url\n' + ''.join(f'{SITE}{o},{SITE}{n}\n' for o, n in OLD + OLDF))
    write('README.txt', 'logo.png naam se apna logo is folder ke root me (index.html ke saath) daalo.\nSabhi city pages aur state hub pages Google me index hote hain aur sitemap.xml me hain.\nAbout, Privacy, Terms pages me [ ] aur HTML comments wali jagah bhariye aur vakeel se confirm karwayein.\nURL badle hain: purane URL _redirects (Netlify/Cloudflare Pages) ya .htaccess (Apache) se 301 hote hain. Upload ke baad Search Console me naya sitemap.xml submit karein.\n')
    print(len(urls), 'pages,', len(OLD) + len(OLDF), 'redirects')
