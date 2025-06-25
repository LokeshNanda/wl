# Weekly Learnings Static Site Generator

![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![CI](https://github.com/LokeshNanda/wl/actions/workflows/ci.yml/badge.svg)

A simple, production-ready static site generator for organizing and publishing your weekly notes, learnings, and findings. Write your notes in Markdown, and generate a beautiful, navigable website with a single command.

---

## Features

- **Markdown-based:** Write notes in plain Markdown files.
- **Automatic Grouping:** Notes are grouped by week (ending Sunday) and rendered to HTML.
- **Modern UI:** Clean, responsive design using Bootstrap and custom CSS.
- **Easy Navigation:** Homepage lists all weeks; each week page has navigation links.
- **Extensible:** Add new Markdown files for different topics (e.g., books, tools, LLM learnings).

---

## Directory Structure

```
.
├── books.md              # Notes about books
├── llm-learning.md       # Notes about LLMs and related topics
├── tools-explore.md      # Notes about tools and experiments
├── build.py              # Main static site generator script
├── requirements.txt      # Python dependencies
├── templates/            # Jinja2 HTML templates
│   ├── index.html        # Homepage template
│   └── week.html         # Weekly notes template
└── output/               # (Generated) Static site output
```

---

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/LokeshNanda/wl.git
   cd wl
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. **Write your notes:**
   - Add daily notes to any `.md` file (e.g., `llm-learning.md`, `books.md`).
   - Use the following format for dates:
     ```markdown
     ## June 2025
     ### 25 Jun 2025
     - Your note here
     ```

2. **Generate the static site:**
   ```bash
   python build.py
   ```
   - The site will be generated in the `output/` directory.

3. **Preview locally:**
   - Open `output/index.html` in your browser.

4. **Deploy:**
   - Upload the contents of `output/` to any static hosting service (e.g., GitHub Pages, Netlify, Vercel).

---

## Adding New Notes

- Create or update any `.md` file in the root directory.
- Each note should be under a date heading (e.g., `### 26 Jun 2025`).
- The generator will automatically pick up all `.md` files (except `README.md`).

---

## Customization

- **Templates:**
  - Edit `templates/index.html` and `templates/week.html` to change the look and feel.
- **Site Title & Subtitle:**
  - Modify `SITE_TITLE` and `SITE_SUBTITLE` in `build.py`.
- **Base URL:**
  - Update `SITE_BASE` in `build.py` if deploying to a custom domain.

---

## CI/CD: GitHub Actions Workflow

This project uses GitHub Actions for CI/CD to automatically build and deploy the static site whenever you push to the `main` branch.

### How it works
- **On every push to `main`:**
  - Checks out the code
  - Installs Python and dependencies
  - Runs the static site generator (`build.py`)
  - Deploys the contents of the `output/` directory to GitHub Pages

> **Note:** Make sure GitHub Pages is enabled for your repository and set to deploy from the `gh-pages` branch.

---

## Contributing

Contributions are welcome! Please open issues or pull requests for improvements, bug fixes, or new features.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details. 