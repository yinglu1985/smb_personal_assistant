#!/usr/bin/env python3
"""
Extract business information from Shamrock Day Spa website using Playwright
"""

import json
from playwright.sync_api import sync_playwright

def extract_shamrock_info():
    """Extract all content from Shamrock Day Spa website"""

    url = "https://www.shamrockdayspaservice.com/"

    with sync_playwright() as p:
        print("🌐 Launching browser...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        page = context.new_page()

        print(f"📄 Loading {url}...")
        page.goto(url, wait_until='domcontentloaded', timeout=30000)
        page.wait_for_timeout(3000)  # Wait for Wix to render

        print("🔍 Extracting content...")

        # Extract all visible text content
        data = page.evaluate("""() => {
            // Get all text content
            const bodyText = document.body.innerText;

            // Try to find specific elements
            const h1s = Array.from(document.querySelectorAll('h1')).map(h => h.innerText);
            const h2s = Array.from(document.querySelectorAll('h2')).map(h => h.innerText);
            const h3s = Array.from(document.querySelectorAll('h3')).map(h => h.innerText);
            const paragraphs = Array.from(document.querySelectorAll('p')).map(p => p.innerText);

            // Try to find contact info
            const links = Array.from(document.querySelectorAll('a')).map(a => ({
                text: a.innerText,
                href: a.href
            }));

            // Get meta info
            const title = document.title;
            const description = document.querySelector('meta[name="description"]')?.content || '';

            return {
                title,
                description,
                bodyText,
                h1s,
                h2s,
                h3s,
                paragraphs: paragraphs.filter(p => p.trim().length > 10),
                links: links.filter(l => l.text && l.text.trim().length > 0)
            };
        }""")

        browser.close()

        print("\n" + "="*70)
        print("SHAMROCK DAY SPA - EXTRACTED INFORMATION")
        print("="*70)

        print(f"\n📌 Title: {data['title']}")
        print(f"📝 Description: {data['description']}")

        print(f"\n📋 H1 Headings ({len(data['h1s'])}):")
        for i, h1 in enumerate(data['h1s'][:10], 1):
            print(f"  {i}. {h1}")

        print(f"\n📋 H2 Headings ({len(data['h2s'])}):")
        for i, h2 in enumerate(data['h2s'][:10], 1):
            print(f"  {i}. {h2}")

        print(f"\n📋 H3 Headings ({len(data['h3s'])}):")
        for i, h3 in enumerate(data['h3s'][:10], 1):
            print(f"  {i}. {h3}")

        print(f"\n📄 Paragraphs ({len(data['paragraphs'])}):")
        for i, p in enumerate(data['paragraphs'][:20], 1):
            if len(p) > 100:
                print(f"  {i}. {p[:100]}...")
            else:
                print(f"  {i}. {p}")

        print(f"\n🔗 Links (showing first 20):")
        for i, link in enumerate(data['links'][:20], 1):
            print(f"  {i}. {link['text'][:50]} -> {link['href'][:60]}")

        print(f"\n📱 Full Body Text (first 2000 chars):")
        print("-"*70)
        print(data['bodyText'][:2000])
        print("-"*70)

        # Save to JSON
        output_file = "shamrock_data.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Full data saved to: {output_file}")

        return data

if __name__ == '__main__':
    try:
        data = extract_shamrock_info()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
