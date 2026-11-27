#!/usr/bin/env python3
"""autenflo: plain HTML site generator.
Chalane ke liye:  python3 build_site.py   (output: ./autenflo-site/)
Shehron ki list cities.json me hai. Naya shehar jodna ho to wahan ek entry badhao aur dobara chalao.
"""
import json, os, re, shutil, urllib.parse as U
from html import escape as E
from industry_data import IND

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'autenflo-site')
R = lambda n: open(os.path.join(HERE, n), encoding='utf-8').read()
data = json.load(open(os.path.join(HERE, 'cities.json'), encoding='utf-8'))
states, cities = data['states'], data['cities']
SITE = 'https://autenflo.com'
TODAY = '2026-11-27'
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
U_IND = '/ai-automation-for-businesses/'
def u_state(st): return f'/{KW}-{st}/'
def u_city(slug): return f'/{KW}-{slug}/'
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

IND_TAG = {
    'd2c': 'Enquiry, order, COD aur repeat customers',
    'coaching': 'Admission enquiry, fees aur attendance alert',
    'clinic': 'Appointment, no-show reminder, report alert',
    'realestate': 'Leads, site visit follow-up, installment',
    'transport': 'Rate quote, gaadi status, bilty aur freight payment',
    'services': 'Documents, due date reminder, fees collection',
}
SOL_MENU = [
    ('Sales & Follow-up', 'Enquiry ka 60 second me reply, 1-3-7 din follow-up'),
    ('Customer Support 24x7', 'Hindi me jawab, mushkil case seedha aap tak'),
    ('Quotation, Billing & Payments', 'Invoice auto, due date se pehle reminder'),
    ('Orders, Stock & Reports', 'Auto record, low stock alert, roz ka summary'),
    ('Marketing & Social Media', 'Posts, reels aur auto-posting'),
]
CHV = '<svg class="chv" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
_WAQ = WA("Namaste autenflo, mujhe free process audit chahiye")
def _mega_menu():
    ind = ''.join(f'<a class="mgi" href="{v["u"]}"><span class="mn">{i:02d}</span><span><b>{E(v["name"])}</b><small>{IND_TAG[k]}</small></span></a>' for i, (k, v) in enumerate(IND.items(), 1))
    m_ind = (f'<div class="mi"><button class="mt" type="button" aria-expanded="false" aria-controls="mm-ind">Industries{CHV}</button><div class="mm" id="mm-ind"><div class="mm-in"><div class="mm-l"><p class="mh">Apni industry chuniye</p><div class="mg2">{ind}</div></div>'
             f'<aside class="mm-r"><b>Business list me nahi hai?</b><p>15 minute ka free process audit. Hum bata denge kaun sa kaam automate hoga.</p><a class="btn wab" href="{_WAQ}">{WI}Abhi baat karein</a><a class="ul" href="{U_IND}">Sabhi industries dekhein →</a></aside></div></div></div>')
    sol = ''.join(f'<a class="mgi" href="/#processes"><span class="mn">{i}</span><span><b>{t}</b><small>{d}</small></span></a>' for i, (t, d) in enumerate(SOL_MENU, 1))
    m_sol = (f'<div class="mi"><button class="mt" type="button" aria-expanded="false" aria-controls="mm-sol">Solutions{CHV}</button><div class="mm" id="mm-sol"><div class="mm-in"><div class="mm-l"><p class="mh">Kaam ke hisaab se</p><div class="mg2">{sol}</div></div>'
             f'<aside class="mm-r mm-t"><span class="tg2">{AI} Training</span><b>Schools, Colleges aur Institutes</b><p>Daily 1 ghante ki live online class, Hindi me.</p><ul><li>Schools <strong>₹6,999</strong></li><li>Colleges <strong>₹9,999</strong></li><li>Others <strong>₹8,999</strong></li></ul><a class="btn" href="{U_TRAIN}">Training plans dekhein</a></aside></div></div></div>')
    cols = ''
    for k in states:
        cols += f'<div class="mc"><a class="mh" href="{u_state(k)}">{STATE_NAME[k].split(" (")[0]} →</a><ul>' + ''.join(f'<li><a href="{u_city(c["slug"])}">{E(c["name"])}</a></li>' for c in cities if c['state'] == k) + '</ul></div>'
    m_city = (f'<div class="mi"><button class="mt" type="button" aria-expanded="false" aria-controls="mm-city">Cities{CHV}</button><div class="mm" id="mm-city"><div class="mm-in mm-c"><div class="mcg">{cols}</div>'
              f'<aside class="mm-r"><b>Setup online hota hai</b><p>Aapka shehar list me na ho tab bhi kaam ho jata hai. Office aane ki zaroorat nahi.</p><a class="ul" href="{U_CITIES}">Sabhi {len(cities)} cities dekhein →</a></aside></div></div></div>')
    return m_ind + m_sol + m_city
def _mobile_menu():
    d = lambda t, inner: f'<details class="ms"><summary>{t}</summary><div>{inner}</div></details>'
    a = lambda h, t: f'<a href="{h}">{t}</a>'
    return (d('Industries', ''.join(a(v['u'], E(v['name'])) for v in IND.values()) + a(U_IND, 'Sabhi industries →'))
            + d('Solutions', ''.join(a('/#processes', t) for t, _ in SOL_MENU) + a(U_TRAIN, 'AI Training (Schools, Colleges)'))
            + d('Cities', ''.join(a(u_state(k), STATE_NAME[k].split(' (')[0] + ' ke sabhi shehar') for k in states) + a(u_city('patna'), 'Patna') + a(u_city('lucknow'), 'Lucknow') + a(u_city('ranchi'), 'Ranchi') + a(U_CITIES, 'Sabhi cities →'))
            + a('/#plans', 'Pricing') + a(U_BLOG, 'Blog') + a(U_ABOUT, 'About')
            + f'<a class="btn wab" href="{_WAQ}">{WI}Baat karein</a>')
HEADER = ('<header><div class="wrap"><a class="wm" href="/" aria-label="autenflo home"><img src="/logo.png" alt="autenflo" width="230" height="38"></a><nav aria-label="Main">'
          + _mega_menu()
          + ''.join(f'<a class="ul" href="{h}">{t}</a>' for h, t in (('/#plans', 'Pricing'), (U_BLOG, 'Blog'), (U_ABOUT, 'About')))
          + f'<a class="btn wab" href="{_WAQ}">{WI}Baat karein</a></nav>'
          '<details class="mnav"><summary aria-label="Menu"><span></span><span></span><span></span></summary><div class="mp">' + _mobile_menu() + '</div></details></div></header>')
def _footer():
    wa = WA("Namaste autenflo, mujhe free process audit chahiye")
    top = {}
    for c in cities: top.setdefault(c['state'], []).append(c)
    cols = ''
    for k in states:
        cols += f'<div class="fc"><h4>{STATE_NAME[k]}</h4><ul>' + ''.join(f'<li><a href="{u_city(c["slug"])}">{E(c["name"])}</a></li>' for c in top[k][:6]) + f'<li><a class="all" href="{u_state(k)}">Sabhi cities dekhein →</a></li></ul></div>'
    return ('<footer class="ft"><div class="wrap">'
      '<div class="fcta glass"><div><h3>Staff nahi badhana? Pehle free process audit karwayein.</h3><p>15 minute me bata denge ki aapke business me kaun se manual aur repetitive kaam automate ho sakte hain. Koi pitch nahi, koi dabaav nahi.</p></div>'
      f'<a class="btn wab" href="{wa}">{WI}Abhi baat karein</a></div>'
      '<div class="fgrid">'
      '<div class="fb0"><a class="wm" href="/" aria-label="autenflo home"><img src="/logo.png" alt="autenflo" width="250" height="42" loading="lazy"></a><p>autenflo aapke business ka AI back-office hai: enquiry se payment tak, har manual aur repetitive process AI se automate. Muzaffarpur, Bihar.</p>'
      f'<div class="fct"><a class="ul" href="mailto:hello@autenflo.com">hello@autenflo.com</a><a class="ul" href="{wa}">Phone: +91 88490 31907</a></div></div>'
      '<div class="fc"><h4>Quick links</h4><ul><li><a href="/">Home</a></li><li><a href="/#aapka">Industries</a></li><li><a href="/#plans">Pricing</a></li><li><a href="/#training">AI Training</a></li><li><a href="/#results">Hamara tareeka</a></li><li><a href="/#faq">FAQ</a></li><li><a href="/#sampark">Contact</a></li></ul></div>'
      f'<div class="fc"><h4>Explore</h4><ul><li><a href="{U_BLOG}">Blog</a></li><li><a href="{U_TRAIN}">AI Training for Institutions</a></li><li><a href="{U_CITIES}">Sabhi Cities</a></li><li><a href="{U_IND}">Industries</a></li><li><a href="{U_ABOUT}">About</a></li><li><a href="{U_PRIVACY}">Privacy Policy</a></li><li><a href="{U_TERMS}">Terms</a></li></ul></div>'
      + cols + '</div>'
      '<div class="fbot"><p>© <span id="yr">2026</span> autenflo. Sabhi adhikar surakshit.</p><p>Bihar, Uttar Pradesh aur Jharkhand ke businesses ka AI back-office.</p><p>Mishratola, Gannipur, Muzaffarpur, Bihar · <a class="ul" href="https://www.instagram.com/autenfloai/" target="_blank" rel="me noopener">Instagram</a> · <a class="ul" href="https://www.linkedin.com/company/autenflo/" target="_blank" rel="me noopener">LinkedIn</a></p><a class="ul" href="#top">Upar jaayein ↑</a></div>'
      '</div></footer>')
