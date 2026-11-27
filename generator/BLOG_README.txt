BLOG: 20 articles
- Content: blog_posts_1..4.py (+ blog_extra.py, blog_extra2.py), registry: blog_data.py
- Images: blog_images/*.webp (build_site.py inhe /assets/blog/ me copy karta hai)
- Naya article: blog_posts_4.py me mk(...) entry jodo, image blog_images/<slug>.webp me daalo, phir: python3 build_site.py
- Purane 3 posts hata diye gaye; unke URL 301 se naye articles par jaate hain (OLD_POST_REDIRECT in blog_data.py, _redirects me bhi)
- Output folder: generator/autenflo-site/  (deploy ke liye upar wala autenflo-site/ use karein)
