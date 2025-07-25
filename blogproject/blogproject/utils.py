import markdown
from bs4 import BeautifulSoup, Tag
import re

def extract_toc(markdown_text):
    html = markdown.markdown(markdown_text)
    soup = BeautifulSoup(html, "html.parser")

    toc = []
    for tag in soup.find_all(re.compile('^h[1-6]$')):
        # Ensure tag is a Tag, not other PageElement type (like NavigableString)
        if not isinstance(tag, Tag):
            continue

        level = int(tag.name[1])
        text = tag.get_text(strip=True)
        # Create slug by removing unwanted chars, trimming, lowering, and replacing spaces with dashes
        slug = re.sub(r'[^\w\s-]', '', text).strip().lower().replace(' ', '-')

        toc.append({
            'level': level,
            'text': text,
            'slug': slug,
        })
    return toc