FOOTER = _footer()
FAB = f'<a class="fab" href="{WA("Namaste autenflo, mujhe free process audit chahiye")}" aria-label="Abhi baat karein">{WI}</a>'

NOINDEX = set()

# ---------- SEO: title <= 60, description <= 155 characters ----------
# slug: (title me shehar ka naam, 2 chhote keyword, local line)
CITY_SEO = {
 'patna': ('Patna', 'Coaching, Clinics', 'Coaching, clinics, real estate: raat 11 baje bhi har enquiry ka reply.'),
 'muzaffarpur': ('Muzaffarpur', 'Retail, Transport', 'Retail, transport aur services: rate, booking aur payment auto.'),
 'gaya': ('Gaya', 'Cab, Tours', 'Pitru Paksha me cab aur tours ki bheed ek saath sambhalen.'),
 'purnia': ('Purnia', 'Transport, Clinics', 'Transport aur clinics: gaon se aayi enquiry ka turant reply.'),
 'bhagalpur': ('Bhagalpur', 'Silk, Retail', 'Silk aur garment sellers ke order, rate, dispatch aur payment ka hisaab.'),
 'arrah': ('Arrah', 'Retail, Coaching', 'Retail dukaan aur coaching: lead ka reply aur follow-up, bina extra staff.'),
 'bihar-sharif': ('Bihar Sharif', 'Retail, Transport', 'Retail aur transport: rate, booking aur payment ka kaam.'),
 'darbhanga': ('Darbhanga', 'Makhana, Clinics', 'Makhana sellers aur clinics: order, appointment aur payment ka kaam.'),
 'lucknow': ('Lucknow', 'Clinics, D2C', 'Clinics aur D2C boutiques: jo pehle reply kare, customer usi ka.'),
 'varanasi': ('Varanasi', 'Tours, Silk', 'Cab, tours aur silk sellers: enquiry se booking tak, ek jagah.'),
 'prayagraj': ('Prayagraj', 'Coaching, Travel', 'Exam coaching, hostel aur mela season ke cab aur tours ka poora kaam.'),
 'gorakhpur': ('Gorakhpur', 'Clinics, Transport', 'Clinics aur transport: door se aaye customer ko turant reply.'),
 'ayodhya': ('Ayodhya', 'Cab, Tours', 'Cab, tours aur dukaan: yatri boom me har enquiry sambhalen.'),
 'mirzapur': ('Mirzapur', 'Retail, Transport', 'Carpet sellers aur transport: catalogue, rate, dispatch aur payment.'),
 'jaunpur': ('Jaunpur', 'Coaching, Garments', 'Coaching admission aur garment dukaan: reply se payment tak.'),
 'azamgarh': ('Azamgarh', 'Coaching, Jewellery', 'Coaching aur jewellery dukaan: parents aur customers ko turant jawab.'),
 'ranchi': ('Ranchi', 'Real Estate, Clinics', 'Real estate aur clinics: leads ka reply, follow-up aur appointment.'),
 'jamshedpur': ('Jamshedpur', 'Transport, Services', 'Transport aur services: quotation, payment aur follow-up ka kaam.'),
 'dhanbad': ('Dhanbad', 'Transport, Clinics', 'Transport aur clinics: booking aur payment follow-up.'),
 'bokaro': ('Bokaro', 'Transport, Schools', 'Transport aur schools: booking, admission aur payment ka kaam.'),
 'deoghar': ('Deoghar', 'Cab, Retail', 'Shravani Mela me cab aur peda dukaan ke orders ki bheed ek saath sambhalen.'),
}

def city_seo(slug):
    n, tags, local = CITY_SEO[slug]
    t1 = tags.split(', ')[0]
    for t in (f'AI Business Automation in {n} | {t1} | autenflo', f'AI Business Automation in {n} | autenflo'):
        if len(t) <= 60: break
    full, short = f'AI process automation, {n}: manual kaam, follow-up, billing, reports.', f'AI automation, {n}: manual kaam, follow-up, billing.'
    for pre, tail in ((full, 'Setup ₹14,999 se.'), (short, 'Setup ₹14,999 se.'), (full, '₹14,999 se.'), (short, '₹14,999 se.')):
        d = f'{pre} {local} {tail}'
        if len(d) <= 155: break
    return t, d


# ---------- city page H1: home style ("... ka poora kaam, / AI ke saath. ..."), har shehar ka apna ----------
CITY_H1 = {
 'patna': 'Patna me enquiry aati hai har waqt. Jawab bhi do, har waqt',
 'muzaffarpur': 'Muzaffarpur ke trader ke liye, enquiry se dispatch tak',
 'gaya': 'Gaya ke cab aur tour operator ke liye AI booking assistant',
 'purnia': 'Purnia ke vyapari ke liye AI jo kabhi chhutti nahi leta',
 'bhagalpur': 'Bhagalpur ke silk aur garment seller ke liye: rate, catalogue, dispatch',
 'arrah': 'Arrah me dukaan chalao, enquiry AI sambhale',
 'bihar-sharif': 'Bihar Sharif me chhota business, bada system',
 'darbhanga': 'Darbhanga ke makhana seller aur retail business ke liye AI',
 'lucknow': 'Lucknow ka business ab customer ko nahi rukata',
 'varanasi': 'Varanasi ke yatri aur khareedar, dono ko turant jawab',
 'prayagraj': 'Prayagraj ke coaching aur travel business ke liye AI assistant',
 'gorakhpur': 'Gorakhpur ke hospital, dukaan aur coaching ke liye 24x7 reply',
 'ayodhya': 'Ayodhya ke cab aur dukaan: booking aur enquiry, 24x7',
 'mirzapur': 'Mirzapur ke exporter ke liye: buyer ko turant jawab',
 'jaunpur': 'Jaunpur ke coaching aur dukandaar ke liye 24x7 assistant',
 'azamgarh': 'Azamgarh ke school aur coaching ke liye: enquiry se admission tak',
 'ranchi': 'Ranchi ke clinic, coaching aur dukaan ke liye AI',
 'jamshedpur': 'Jamshedpur ke chhote udyog ke liye AI jo hisaab aur reminder dekhe',
 'dhanbad': 'Dhanbad ke dukandaar aur clinic ke liye: har customer ko jawab',
 'bokaro': 'Bokaro ke dukandaar aur coaching ke liye 24x7 reply',
 'deoghar': 'Deoghar ke cab aur peda dukaan ke liye AI assistant',
}
HUB_H1 = {
 'bihar': 'Gaya se Purnia tak: har enquiry ka turant jawab.',
 'uttar-pradesh': 'Lucknow se Gorakhpur tak: enquiry se payment tak, sab AI se.',
 'jharkhand': 'Ranchi se Dhanbad tak: reply, follow-up, hisaab, sab AI se.',
}
def aih(t): return re.sub(r'\bAI\b', AI, E(t))
def city_h1(slug): return aih(CITY_H1[slug])

