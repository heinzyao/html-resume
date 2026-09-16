# html-resume

[English](#english) | [繁體中文](#繁體中文)

Magazine-style bilingual résumé (中文 / English), content separated from design.
Live: **https://heinzyao.github.io/html-resume/**

---

## English

### Structure

```
html-resume/
├── resume_data.yaml   # résumé content (the only file you need to edit)
├── template.html      # Jinja2 template (design layer, Tailwind CSS)
├── build.py           # build script: YAML → HTML, optional --pdf
├── index.html         # generated static page (served by GitHub Pages)
└── pyproject.toml     # uv project config (jinja2, pyyaml)
```

### Everyday Use

#### Update the content

Edit `resume_data.yaml` only — every Chinese and English field lives there:

```bash
vim resume_data.yaml
uv run python build.py   # regenerate index.html
```

#### Generate a PDF

Requires Playwright:

```bash
uv pip install playwright
playwright install chromium
uv run python build.py --pdf   # writes resume.pdf
```

The PDF is auto-scaled so everything fits on a single A4 page.

#### Publish

```bash
git add .
git commit -m "update resume"
git push
```

GitHub Pages updates about a minute later.

### Data Model (resume_data.yaml)

| Section | Description |
|------|------|
| `personal` | Name, email, phone, LinkedIn, GitHub |
| `summary` | Personal summary (`zh` / `en`) |
| `skills_zh` / `skills_en` | Skill categories (defined separately per language) |
| `education` | Education (`degree_zh/en`, `school_zh/en`, `period`) |
| `certifications` | Certifications (shown in the Chinese version only) |
| `experience` | Work history (`bullets_zh` / `bullets_en`, bulleted per language) |

### Design Notes

- **Fonts**: Merriweather (English serif) + Noto Serif TC (Chinese) + Inter (body)
- **Print**: `@media print` forces the two-column grid, `zoom` auto-scales to one A4 page
- **Language toggle**: top-right button, plain JavaScript, no page reload

---

## 繁體中文

雜誌風雙語履歷（中文 / English），內容與設計分離。
線上版：**https://heinzyao.github.io/html-resume/**

### 架構

```
html-resume/
├── resume_data.yaml   # 履歷內容（唯一需要編輯的檔案）
├── template.html      # Jinja2 模板（設計層，Tailwind CSS）
├── build.py           # 建置腳本：YAML → HTML，可選 --pdf
├── index.html         # 產出的靜態頁面（GitHub Pages 用）
└── pyproject.toml     # uv 專案設定（jinja2、pyyaml）
```

### 日常使用

#### 更新履歷內容

只需編輯 `resume_data.yaml`，所有中英文欄位皆在此：

```bash
vim resume_data.yaml
uv run python build.py   # 重新產生 index.html
```

#### 產生 PDF

需先安裝 Playwright：

```bash
uv pip install playwright
playwright install chromium
uv run python build.py --pdf   # 產出 resume.pdf
```

PDF 會自動縮放以確保內容完整呈現在一頁 A4 內。

#### 推送上線

```bash
git add .
git commit -m "update resume"
git push
```

GitHub Pages 約 1 分鐘後自動更新。

### 資料結構（resume_data.yaml）

| 區塊 | 說明 |
|------|------|
| `personal` | 姓名、Email、電話、LinkedIn、GitHub |
| `summary` | 個人簡介（`zh` / `en`） |
| `skills_zh` / `skills_en` | 技術技能分類（中英文各自定義） |
| `education` | 學歷（`degree_zh/en`、`school_zh/en`、`period`） |
| `certifications` | 技能認證（僅顯示於中文版） |
| `experience` | 工作經歷（`bullets_zh` / `bullets_en` 各自列點） |

### 設計特點

- **字型**：Merriweather（英文 serif）+ Noto Serif TC（中文）+ Inter（內文）
- **列印**：`@media print` 強制雙欄格線，`zoom` 自動縮放至一頁 A4
- **語言切換**：右上角按鈕，純 JavaScript，無需重整頁面
