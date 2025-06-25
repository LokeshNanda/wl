import os
import re
from datetime import datetime, timedelta
from markdown import markdown
from jinja2 import Environment, FileSystemLoader
from collections import defaultdict

# Constants
DATE_HEADING_RE = re.compile(r"^### (\d{1,2}) (\w{3}) (\d{4})")
MONTH_HEADING_RE = re.compile(r"^## \w+ \d{4}")
MONTHS = {m: i for i, m in enumerate(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], 1)}

TEMPLATE_DIR = "templates"
OUTPUT_DIR = "output"
SITE_TITLE = "Lokesh Nanda - Weekly Notes"
SITE_SUBTITLE = "Weekly Learnings & Findings"
SITE_BASE = "https://to-add.org"

# Jinja setup
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
index_template = env.get_template("index.html")
week_template = env.get_template("week.html")

def parse_date_str(day, month, year):
    return datetime(int(year), MONTHS[month], int(day))

def get_week_end(date):
    return (date + timedelta(days=(6 - date.weekday()))).date()

def extract_notes_from_file(path):
    notes = []
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()

    current_note_lines = []
    current_date = None

    for line in lines:
        line = line.rstrip()

        # Match and skip month headers (## July 2025, etc.)
        if MONTH_HEADING_RE.match(line):
            continue

        # Match date header like ### 13 Jul 2025
        match = DATE_HEADING_RE.match(line)
        if match:
            if current_date and current_note_lines:
                notes.append((current_date, "\n".join(current_note_lines)))
            current_note_lines = []
            current_date = parse_date_str(*match.groups())
        elif current_date:
            current_note_lines.append(line)

    # Add last note
    if current_date and current_note_lines:
        notes.append((current_date, "\n".join(current_note_lines)))

    return notes

def load_all_notes():
    all_notes = []
    for file in os.listdir():
        if file.endswith(".md") and not file.startswith("README"):
            print(f"Processing: {file}")
            all_notes.extend(extract_notes_from_file(file))
    return sorted(all_notes, key=lambda x: x[0])

def group_notes_by_week(notes):
    grouped = defaultdict(list)
    for date, content in notes:
        week_end = get_week_end(date)
        grouped[week_end].append(content)
    return dict(sorted(grouped.items(), reverse=True))

def render_week_page(week_end, note_contents, all_weeks):
    index = all_weeks.index(week_end)
    prev_week = all_weeks[index + 1] if index + 1 < len(all_weeks) else None
    next_week = all_weeks[index - 1] if index - 1 >= 0 else None

    # Convert each markdown note to HTML separately
    notes_html = [
        markdown(content, extensions=["extra", "codehilite"])
        for content in note_contents
    ]

    html = week_template.render(
        site_title=SITE_TITLE,
        subtitle=SITE_SUBTITLE,
        week_end=week_end.strftime("%d %b %Y"),
        notes=notes_html,
        prev_week=prev_week,
        next_week=next_week
    )

    filename = f"{week_end}.html"
    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
        f.write(html)


def render_index(all_weeks):
    html = index_template.render(
        site_title=SITE_TITLE,
        subtitle=SITE_SUBTITLE,
        weeks=sorted(all_weeks, reverse=True)
    )
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    notes = load_all_notes()
    weekly_notes = group_notes_by_week(notes)
    all_weeks = list(weekly_notes.keys())

    for week_end, notes_for_week in weekly_notes.items():
        render_week_page(week_end, notes_for_week, all_weeks)
    render_index(all_weeks)

if __name__ == "__main__":
    main()