SEO_OV = {
 '/ai-automation-for-clinics-and-hospitals/': ('Clinic & Hospital AI WhatsApp Automation | autenflo', 'Clinic, hospital aur diagnostic center ke liye AI: appointment booking, no-show reminder, report ready alert aur follow-up. Bihar, UP, Jharkhand.'),
 '/ai-automation-for-coaching-institutes/': ('Coaching Institute AI WhatsApp Automation | autenflo', 'Coaching, tuition aur school ke liye AI: admission enquiry ka 60 second me reply, demo follow-up, fees reminder aur attendance alert. Bihar, UP, Jharkhand.'),
 '/ai-automation-for-businesses/': (None, 'Coaching, clinics aur anya businesses ke liye AI WhatsApp automation: har industry ki problem aur uska hal. Bihar, Uttar Pradesh aur Jharkhand me.'),
 '/ai-whatsapp-automation-bihar/': ('AI Business Automation in Bihar: 8 Cities | autenflo', 'Bihar ke 8 shehron (Patna, Gaya, Bhagalpur, Muzaffarpur aur aage) me AI process automation: sales, marketing, operations, finance. ₹14,999 se.'),
 '/ai-whatsapp-automation-jharkhand/': ('AI Business Automation in Jharkhand: 5 Cities | autenflo', 'Jharkhand ke 5 shehron (Ranchi, Jamshedpur, Dhanbad, Bokaro, Deoghar) me AI process automation: sales, marketing, operations, finance. ₹14,999 se.'),
 '/ai-whatsapp-automation-bihar-up-jharkhand/': (None, 'Bihar, Lucknow se Purvanchal aur Jharkhand ke 21 shehron me business ke liye AI process automation: sales, marketing, operations, finance, support.'),
 '/ai-whatsapp-automation-purnia/': (None, 'AI automation, Purnia: manual kaam, follow-up, billing. Makhana traders aur clinics: gaon se aayi enquiry ka turant reply. Setup ₹14,999 se shuru.'),
 '/about-autenflo/': (None, 'autenflo Muzaffarpur, Bihar se chalta hai: AI se sales, marketing, operations, finance aur customer service ke manual kaam automate. Free 15 minute audit.'),
 '/blog/': ('Business, AI aur Marketing Tips | autenflo Blog Hindi', None),
 '/': (None, 'Naya staff nahi, agency nahi, manual work nahi. Aapke business ka AI back-office: enquiry se payment tak har process automate. Free 15 minute audit.'),
 '/privacy-policy/': ('Privacy Policy: Aapka Data Kaise Use Hota Hai | autenflo', 'autenflo kaun si jaankari leta hai, kyun leta hai, kitne samay rakhta hai aur kin ke saath share karta hai. Aapke adhikar aur sampark ki details yahan.'),
 '/terms-of-service/': ('Terms of Service: Charges, AI Seema, Cancellation | autenflo', 'autenflo ki service, charges, AI ki seema, payment aur cancellation ke niyam. Shuru karne se pehle ye saari shartein ek baar dhyan se padh lijiye.'),
}
PAGES = {}
BIZ_LD = {'@context': 'https://schema.org', '@type': 'ProfessionalService', '@id': SITE + '/#business', 'name': 'autenflo', 'url': SITE, 'logo': SITE + '/logo.png', 'image': SITE + '/og.png',
          'description': 'AI WhatsApp automation for businesses in Bihar, Uttar Pradesh and Jharkhand: enquiry reply, follow-up, marketing and payment reminders.',
          'sameAs': ['https://www.instagram.com/autenfloai/', 'https://www.linkedin.com/company/autenflo/'], 'email': 'hello@autenflo.com', 'telephone': '+918849031907', 'address': {'@type': 'PostalAddress', 'streetAddress': 'Mishratola, Gannipur', 'addressLocality': 'Muzaffarpur', 'addressRegion': 'Bihar', 'addressCountry': 'IN'},
          'areaServed': [{'@type': 'State', 'name': x} for x in ('Bihar', 'Uttar Pradesh', 'Jharkhand')], 'parentOrganization': {'@type': 'Organization', '@id': SITE + '/#organization'}}

def page(path, title, desc, main, jsonld=(), extra_js=(), og='website', noindex=False, crumbs=None, image=None):
    if noindex: NOINDEX.add(path)
    url = SITE + '/' + path.replace('index.html', '').lstrip('/')
    ov = SEO_OV.get('/' + path.replace('index.html', '').lstrip('/'))
    if ov: title, desc = ov[0] or title, ov[1] or desc
    PAGES[url] = (title, desc)
    if '<article' not in main: main = re.sub(r'(<main[^>]*>)(.*)(</main>)', r'\1<article>\2</article>\3', main, count=1, flags=re.S)
    jl = list(jsonld) + ([crumbs_ld(crumbs)] if crumbs else []) + ([] if noindex else [BIZ_LD])
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jl)
    js = ''.join(f'<script defer src="{s}"></script>' for s in ('/assets/site.js', *extra_js))
    rb = '<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    img = image or SITE + '/og.png'
    html = (f'<!doctype html>\n<html lang="hi-Latn"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'{rb}<title>{E(title)}</title><meta name="description" content="{E(desc, quote=True)}"><link rel="canonical" href="{url}"><link rel="icon" href="/logo.png">'
            f'<meta name="theme-color" content="#ffffff"><meta property="og:type" content="{og}"><meta property="og:site_name" content="autenflo"><meta property="og:title" content="{E(title, quote=True)}">'
            f'<meta property="og:description" content="{E(desc, quote=True)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{img}"><meta property="og:locale" content="hi_IN"><meta name="twitter:card" content="summary_large_image">'
            f'<meta name="twitter:title" content="{E(title, quote=True)}"><meta name="twitter:description" content="{E(desc, quote=True)}"><meta name="twitter:image" content="{img}">'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" media="print" onload="this.media=\'all\'"><noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet"></noscript><script>document.documentElement.className="js"</script>'
            f'<link rel="stylesheet" href="/assets/style.css">{ld}'
            '<script async src="https://www.googletagmanager.com/gtag/js?id=G-6012ZHG9SS"></script>'
            "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-6012ZHG9SS');</script></head>\n"
            f'<body>{SPRITE}'
            '<a class="ann" href="/#plans"><mark class="stx">Startups</mark> ke liye khaas offer: har plan ke saath <b>FREE Branding Consulting</b> →</a>'
            f'{HEADER}\n{main}\n{FOOTER}{FAB}{js}</body></html>')
    write(path, html)
    return url

def hero_art(a, b, label):
    rows = (('11:47 PM', 'Enquiry aayi, 3 second me reply'), ('11:48 PM', 'Quotation aur payment link gaya'), ('Din 1-3-7', 'Follow-up khud chala'), ('Roz shaam', 'Aaj ka hisaab taiyar'))
    return (f'<div class="hart" role="img" aria-label="{label}"><div class="hart-top"><span>Aaj ka khata</span><span>staff: 0</span></div><div class="hart-rows">'
            + ''.join(f'<div><time>{t}</time><span>{x}</span></div>' for t, x in rows)
            + '</div><div class="hart-sum">Aap bas deal close karo.</div></div>')

PROBLEMS = [
    ('💬', 'Enquiry ka reply late jata hai', 'Har source ki enquiry ek jagah, turant reply, 24x7.'),
    ('🔥', 'Hot leads ka follow-up chhoot jata hai', '1, 3 aur 7 din par auto follow-up, aur hot lead par seedha alert.'),
    ('📣', 'Marketing aur social media regular nahi', 'Posts, posters aur videos ka calendar, aur sabhi social channels par auto-post.'),
    ('🧾', 'Payment aur hisaab bikhra rehta hai', 'Payment reminder, bill ki photo se entry aur invoice.'),
    ('⚙️', 'Manual kaam me time jata hai', 'Order, data entry, task aur report ka roz ka kaam AI se.'),
]
STEPS = [('Aap apne processes batate ho', 'Business, team aur roz ke kaam ke baare me batate ho.'), ('Hum setup karte hain', 'Follow-up, data entry, billing, reminders aur reports, sab online.'), ('AI kaam karta hai, aap deal close karte ho', 'Har mahine ek simple report aur zaroorat par tuning.')]
BIZ = ['D2C & Retail', 'Coaching & Schools', 'Clinics & Diagnostics', 'Real Estate', 'Transport & Logistics', 'Professional Services & Agencies']
PLANS = [
    ('Launch', 'For Startups', '14,999', '5,999', ['Free Website Revamp', f'3 Days {AI} Training to Staff @ ₹999', 'Free Social Media Starter Package']),
    ('Accelerate', 'For Growing Businesses', '24,999', '9,999', ['Free Website', f'Free {AI} Training to Staff', 'Free Social Media Package']),
    ('Titan', 'For Established Businesses', '44,999', '17,999', ['Free Website', f'Free {AI} Training to Staff', 'Free Social Media Package']),
]

# Home page ka poora pricing block (plans, comparison, service table, monthly charge). Home me badlo, city pages me apne aap aa jata hai.
_H = R('home.html')
PRICING = _H[_H.index('<!--pricing-->') + len('<!--pricing-->'):_H.index('<!--/pricing-->')]

# autenflo ke saare solutions, process ke hisaab se
SOLUTIONS = [
    ('Sales', 'Har lead ko 60 second me reply. Phir 1, 3 aur 7 din par follow-up, khud.',
     ['Har enquiry ek jagah, ek bhi nahi chhooti', 'Quotation aur catalogue turant bhejta hai', 'Hot lead par aapko seedha alert']),
    ('Marketing & Social Media (add-on)', 'Poore mahine ke posts, reels aur videos ek baar me. Hindi captions, design aur auto-posting.',
     ['Posts, posters aur Hindi captions aapke business ke andaaz me', 'Reels aur videos: idea, script aur editing, schedule ke saath', 'Sabhi social channels par auto-post, plus report ki kya chala']),
    ('Operations', 'Order aate hi record. Stock kam hote hi alert. Kaam seedha sahi insaan ke paas.',
     ['Order apne aap record', 'Stock khatam hone se pehle alert', 'Kaam staff ko auto assign, status track']),
    ('Customer service', f'24x7 reply, Hindi me, aapke andaaz me. Jo {AI} na sambhaal paye, wo seedha aapko.',
     [f'{AI} assistant, 24x7', 'Catalogue, price aur FAQ ka turant jawab', 'Zaroori baat par turant aapko forward']),
    ('Finance', 'Reminder tameez se, khud. Bill ki photo se entry. Har shaam aaj ka hisaab.',
     ['Due date par polite payment reminder', 'Bill ki photo se data entry aur tax details', 'Roz shaam kamai aur baaki ka summary']),
    ('Training', f'Schools, Colleges aur Institutions ke liye {AI} Training.',
     ['Daily 1 ghante ki live online class', 'Schools, colleges, ITIs, workplaces aur private/govt institutions ke liye', 'Schools ₹6,999, Colleges ₹9,999, Others ₹8,999 per month']),
]

