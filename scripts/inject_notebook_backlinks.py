#!/usr/bin/env python3
"""Inject a styled "Back to the book" card into the rendered notebook HTML pages.

Run AFTER `nbconvert`. The card is added only to the View-Notebook HTML (which opens
in the same browser tab) — NOT to the .ipynb files (those open in their own Colab tab,
so they need no back-link). Wired into both scripts/build_notebook_html.sh and the
GitHub Actions deploy workflow so it survives every re-render.

Add a chapter's notebooks to MAP as they ship.
"""
import os

HTML_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "chapters", "notebooks", "html")

# notebook-html filename -> (relative href to the chapter section, kicker, title)
MAP = {
    "ch01_what_is_statistics.html":
        ("../../ch01.html#notebook", "Back to the book", "Chapter 1 · What Is Statistics?"),
    "ch01_challenges_solutions.html":
        ("../../ch01.html#quiz", "Back to the book", "Chapter 1 · Take the quiz &amp; aim for 100%"),
    "ch02_stats_ds_ai.html":
        ("../../ch02.html#notebook", "Back to the book", "Chapter 2 · Statistics, Data Science &amp; AI"),
    "ch02_challenges_solutions.html":
        ("../../ch02.html#quiz", "Back to the book", "Chapter 2 · Take the quiz &amp; aim for 100%"),
    "ch03_data_science_lifecycle.html":
        ("../../ch03.html#notebook", "Back to the book", "Chapter 3 · The Data Science Lifecycle"),
    "ch03_challenges_solutions.html":
        ("../../ch03.html#quiz", "Back to the book", "Chapter 3 · Take the quiz &amp; aim for 100%"),
    "ch04_types_of_data.html":
        ("../../ch04.html#notebook", "Back to the book", "Chapter 4 · Types of Data &amp; Variables"),
    "ch04_challenges_solutions.html":
        ("../../ch04.html#quiz", "Back to the book", "Chapter 4 · Take the quiz &amp; aim for 100%"),
    "ch05_levels_of_measurement.html":
        ("../../ch05.html#notebook", "Back to the book", "Chapter 5 · Levels of Measurement"),
    "ch05_challenges_solutions.html":
        ("../../ch05.html#quiz", "Back to the book", "Chapter 5 · Take the quiz &amp; aim for 100%"),
    "ch06_population_vs_sample.html":
        ("../../ch06.html#notebook", "Back to the book", "Chapter 6 · Population vs. Sample"),
    "ch06_challenges_solutions.html":
        ("../../ch06.html#quiz", "Back to the book", "Chapter 6 · Take the quiz &amp; aim for 100%"),
    "ch07_math_refresher.html":
        ("../../ch07.html#notebook", "Back to the book", "Chapter 7 · Math Refresher for Statistics"),
    "ch07_challenges_solutions.html":
        ("../../ch07.html#quiz", "Back to the book", "Chapter 7 · Take the quiz &amp; aim for 100%"),
    "ch08_central_tendency.html":
        ("../../ch08.html#notebook", "Back to the book", "Chapter 8 · Measures of Central Tendency"),
    "ch08_challenges_solutions.html":
        ("../../ch08.html#quiz", "Back to the book", "Chapter 8 · Take the quiz &amp; aim for 100%"),
    "ch09_dispersion.html":
        ("../../ch09.html#notebook", "Back to the book", "Chapter 9 · Measures of Dispersion"),
    "ch09_challenges_solutions.html":
        ("../../ch09.html#quiz", "Back to the book", "Chapter 9 · Take the quiz &amp; aim for 100%"),
    "ch10_position.html":
        ("../../ch10.html#notebook", "Back to the book", "Chapter 10 · Measures of Position"),
    "ch10_challenges_solutions.html":
        ("../../ch10.html#quiz", "Back to the book", "Chapter 10 · Take the quiz &amp; aim for 100%"),
    "ch11_shape.html":
        ("../../ch11.html#notebook", "Back to the book", "Chapter 11 · Shape of a Distribution"),
    "ch11_challenges_solutions.html":
        ("../../ch11.html#quiz", "Back to the book", "Chapter 11 · Take the quiz &amp; aim for 100%"),
    "ch12_standardization.html":
        ("../../ch12.html#notebook", "Back to the book", "Chapter 12 · Standardization & z-scores"),
    "ch12_challenges_solutions.html":
        ("../../ch12.html#quiz", "Back to the book", "Chapter 12 · Take the quiz &amp; aim for 100%"),
    "ch13_frequency.html":
        ("../../ch13.html#notebook", "Back to the book", "Chapter 13 · Frequency Distributions"),
    "ch13_challenges_solutions.html":
        ("../../ch13.html#quiz", "Back to the book", "Chapter 13 · Take the quiz &amp; aim for 100%"),
    "ch14_categorical_charts.html":
        ("../../ch14.html#notebook", "Back to the book", "Chapter 14 · Charts for Categorical Data"),
    "ch14_challenges_solutions.html":
        ("../../ch14.html#quiz", "Back to the book", "Chapter 14 · Take the quiz &amp; aim for 100%"),
    "ch15_numerical_charts.html":
        ("../../ch15.html#notebook", "Back to the book", "Chapter 15 · Charts for Numerical Data"),
    "ch15_challenges_solutions.html":
        ("../../ch15.html#quiz", "Back to the book", "Chapter 15 · Take the quiz &amp; aim for 100%"),
    "ch16_multivariate.html":
        ("../../ch16.html#notebook", "Back to the book", "Chapter 16 · Multivariate &amp; Specialized Visuals"),
    "ch16_challenges_solutions.html":
        ("../../ch16.html#quiz", "Back to the book", "Chapter 16 · Take the quiz &amp; aim for 100%"),
    "ch17_choosing_viz.html":
        ("../../ch17.html#notebook", "Back to the book", "Chapter 17 · Choosing the Right Visualization"),
    "ch17_challenges_solutions.html":
        ("../../ch17.html#quiz", "Back to the book", "Chapter 17 · Take the quiz &amp; aim for 100%"),
    "ch18_data_cleaning_mindset.html":
        ("../../ch18.html#notebook", "Back to the book", "Chapter 18 · The Data-Cleaning Mindset"),
    "ch18_challenges_solutions.html":
        ("../../ch18.html#quiz", "Back to the book", "Chapter 18 · Take the quiz &amp; aim for 100%"),
    "ch19_duplicates_inconsistencies.html":
        ("../../ch19.html#notebook", "Back to the book", "Chapter 19 · Finding & Removing Duplicates and Inconsistencies"),
    "ch19_challenges_solutions.html":
        ("../../ch19.html#quiz", "Back to the book", "Chapter 19 · Take the quiz &amp; aim for 100%"),
}

