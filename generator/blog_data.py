# -*- coding: utf-8 -*-
"""autenflo blog: 20 articles. Naya article jodna ho to blog_posts_*.py me ek entry badhao aur build_site.py dobara chalao."""
from blog_posts_1 import P1
from blog_posts_2 import P2
from blog_posts_3 import P3
from blog_posts_4 import P4
POSTS = P1 + P2 + P3 + P4
from blog_extra import EXTRA
from blog_extra2 import EXTRA2
for _p in POSTS:
    _x = ''.join(e for e in (EXTRA.get(_p['slug']), EXTRA.get(_p['slug'] + '#2'), EXTRA2.get(_p['slug'])) if e)
    if _x:
        _i = _p['body'].rfind('<h2>')
        _p['body'] = _p['body'][:_i] + _x + _p['body'][_i:]
# purane 3 posts ke URL -> naye relevant article par 301
OLD_POST_REDIRECT = [
 ('missed-enquiry-check-khud-kaise-karein', 'whatsapp-par-customer-ko-reply-kaise-dein-rules'),
 ('missed-whatsapp-enquiry-kaise-check-karein-7-din', 'whatsapp-par-customer-ko-reply-kaise-dein-rules'),
 ('follow-up-1-3-7-din-ka-rule', 'follow-up-kab-karein-bina-pareshan-kiye'),
 ('customer-follow-up-1-3-7-din-rule-templates', 'follow-up-kab-karein-bina-pareshan-kiye'),
 ('whatsapp-par-60-second-me-reply', 'whatsapp-customer-reply-ready-templates'),
 ('whatsapp-par-customer-ko-60-second-me-reply-kaise-dein', 'whatsapp-customer-reply-ready-templates'),
]