def faq_list(n):
    return [
        (f'autenflo {n} ke business ke liye kya karta hai?', f'autenflo {n} ke business ko AI ki power deta hai: enquiry ka turant reply, hot leads ka follow-up, marketing aur social media posts aur videos, payment reminder aur hisaab me madad. Ye sab automatic chalta hai, 24x7.'),
        (f'Kya {n} me setup ke liye office aana padta hai?', 'Nahi. Poora setup online hota hai. Aap apne processes batate ho, baaki kaam hum sambhalte hain.'),
        ('Shuruaat kitne se hoti hai?', 'Launch plan ki one-time installation ₹14,999 aur monthly charge ₹5,999 se shuru hota hai. Messaging platform, API aur AI usage ka kharcha aapke apne account se jata hai.'),
        ('Kya customer se Hindi me baat hoti hai?', 'Haan, Hindi me aur zaroorat par English me. Jahan insaan ki zaroorat ho, wahan baat seedha aap ya aapke staff tak pahunch jaati hai.'),
    ]

from city_data import CITY


def ans_block(lead, parts, lo=40, hi=60):
    t, last = lead, lead
    for p in parts:
        t = (t + ' ' + p).strip()
        n = len(t.split())
        if n > hi: return last if len(last.split()) >= lo else t
        last = t
        if n >= lo: return t
    return last

def city_page(c):
    n, st = c['name'], c['state']; s = states[st]; sn = STATE_NAME[st]; d = CITY[c['slug']]
    url = SITE + u_city(c['slug'])
    CR = [('Home', '/'), ('Cities', U_CITIES), (sn, u_state(st)), (n, u_city(c['slug']))]
    msg = WA(f'Namaste autenflo, main {n} se hu. Mujhe apne business ko AI ki power chahiye.')
    near = [x for x in cities if x['state'] == st and x['slug'] != c['slug']][:4]
    b0, b1, b2 = d['biz']
    faq = [d['faq'], faq_list(n)[2],
           (f'{n} me AI WhatsApp automation kin businesses ke liye sabse zyada kaam aata hai?', f'{n} me {b0[0]}, {b1[0]} aur {b2[0]} jaise businesses ko sabse zyada fayda milta hai, kyunki inme enquiry, appointment aur payment ka kaam roz hota hai aur aksar manual rehta hai.'),
           (f'{n} ke {b0[0]} business ko autenflo kaise madad karta hai?', f'{b0[1]} {b0[2]}'),
           (f'{n} ke {b1[0]} business ko autenflo kaise madad karta hai?', f'{b1[1]} {b1[2]}'),
           (f'{n} me AI ko kab ON karna sabse faydemand hai?', d['season'])]
    leak = ans_block(f'{n} ke business me paisa teen jagah leak hota hai.', [x[1] for x in d['biz']] + [x[2] for x in d['biz']])
    pricing = PRICING.replace('text=Namaste%20autenflo%2C%20mujhe%20', 'text=' + U.quote(f'Namaste autenflo, main {n} se hu. Mujhe '))
    sol = ''.join(f'<article class="glass bz"><span class="tg2">{t}</span><h3>{h}</h3><ul class="sl">' + ''.join(f'<li>{x}</li>' for x in li) + '</ul>' + ('<p style="margin-top:14px"><a class="ul" href="' + U_TRAIN + '">Plans dekhein →</a></p>' if t.startswith('Training') else '') + '</article>' for t, h, li in SOLUTIONS)
    t1, t2 = d['biz'][0][0], d['biz'][1][0]
    offer = ('<div class="offer glass"><span class="gi">FREE</span><div><b><mark class="stx">Startups</mark> ke liye khaas offer</b><p>Har plan ke saath <strong>FREE Branding Consulting</strong>.</p></div></div>' if st == 'bihar' else '')
    cards = ''.join(f'<article class="glass bz"><span class="em">{e}</span><h3>{E(t)}</h3><p class="fx1"><b>Problem:</b> {E(l)}</p><p class="fx1"><b>autenflo:</b> {E(f)}</p></article>' for (t, l, f), e in zip(d['biz'], ('01', '02', '03')))
    areas = ''.join(f'<span>{E(a)}</span>' for a in d['areas'])
    main = f"""<main id="top"><section class="chero"><div class="wrap">{crumbs_html(CR)}<div class="chg"><div><span class="eyebrow">{n} · {sn}</span><h1 class="h1s">{city_h1(c["slug"])}</h1><p class="lead">{E(d['hook'])}</p><div class="cta"><a class="btn wab" href="{msg}">{WI}{n} ke liye baat karein</a><a class="btn ghost" href="#plans">Pricing dekhein</a></div></div>{hero_art(s['a'], s['b'], 'autenflo AI ka business setup')}</div></div></section>
<section class="sec"><div class="wrap"><span class="eyebrow">{n} ke business</span><h2 class="wide">{n} ke business me paisa kahan leak hota hai?</h2><p class="sub ans">{E(leak)}</p><div class="g3">{cards}</div></div></section>
<section class="sec" id="solutions"><div class="wrap"><span class="eyebrow">Hamare solutions</span><h2 class="wide">{n} ke business ke poore processes, ek jagah.</h2><p class="sub">Enquiry se payment tak, har manual aur repetitive kaam. Sales, marketing, operations, customer service aur finance, sab hum sambhalte hain, aur institutions ke liye {AI} Training bhi.</p><div class="g3">{sol}</div></div></section>
<section class="sec"><div class="wrap"><span class="eyebrow">{n} ka business calendar</span><h2 class="wide">Kab {AI} ON karna sabse zyada kaam aata hai.</h2><p class="sub">{E(d['season'])}</p></div></section>
<section class="sec"><div class="wrap"><span class="eyebrow">Hum kahan kaam karte hain</span><h2 class="wide">{n} ke in ilaakon ke business ke liye.</h2><div class="chips">{areas}</div></div></section>
<section class="sec" id="plans"><div class="wrap"><span class="eyebrow">Pricing · {n}</span><h2 class="wide">Same kaam ke staff ka kharcha ₹20,000 se ₹85,000 mahina. autenflo ₹5,999 se.</h2>{pricing}</div></section>
<section class="sec fq"><div class="wrap"><span class="eyebrow">Mann me jo sawal hain</span><h2>Pehle ye jaan lijiye</h2>{''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq)}</div></section>
<section class="sec"><div class="wrap"><div class="glass fin2"><div><h2>{n} ke apne business me {AI} lagayein.</h2><p class="sub">Batayiye aapka business kya hai, hum bataenge kaun se manual kaam sabse pehle automate hon.</p></div><a class="btn wab" href="{msg}">{WI}Abhi baat karein</a></div><h3 class="mt2">{sn} ke aur shehar</h3><div class="cgrid">{''.join(f'<a class="cc glass" href="{u_city(x["slug"])}"><div><h3>{x["name"]}</h3><p>{E(CITY[x["slug"]]["biz"][0][0])}</p></div></a>' for x in near)}</div></div></section></main>"""
    seo_t, seo_d = city_seo(c['slug'])
    ld = [{'@context': 'https://schema.org', '@type': 'WebPage', '@id': url, 'url': url, 'name': seo_t, 'description': seo_d, 'inLanguage': 'hi-Latn', 'isPartOf': {'@type': 'WebSite', 'name': 'autenflo', 'url': SITE}},
          {'@context': 'https://schema.org', '@type': 'Service', 'name': f'AI business process automation in {n}', 'serviceType': 'AI business process automation', 'url': url,
           'description': seo_d, 'provider': ORG, 'areaServed': {'@type': 'City', 'name': n, 'containedInPlace': {'@type': 'State', 'name': sn}},
           'offers': {'@type': 'Offer', 'name': 'Launch plan: one-time installation', 'priceCurrency': 'INR', 'price': '14999', 'url': url + '#plans'}},
          {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]}]
    page(fp(u_city(c['slug'])), seo_t, seo_d, main, ld, crumbs=CR)
    return url