def card(href, kicker, title):
    # Matches the book's chapter-nav card look (inlined, since nbconvert HTML has no book CSS).
    return (
      '<a class="book-backlink" href="' + href + '" '
      'style="display:flex;align-items:center;gap:12px;max-width:760px;margin:18px auto;'
      'text-decoration:none;border:1px solid #e6e9f2;border-radius:13px;padding:15px 20px;'
      'background:#ffffff;box-shadow:0 6px 18px rgba(20,30,80,0.06);'
      "font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif\">"
      '<span style="font-size:22px;color:#0891b2;line-height:1">&#8592;</span>'
      '<span>'
      '<span style="display:block;font-size:11px;font-weight:700;letter-spacing:0.08em;'
      'text-transform:uppercase;color:#8b94b3">' + kicker + '</span>'
      '<span style="font-weight:700;color:#1a2138;font-size:15px">' + title + '</span>'
      '</span></a>'
    )

# Override nbconvert's centered tables so they left-align like Colab.
TABLE_ALIGN_CSS = (
    '<style id="book-table-align">'
    '.jp-RenderedHTMLCommon table{margin-left:0 !important;margin-right:auto !important;}'
    '</style>'
)

def inject(path, href, kicker, title):
    html = open(path, encoding="utf-8").read()
    if 'class="book-backlink"' in html:
        return "already had link"
    # left-align tables (inject the style once, before </head>)
    if 'id="book-table-align"' not in html:
        html = html.replace("</head>", TABLE_ALIGN_CSS + "\n</head>", 1)
    c = card(href, kicker, title)
    # top: right after the opening <body ...> tag
    i = html.find("<body")
    if i != -1:
        j = html.find(">", i) + 1
        html = html[:j] + "\n" + c + html[j:]
    # bottom: right before </body>
    html = html.replace("</body>", c + "\n</body>", 1)
    open(path, "w", encoding="utf-8").write(html)
    return "injected"

def main():
    if not os.path.isdir(HTML_DIR):
        print("No HTML dir yet:", HTML_DIR); return
    for fname, (href, kicker, title) in MAP.items():
        path = os.path.join(HTML_DIR, fname)
        if os.path.exists(path):
            print(f"{fname}: {inject(path, href, kicker, title)}")
        else:
            print(f"{fname}: (not rendered yet, skipped)")

if __name__ == "__main__":
    main()