def hub_page(st):
    s = states[st]; sn = STATE_NAME[st]; lst = [x for x in cities if x['state'] == st]
    grid = ''.join(f'<a class="cc glass" href="{u_city(x["slug"])}"><div><h3>{x["name"]}</h3><p>Business ke liye AI ki power</p></div></a>' for x in lst)
    CR = [('Home', '/'), ('Cities', U_CITIES), (sn, u_state(st))]
    main = f'''<main id="top"><section class="chero"><div class="wrap">{crumbs_html(CR)}<div class="chg"><div><span class="eyebrow">{sn}</span><h1 class="h1s">{aih(HUB_H1[st])}</h1><p class="lead">{sn} ke {len(lst)} bade shehron me autenflo ka {AI} setup: enquiry ka reply, follow-up, marketing aur payment reminder.</p></div>{hero_art(s['a'], s['b'], 'autenflo AI')}</div><div class="cgrid">{grid}</div></div></section></main>'''
    nl = [x['name'] for x in lst]; inds = []
    for x in lst:
        for b in CITY[x['slug']]['biz']:
            if b[0] not in inds: inds.append(b[0])
    hans = f'{sn} me autenflo {", ".join(nl[:-1])} aur {nl[-1]} me kaam karta hai. Har shehar ke business ke hisaab se alag setup hota hai: enquiry ka turant reply, follow-up, marketing, payment reminder aur data entry, sab WhatsApp par.'
    hfaq = [(f'{sn} me autenflo kin shehron me kaam karta hai?', f'autenflo {sn} ke {len(nl)} shehron me kaam karta hai: {", ".join(nl)}. Setup online hota hai, isliye office aana zaroori nahi.'),
            (f'{sn} ke businesses ke liye AI WhatsApp automation kya karta hai?', 'Ye enquiry ka turant reply deta hai, hot leads ka 1-3-7 din follow-up karta hai, marketing ka content banata hai aur payment reminder bhejta hai. Sab aapke apne WhatsApp number par chalta hai.'),
            (f'{sn} me kaun si industries sabse zyada fayda leti hain?', f'{sn} me {", ".join(inds[:6])} jaise businesses ko sabse zyada fayda milta hai, kyunki inme enquiry aur follow-up ka kaam roz hota hai.'),
            faq_list(sn)[2], faq_list(sn)[1], faq_list(sn)[3]]
    extra = f'<section class="sec"><div class="wrap"><span class="eyebrow">{sn} me AI</span><h2 class="wide">{sn} me AI automation kahan available hai?</h2><p class="sub ans">{E(hans)}</p></div></section><section class="sec fq"><div class="wrap"><span class="eyebrow">Mann me jo sawal hain</span><h2>{sn}: aapke sawal, seedhe jawab</h2>' + ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in hfaq) + '</div></section>'
    main = main.replace('</main>', extra + '</main>')
    t = f'AI Business Automation in {states[st]["short"]} | autenflo'
    d = f'{states[st]["short"]} ke {len(lst)} shehron ({", ".join(x["name"] for x in lst[:3])} aur aage) me AI process automation: sales, marketing, operations, finance. ₹14,999 se.'
    hu = SITE + u_state(st)
    ld = [{'@context': 'https://schema.org', '@type': 'CollectionPage', '@id': hu, 'url': hu, 'name': t, 'description': d, 'inLanguage': 'hi-Latn', 'isPartOf': {'@type': 'WebSite', 'name': 'autenflo', 'url': SITE},
           'mainEntity': {'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i, 'name': x['name'], 'url': SITE + u_city(x['slug'])} for i, x in enumerate(lst, 1)]}}]
    ld.append({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in hfaq]})
    return page(fp(u_state(st)), t, d, main, ld, crumbs=CR)

def cities_index():
    CRI = [('Home', '/'), ('Cities', U_CITIES)]
    blocks = ''.join(f'<div class="wrap stsec"><h2><a href="{u_state(k)}">{STATE_NAME[k]}</a></h2><div class="cgrid">' + ''.join(f'<a class="cc glass" href="{u_city(x["slug"])}"><div><h3>{x["name"]}</h3><p>Business ke liye AI ki power</p></div></a>' for x in cities if x['state'] == k) + '</div></div>' for k in states)
    main = f'<main id="top" class="sec"><div class="wrap">{crumbs_html(CRI)}<span class="eyebrow">Aapka shehar</span><h1 class="h1s">{aih("Apna shehar chuniye, dekhiye AI aapke business me kya badlega.")}</h1><p class="sub">Bihar, Purvanchal aur Jharkhand ke shehron me autenflo ka {AI} setup. Apna shehar chuniye.</p></div>{blocks}</main>'
    cnt = {k: sum(1 for x in cities if x['state'] == k) for k in states}
    ia = f'autenflo {len(cities)} shehron me kaam karta hai: ' + ', '.join(f'{STATE_NAME[k]} ke {cnt[k]}' for k in states) + '. Setup online hota hai, isliye office aana zaroori nahi. Har shehar ke business ke hisaab se enquiry reply, follow-up, marketing aur payment reminder alag set kiye jate hain, sab WhatsApp par.'
    cf = [('AI automation kin states aur shehron me available hai?', f'Bihar ke {cnt["bihar"]}, Uttar Pradesh ke {cnt["uttar-pradesh"]} aur Jharkhand ke {cnt["jharkhand"]} shehron me, yaani kul {len(cities)} shehron me. Setup online hota hai.'),
          ('Kaun si industries ke liye AI automation hai?', 'D2C aur retail (garments, jewellery, mobile), coaching aur schools, clinics aur diagnostics, real estate, transport aur logistics, aur professional services aur agencies ke liye. Har industry ka alag page hai.'),
          ('Agar mera shehar list me nahi hai to?', 'Setup online hota hai, isliye aap kisi bhi shehar se shuru kar sakte hain. Hum aapke business ka process dekhkar bata dete hain ki kya aur kaise automate hoga.'),
          faq_list('Bihar')[2], faq_list('Bihar')[1], faq_list('Bihar')[3]]
    main = main.replace('</main>', f'<section class="sec"><div class="wrap"><span class="eyebrow">Hamare shehar</span><h2 class="wide">autenflo kin shehron me kaam karta hai?</h2><p class="sub ans">{E(ia)}</p></div></section><section class="sec fq"><div class="wrap"><span class="eyebrow">Mann me jo sawal hain</span><h2>Shehron ke baare me sawal, seedhe jawab</h2>' + ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in cf) + '</div></section></main>')
    t = 'AI Business Automation in Bihar, UP, Jharkhand | autenflo'
    d = f'Bihar, Lucknow se Purvanchal aur Jharkhand ke {len(cities)} shehron me business ke liye AI process automation: sales, marketing, operations, finance.'
    cu = SITE + U_CITIES
    ld = [{'@context': 'https://schema.org', '@type': 'CollectionPage', '@id': cu, 'url': cu, 'name': t, 'description': d, 'inLanguage': 'hi-Latn', 'isPartOf': {'@type': 'WebSite', 'name': 'autenflo', 'url': SITE},
           'mainEntity': {'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i, 'name': x['name'], 'url': SITE + u_city(x['slug'])} for i, x in enumerate(cities, 1)]}}]
    ld.append({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': x}} for q, x in cf]})
    return page(fp(U_CITIES), t, d, main, ld, crumbs=CRI)

# ---------- blog ----------
from blog_data import POSTS, OLD_POST_REDIRECT
BLOG_IMG = lambda slug: f'/assets/blog/{slug}.webp'
POST_BY = {p['slug']: p for p in POSTS}
def u_post(slug): return f'/blog/{slug}/'
def _wc(h): return len(re.sub(r'<[^>]+>', ' ', h).split())
def _body_toc(body):
    heads = re.findall(r'<h2>(.*?)</h2>', body)
    for i, h in enumerate(heads, 1): body = body.replace(f'<h2>{h}</h2>', f'<h2 id="s{i}">{h}</h2>', 1)
    toc = '<nav class="toc" aria-label="Is article me"><b>Is article me</b><ol>' + ''.join(f'<li><a href="#s{i}">{h}</a></li>' for i, h in enumerate(heads, 1)) + '</ol></nav>'
    return body, toc
def _related(p):
    same = [q for q in POSTS if q['kw'] == p['kw'] and q['slug'] != p['slug']]
    idx = POSTS.index(p)
    others = [POSTS[(idx + k) % len(POSTS)] for k in (2, 5, 9)]
    out = same + [q for q in others if q['slug'] != p['slug'] and q not in same]
    return out[:3]

def blog_pages():
    urls = [SITE + U_BLOG]
    CRB = [('Home', '/'), ('Blog', U_BLOG)]
    cards = ''
    for p in POSTS:
        url = SITE + u_post(p['slug']); urls.append(url)
        img = SITE + BLOG_IMG(p['slug'])
        CR = [('Home', '/'), ('Blog', U_BLOG), (p['title'], u_post(p['slug']))]
        body, toc = _body_toc(p['body'])
        faq = ''.join(f'<details class="pfq"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in p['faq'])
        rel = ''.join(f'<a class="rc" href="{u_post(q["slug"])}"><span class="meta">{E(q["cat"])}</span><b>{E(q["title"])}</b></a>' for q in _related(p))
        words = _wc(p['answer']) + _wc(p['body']) + sum(_wc(q + ' ' + a) for q, a in p['faq'])
        p['_words'] = words
        main = f'''<main id="top" class="sec"><div class="wrap">{crumbs_html(CR)}
<article><header class="post-head"><p class="meta">{E(p['cat'])} · {p['dlabel']} · {max(4, round(words / 200))} min padhne me</p><h1 class="h1s">{E(p['title'])}</h1><p class="sub">{E(p['desc'])}</p></header>
<figure class="post-fig"><img src="{BLOG_IMG(p['slug'])}" alt="{E(p['alt'], quote=True)}" width="1600" height="900" fetchpriority="high" decoding="async"></figure>
<div class="prose">
<div class="ans"><b>Seedha jawab</b><p>{p['answer']}</p></div>
{toc}
{body}
<h2 class="faqh">Aksar poochhe jaane wale sawal</h2>
{faq}
</div></article>
<aside class="relw" aria-label="Aur padhein"><h2>Ye bhi padhiye</h2><div class="relg">{rel}</div></aside>
<div class="glass fin2"><div><h2>Apne business ka free process audit.</h2><p class="sub">15 minute baat karke dekhiye aapke liye kya sahi rahega.</p></div><a class="btn wab" href="{WA('Namaste autenflo, maine aapka blog padha. Mujhe free process audit chahiye.')}">{WI}Abhi baat karein</a></div></div></main>'''
        ld = [{'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': p['title'], 'description': p['desc'], 'datePublished': p['date'], 'dateModified': p['date'], 'inLanguage': 'hi-Latn',
               'image': [img], 'url': url, 'wordCount': words, 'keywords': p['kw'], 'articleSection': p['cat'], 'mainEntityOfPage': {'@type': 'WebPage', '@id': url},
               'author': ORG, 'publisher': {'@type': 'Organization', 'name': 'autenflo', 'url': SITE, 'logo': {'@type': 'ImageObject', 'url': SITE + '/logo.png'}}},
              {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in p['faq']]}]
        page(fp(u_post(p['slug'])), p['seo_title'], p['desc'], main, ld, og='article', crumbs=CR, image=img)
        cards += f'<a class="bc glass" href="{u_post(p["slug"])}"><img src="{BLOG_IMG(p["slug"])}" alt="{E(p["alt"], quote=True)}" width="1600" height="900" loading="lazy" decoding="async"><div><p class="meta">{E(p["cat"])} · {p["dlabel"]}</p><h3>{E(p["title"])}</h3><p>{E(p["desc"])}</p></div></a>'
    main = f'''<main id="top" class="sec"><div class="wrap">{crumbs_html(CRB)}<span class="eyebrow">Blog</span><h1 class="h1s">Leads, follow-up aur reply: seedhi bhasha me.</h1><p class="sub">Practical articles: WhatsApp reply, follow-up, templates, clinic, coaching, real estate aur AI training. Sawal ka seedha jawab, copy-paste templates ke saath.</p>
<div class="bgrid">
{cards}
</div></div></main>'''
    bt, bd = 'Business, AI aur Marketing Tips | autenflo Blog', 'Chhote business ke liye WhatsApp reply, follow-up, billing aur AI ke practical tareeke, Hindi me. Message templates, checklists aur seedhe jawab ke saath.'
    bl = SITE + U_BLOG
    bld = [{'@context': 'https://schema.org', '@type': 'Blog', '@id': bl, 'url': bl, 'name': 'autenflo Blog', 'description': bd, 'inLanguage': 'hi-Latn', 'publisher': ORG,
            'blogPost': [{'@type': 'BlogPosting', 'headline': p['title'], 'url': SITE + u_post(p['slug']), 'datePublished': p['date'], 'image': SITE + BLOG_IMG(p['slug'])} for p in POSTS]}]
    page(fp(U_BLOG), bt, bd, main, bld, crumbs=CRB)
    return urls

# ---------- trust pages: about, privacy, terms ----------
def trust_pages():
    cta = f'<div class="glass fin2"><div><h2>Pehle free process audit, phir baat.</h2><p class="sub">15 minute me aapke manual aur repetitive kaam gin kar batate hain.</p></div><a class="btn wab" href="{WA("Namaste autenflo, mujhe free process audit chahiye")}">{WI}Abhi baat karein</a></div>'
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
<p>autenflo Muzaffarpur, Bihar se chalta hai. Hum chhote aur beech ke business ke liye AI se manual aur repetitive processes (data entry, follow-up, billing, reminders, reports aur marketing) automate karte hain, aur Hindi me, aapke saath baith kar setup karte hain.</p>
<h2>Hum kaise kaam karte hain</h2>
<ul><li><b>Pehle free process audit:</b> aapke manual aur repetitive kaam gin kar batate hain ki kitna time aur paisa ja raha hai.</li><li><b>Phir pehla kaam:</b> ek kaam, ek tay metric, end me result report.</li><li><b>Saaf kharcha:</b> hamari fees, platform aur API ka kharcha, sab pehle likh kar dete hain.</li><li><b>Likhit agreement:</b> kaam ka scope, data kiska hai, aur band kaise karna hai.</li></ul>
<h2>AI aur insaan</h2>
<p>Aapke customer ko pehle message me hi pata hota hai ki wo AI sahayak se baat kar raha hai. Wo insaan se baat maange to chat seedha aapko ya aapke staff ko jaati hai. Paisa, medical ya complaint jaise sawal AI khud nahi sambhalta.</p>
<h2>Aap kaise sampark karein</h2>
<p>Email: <a href="mailto:hello@autenflo.com">hello@autenflo.com</a><br>Phone: <a href="https://wa.me/918849031907">+91 88490 31907</a><br>Address: Mishratola, Gannipur, Muzaffarpur, Bihar<!-- ✏️ Poora address / registered business name / GST yahan jodein, jab ho --></p>"""
    privacy = """<!-- ⚠️ YE EK SHURUATI DRAFT HAI. Live karne se pehle apne vakeel/CA se India ke DPDP Act 2023 ke hisaab se zaroor confirm karwayein. -->
<p>Antim update: 12 November 2026</p>
<h2>Hum kya jaankari lete hain</h2>
<p>Website ke form me aap naam, phone number aur business ki jaankari dete hain. Aap jo message bhejte hain, wo bhi hum dekhte hain. Website par Google Analytics se anonymous visit data (kaun sa page, kitni der) liya jata hai.</p>
<h2>Hum ise kyun use karte hain</h2>
<p>Aapse baat karne, demo dikhane, service dene, aur website behtar karne ke liye. Hum aapki jaankari bechte nahi.</p>
<h2>Kin ke saath share hota hai</h2>
<p>Sirf un tools ke saath jo kaam ke liye zaroori hain: messaging platform providers, AI aur automation tools, Google Analytics, aur website form ka hosting provider. Client ke customers ka data client ke agreement ke hisaab se hi handle hota hai.</p>
<h2>Kitne din rakhte hain</h2>
<p>Jab tak aapse baat ya service chal rahi hai, aur uske baad zaroori kaam (hisaab, agreement) ke liye jitna chahiye. Aap kabhi bhi jaankari hatane ko keh sakte hain.</p>
<h2>Aapke adhikar</h2>
<p>Aap apni jaankari dekhne, sudharne ya hatane ke liye <a href="mailto:hello@autenflo.com">hello@autenflo.com</a> par likh sakte hain.</p>
<h2>Cookies</h2>
<p>Hum analytics ke liye cookies use karte hain. Browser settings se aap ise rok sakte hain.</p>"""
    terms = """<!-- ⚠️ YE EK SHURUATI DRAFT HAI. Live karne se pehle vakeel se confirm karwayein, aur [ ] wale business-decision (notice period, refund) apne hisaab se tay karein. -->
<p>Antim update: 12 November 2026</p>
<h2>Hamari service</h2>
<p>autenflo AI se business ke repetitive processes (reply, follow-up, entry, reminder, reports aur sambandhit kaam) sambhalta hai, jaisa aapke plan ya agreement me likha ho. Naye kaam ya add-on alag se tay hote hain.</p>
<h2>Charges</h2>
<p>Ek baar ka installation aur monthly charge plan ke hisaab se. Messaging platform aur API ke charges, AI usage aur domain jaise third-party kharche aapke apne account se jaate hain aur hamare charge me shamil nahi hain.</p>
<h2>AI aur uski seema</h2>
<p>AI kabhi-kabhi galat reply de sakta hai. Hum galat jawab ke rules aur insaan tak handover set karte hain aur replies par nazar rakhte hain, par poori guarantee nahi de sakte. Customer ko AI sahayak hone ki baat saaf dikhaai jaati hai.</p>
<h2>Aapki zimmedari</h2>
<p>Aap sahi jaankari (rate, offer, FAQ) dete hain, aur sirf un logon ko message bhejte hain jinhone sampark kiya ho ya jinki anumati ho. Platform ke niyam todne par account ban ho sakta hai, jiske liye hum zimmedar nahi honge.</p>
<h2>Data</h2>
<p>Aapke business aur customers ka data aapka hai. Hum use sirf service dene ke liye use karte hain.</p>
<h2>Band karna</h2>
<p>Koi lamba contract nahi. Aap [30 din ke notice] par service band kar sakte hain. Us mahine tak ka monthly charge lagta hai. [Refund ka niyam yahan likhein.]</p>
<h2>Seema aur kanoon</h2>
<p>Hamari zimmedari us mahine ke monthly charge tak seemit rahegi. Ye shartein Bharat ke kanoon ke adheen hain. [Vivad ke liye adhikar-kshetra: Muzaffarpur, Bihar.]</p>
<h2>Sampark</h2>
<p><a href="mailto:hello@autenflo.com">hello@autenflo.com</a></p>"""
    return [shell(U_ABOUT, 'About', aih('Hum kaun hain: Hindi me, aapke saath baith kar AI lagate hain.'), 'Seedhi baat: hum kya karte hain, kaise karte hain, aur kya nahi karte.', about, 'About autenflo | AI Back-office for Business, Patna, Bihar', 'autenflo Muzaffarpur, Bihar se chalta hai: AI se sales, marketing, operations, finance aur customer service ke manual kaam automate. Pehle free 15 minute ka audit.', 'AboutPage'),
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
    org = {'@context': 'https://schema.org', '@type': 'Organization', '@id': SITE + '/#organization', 'name': 'autenflo', 'url': SITE, 'logo': SITE + '/logo.png', 'sameAs': ['https://www.instagram.com/autenfloai/', 'https://www.linkedin.com/company/autenflo/'], 'email': 'hello@autenflo.com',
           'description': 'AI se sales, marketing, operations, finance aur customer service ke manual kaam automate: chhote aur beech ke business ke liye, Hindi me.',
           'address': {'@type': 'PostalAddress', 'streetAddress': 'Mishratola, Gannipur', 'addressLocality': 'Muzaffarpur', 'addressRegion': 'Bihar', 'addressCountry': 'IN'},
           'contactPoint': [{'@type': 'ContactPoint', 'contactType': 'customer support', 'telephone': '+91-88490-31907', 'email': 'hello@autenflo.com', 'availableLanguage': ['Hindi', 'English']}],
           'areaServed': [{'@type': 'State', 'name': 'Bihar'}, {'@type': 'State', 'name': 'Uttar Pradesh'}, {'@type': 'State', 'name': 'Jharkhand'}]}
    site = {'@context': 'https://schema.org', '@type': 'WebSite', '@id': SITE + '/#website', 'name': 'autenflo', 'url': SITE, 'inLanguage': 'hi-Latn', 'publisher': {'@id': SITE + '/#organization'}}
    ld = [org, site] + ([f] if (f := _faq_ld(home)) else [])
    page('index.html', 'autenflo: AI Business Automation for Bihar, UP, Jharkhand', 'Naya staff nahi, agency nahi, manual work nahi. Aapke business ka AI back-office: enquiry se payment tak har repetitive process automate. Free 15 minute process audit.', home, ld, ('/assets/home.js',))
    CRT = [('Home', '/'), ('AI Training', U_TRAIN)]
    tr = R('training.html').replace('<div class="hv">', '<div class="hv"><div class="tart">' + LEARN + '</div>').replace('<div class="hl">', '<div class="hl">' + crumbs_html(CRT), 1)
    tu = SITE + U_TRAIN
    tld = [{'@context': 'https://schema.org', '@type': 'Service', 'name': 'AI Training for Schools, Colleges and Institutions', 'url': tu, 'serviceType': 'Live online AI training', 'provider': ORG,
            'areaServed': {'@type': 'Country', 'name': 'India'},
            'description': 'Daily 1 ghante ki live online AI class, Hindi me, schools, colleges, ITIs, workplaces aur institutions ke liye.',
            'offers': [{'@type': 'Offer', 'name': n, 'price': pr, 'priceCurrency': 'INR', 'description': 'per month', 'url': tu} for n, pr in (('Schools', '6999'), ('Colleges', '9999'), ('Others', '8999'))]}]
    page(fp(U_TRAIN), 'AI Training for Schools, Colleges & ITIs | autenflo', 'Daily 1 ghante ki live online AI class: Schools ₹6,999, Colleges ₹9,999, Others ₹8,999 per month. ITIs, workplaces aur institutions ke liye.', tr, tld, crumbs=CRT)
    return [SITE + '/', tu]

from industry_data import IND
U_IND = '/ai-automation-for-businesses/'

def industry_page(k):
    d = IND[k]; url = SITE + d['u']; nm = d['name']
    CR = [('Home', '/'), ('Industries', U_IND), (nm, d['u'])]
    msg = WA(f'Namaste autenflo, mera business {nm} me hai. Mujhe AI ki power chahiye.')
    h1 = d['h1'].replace('{AI}', AI)
    probs = ''.join(f'<article class="glass bz"><span class="em">{i:02d}</span><h3>{E(h)}</h3><p class="fx1"><b>Problem:</b> {E(p)}</p><p class="fx1"><b>autenflo:</b> {E(f)}</p></article>' for i, (h, p, f) in enumerate(d['probs'], 1))
    uses = ''.join(f'<li>{E(x)}</li>' for x in d['uses'])
    tbl = ''.join(f'<tr><td>{E(h)}</td><td>{E(f)}</td></tr>' for h, p, f in d['probs'])
    u_ = [x.lower() for x in d['uses']]
    ans = f'{nm} me {AI} WhatsApp par ye kaam khud karta hai: {u_[0]}, {u_[1]} aur {u_[2]}. Jahan insaan ki zaroorat ho, wahan baat seedha aap ya aapke staff tak pahunchti hai.'
    q, a = d['chat']
    near = ''.join(f'<a class="cc glass" href="{u_city(x)}"><div><h3>{E(next(c["name"] for c in cities if c["slug"] == x))}</h3><p>{E(nm)} ke liye AI</p></div></a>' for x in d['cities'])
    other = ''.join(f'<a class="cc glass" href="{v["u"]}"><div><h3>{E(v["name"])}</h3><p>AI se kya solve hota hai</p></div></a>' for kk, v in IND.items() if kk != k)
    faq = ''.join(f'<details><summary>{E(x)}</summary><p>{E(y)}</p></details>' for x, y in d['faq'])
    main = f"""<main id="top"><section class="chero"><div class="wrap">{crumbs_html(CR)}<div><span class="eyebrow">{E(nm)}</span><h1 class="h1s">{h1}</h1><p class="lead">{E(d['lead'])}</p><div class="cta"><a class="btn wab" href="{msg}">{WI}Free audit ke liye baat karein</a><a class="btn ghost" href="#plans">Pricing dekhein</a></div></div></div></section>
<section class="sec"><div class="wrap"><span class="eyebrow">Ye page kis ke liye hai</span><h2 class="wide">{E(nm)} me kaam kahan atakta hai?</h2><p class="sub ans">{E(d['intro'])}</p></div></section>
<section class="sec"><div class="wrap"><span class="eyebrow">{len(d['probs'])} badi problems</span><h2 class="wide">Problem aur uska {AI} wala hal.</h2><div class="g3">{probs}</div><h3 class="mt2">Manual tareeka vs autenflo {AI}</h3><div class="tw"><table class="tbl"><caption class="eyebrow">{E(nm)}: kaam kaise badalta hai</caption><tr><th scope="col">Problem</th><th scope="col">autenflo {AI} se</th></tr>{tbl}</table></div></div></section>
<section class="sec"><div class="wrap"><span class="eyebrow">AI kahan lagta hai</span><h2 class="wide">{E(nm)} me {AI} kya kaam karta hai?</h2><p class="sub ans">{ans}</p><ul class="sl">{uses}</ul><div class="glass bz" style="margin-top:18px"><h3>Ek asli chat ka namuna</h3><p class="fx1"><b>Customer:</b> {E(q)}</p><p class="fx1"><b>{AI} assistant:</b> {E(a)}</p></div></div></section>
<section class="sec" id="plans"><div class="wrap"><span class="eyebrow">Pricing</span><h2 class="wide">{E(nm)} ke liye {AI} ka kharcha kitna aata hai?</h2><p class="sub ans">Launch plan ki one-time installation 14,999 rupaye aur monthly charge 5,999 rupaye se shuru hota hai. Accelerate aur Titan plan me zyada process jude hote hain. Messaging platform, API aur AI usage ka kharcha aapke apne account se jata hai.</p>{PRICING}</div></section>
<section class="sec fq"><div class="wrap"><span class="eyebrow">Mann me jo sawal hain</span><h2>{E(nm)}: 10 sawal, 10 jawab</h2>{faq}</div></section>
<section class="sec"><div class="wrap"><div class="glass fin2"><div><h2>Apne {E(nm)} me {AI} lagayein.</h2><p class="sub">Batayiye aapka business kya hai, hum bataenge kaun se manual kaam sabse pehle automate hon.</p></div><a class="btn wab" href="{msg}">{WI}Abhi baat karein</a></div><h3 class="mt2">In shehron me bhi</h3><div class="cgrid">{near}</div>{('<h3 class="mt2">Aur industries</h3><div class="cgrid">' + other + '</div>') if other else ''}</div></section></main>"""
    ld = [{'@context': 'https://schema.org', '@type': 'WebPage', '@id': url, 'url': url, 'name': d['title'], 'description': d['desc'], 'inLanguage': 'hi-Latn', 'isPartOf': {'@type': 'WebSite', 'name': 'autenflo', 'url': SITE}},
          {'@context': 'https://schema.org', '@type': 'Service', 'name': f'AI WhatsApp automation for {nm}', 'serviceType': 'AI business process automation', 'url': url, 'description': d['desc'], 'provider': ORG,
           'areaServed': [{'@type': 'State', 'name': x} for x in ('Bihar', 'Uttar Pradesh', 'Jharkhand')],
           'offers': {'@type': 'Offer', 'name': 'Launch plan: one-time installation', 'priceCurrency': 'INR', 'price': '14999', 'url': url + '#plans'}},
          {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': x, 'acceptedAnswer': {'@type': 'Answer', 'text': y}} for x, y in d['faq']]}]
    page(fp(d['u']), d['title'], d['desc'], main, ld, crumbs=CR)
    return url

def industries_index():
    CR = [('Home', '/'), ('Industries', U_IND)]
    cards = ''.join(f'<a class="cc glass" href="{v["u"]}"><div><h3>{E(v["name"])}</h3><p>{E(v["probs"][0][0])}; {E(v["probs"][1][0])}</p></div></a>' for v in IND.values())
    main = f"""<main id="top"><section class="chero"><div class="wrap">{crumbs_html(CR)}<span class="eyebrow">Industries</span><h1 class="h1s">Aapke business ke liye {AI}: industry ke hisaab se.</h1><p class="lead">Har industry ki apni problem hoti hai. Apni industry chuniye aur dekhiye {AI} wahan kya solve karta hai.</p></div></section>
<section class="sec"><div class="wrap"><div class="cgrid">{cards}</div></div></section></main>"""
    t, dsc = 'Industries ke liye AI WhatsApp Automation | autenflo', 'Coaching, clinics aur aur business ke liye AI WhatsApp automation: har industry ki problem aur uska hal. Bihar, UP, Jharkhand.'
    page(fp(U_IND), t, dsc, main, [], crumbs=CR)
    return SITE + U_IND

if __name__ == '__main__':
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT + '/assets')
    write('assets/style.css', R('global.css') + '\n' + R('extra.css'))
    write('assets/site.js', 'var y=document.getElementById("yr");if(y)y.textContent=new Date().getFullYear();document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("a[href*=\'wa.me\']");if(a&&window.gtag)gtag("event","whatsapp_click",{page_path:location.pathname,link_text:(a.textContent||"").trim().slice(0,40)})});var mi=[].slice.call(document.querySelectorAll(".mi"));function mc(x){mi.forEach(function(m){if(m!==x){m.classList.remove("open");m.querySelector(".mt").setAttribute("aria-expanded","false")}})}mi.forEach(function(m){var b=m.querySelector(".mt");b.addEventListener("click",function(e){var o=(matchMedia("(hover:hover)").matches&&e.detail>0)?true:!m.classList.contains("open");mc(m);m.classList.toggle("open",o);b.setAttribute("aria-expanded",o)});m.addEventListener("mouseenter",function(){if(matchMedia("(hover:hover)").matches){mc(m);m.classList.add("open");b.setAttribute("aria-expanded","true")}});m.addEventListener("mouseleave",function(){if(matchMedia("(hover:hover)").matches){m.classList.remove("open");b.setAttribute("aria-expanded","false")}});m.addEventListener("focusout",function(e){if(!m.contains(e.relatedTarget)){m.classList.remove("open");b.setAttribute("aria-expanded","false")}})});document.addEventListener("keydown",function(e){if(e.key==="Escape")mc(null)});document.addEventListener("click",function(e){if(!e.target.closest(".mi"))mc(null)});var f=document.querySelector("form[name=contact]");if(f)f.addEventListener("submit",function(){if(window.gtag)gtag("event","form_submit",{page_path:location.pathname})});')
    write('assets/home.js', R('home.js'))
    shutil.copy(os.path.join(HERE, 'og.png'), os.path.join(OUT, 'og.png'))
    shutil.copytree(os.path.join(HERE, 'blog_images'), os.path.join(OUT, 'assets', 'blog'))
    for lg in ('logo.png', 'logo.webp'):
        if os.path.exists(os.path.join(HERE, lg)): shutil.copy(os.path.join(HERE, lg), os.path.join(OUT, lg))
    urls = home_training() + blog_pages() + [cities_index(), industries_index()] + [industry_page(k) for k in IND] + trust_pages() + [hub_page(k) for k in states] + [city_page(c) for c in cities]
    skip = {SITE + '/' + p.replace('index.html', '').lstrip('/') for p in NOINDEX}
    urls = [u for u in urls if u not in skip]
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>' for u in urls) + '</urlset>')
    bots = ['Googlebot', 'Bingbot', 'GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-User', 'Claude-SearchBot', 'anthropic-ai', 'PerplexityBot', 'Perplexity-User', 'Google-Extended', 'Applebot-Extended', 'CCBot']
    write('robots.txt', ''.join(f'User-agent: {b}\nAllow: /\nDisallow: /404.html\n\n' for b in bots) + f'User-agent: *\nAllow: /\nDisallow: /404.html\n\nSitemap: {SITE}/sitemap.xml\n')
    head = ('# autenflo\n\n> autenflo ek AI back-office service hai (Mishratola, Gannipur, Muzaffarpur, Bihar): WhatsApp par enquiry ka 60 second me reply, 1-3-7 din follow-up, marketing aur social media, payment reminder aur data entry. Bihar, Uttar Pradesh aur Jharkhand ke businesses ke liye. Setup Rs 14,999 se, monthly Rs 5,999 se. Contact: hello@autenflo.com, +91 88490 31907. Instagram: https://www.instagram.com/autenfloai/ LinkedIn: https://www.linkedin.com/company/autenflo/\n\n')
    def sect(title, pred): return f'## {title}\n\n' + ''.join(f'- [{PAGES[u][0]}]({u}): {PAGES[u][1]}\n' for u in urls if u in PAGES and pred(u[len(SITE):])) + '\n'
    isc = lambda p: p.startswith('/ai-whatsapp-automation-') and p.count('-') > 2 and not any(p.endswith(x) for x in ('-bihar/', '-uttar-pradesh/', '-jharkhand/', '-bihar-up-jharkhand/'))
    write('llms.txt', head + sect('Main pages', lambda p: p in ('/', U_TRAIN, U_ABOUT, U_CITIES, U_IND)) + sect('Industries', lambda p: p.startswith('/ai-automation-for-') and p != U_IND) + sect('Blog', lambda p: p.startswith('/blog/')) + sect('Cities', isc) + sect('Policies', lambda p: p in (U_PRIVACY, U_TERMS)) + f'## Full version\n\n- [llms-full.txt]({SITE}/llms-full.txt)\n')
    full = head
    for k, v in IND.items():
        full += f'## {v["name"]} ({SITE}{v["u"]})\n\n{v["lead"]}\n\n### Problems and how autenflo solves them\n\n' + ''.join(f'- {a}: {b} autenflo: {c}\n' for a, b, c in v['probs']) + '\n### FAQ\n\n' + ''.join(f'**{q}**\n{a}\n\n' for q, a in v['faq'])
    write('llms-full.txt', full + sect('All pages', lambda p: True))
    # 404 page
    nf = f'<main id="top" class="sec"><div class="wrap"><span class="eyebrow">404</span><h1 class="h1s">Ye page nahi mila.</h1><p class="sub">Link purana ho sakta hai. Home par jaayein ya apna shehar chuniye.</p><div class="cta"><a class="btn wab" href="/">Home par jaayein</a><a class="btn ghost" href="{U_CITIES}">Sabhi cities</a></div></div></main>'
    page('404.html', 'Page nahi mila | autenflo', 'Ye page nahi mila. autenflo ke home page ya cities page par jaayein.', nf, noindex=True)
    # ---- purane URL -> naye URL (301) ----
    OLD = [('/cities/', U_CITIES), ('/ai-training/', U_TRAIN), ('/about/', U_ABOUT), ('/privacy/', U_PRIVACY), ('/terms/', U_TERMS)]
    OLD += [('/ai-automation-for-retail-shops/', IND['d2c']['u']), ('/ai-automation-for-hotels-and-travel/', IND['transport']['u']), ('/ai-automation-for-wholesale-and-hardware/', U_IND)]
    OLD += [(f'/{k}/', u_state(k)) for k in states] + [(f'/{c["state"]}/{c["slug"]}/', u_city(c['slug'])) for c in cities]
    OLDF = [(f'/blog/{o}.html', u_post(n)) for o, n in OLD_POST_REDIRECT]
    red = ['# 301 redirects: purane URL -> naye SEO URL (Netlify / Cloudflare Pages format)']
    for o, n in OLD: red += [f'{o} {n} 301', f'{o}index.html {n} 301']
    for o, n in OLDF: red += [f'{o} {n} 301', f'{o[:-5]} {n} 301', f'{o[:-5]}/ {n} 301']
    write('_redirects', '\n'.join(red) + '\n')
    ht = ['# 301 redirects (Apache). Agar aap Netlify/Cloudflare Pages par ho to ye file ignore hoti hai, _redirects kaam karti hai.', 'ErrorDocument 404 /404.html', 'Options -Indexes', '']
    for o, n in OLD: ht.append(f'RedirectMatch 301 ^{o}(index\\.html)?$ {n}')
    for o, n in OLDF: ht.append(f'RedirectMatch 301 ^{o.replace(".", chr(92) + ".")}$ {n}'); ht.append(f'RedirectMatch 301 ^{o[:-5]}/?$ {n}')
    write('.htaccess', '\n'.join(ht) + '\n')
    open(os.path.join(HERE, 'redirect-map.csv'), 'w', encoding='utf-8').write('old_url,new_url\n' + ''.join(f'{SITE}{o},{SITE}{n}\n' for o, n in OLD + OLDF))
    write('README.txt', 'logo.png naam se apna logo is folder ke root me (index.html ke saath) daalo.\nSabhi city pages aur state hub pages Google me index hote hain aur sitemap.xml me hain.\nAbout, Privacy, Terms pages me [ ] aur HTML comments wali jagah bhariye aur vakeel se confirm karwayein.\nURL badle hain: purane URL _redirects (Netlify/Cloudflare Pages) ya .htaccess (Apache) se 301 hote hain. Upload ke baad Search Console me naya sitemap.xml submit karein.\n')
    print(len(urls), 'pages,', len(OLD) + len(OLDF), 'redirects')
