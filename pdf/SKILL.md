---
name: pdf
description: 当用户想要对 PDF 文件执行任何操作时，请使用此技能。这包括：读取或提取 PDF 中的文本/表格、将多个 PDF 合并为一个文件、拆分 PDF、旋转页面、添加水印、创建新 PDF、填写 PDF 表单、加密/解密 PDF、提取图片，以及对扫描版 PDF 进行 OCR 处理使其可搜索。如果用户提到 .pdf 文件或要求生成 PDF，就使用此技能。
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Processing Guide

## Overview

This guide covers essential PDF processing operations using Python libraries and command-line tools. For advanced features, JavaScript libraries, and detailed examples, see REFERENCE.md. If you need to fill out a PDF form, read FORMS.md and follow its instructions.

## Quick Start

```python
from pypdf import PdfReader, PdfWriter

# Read a PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## Python Libraries

### pypdf - Basic Operations

#### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

#### Split PDF
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

#### Extract Metadata
```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```

#### Rotate Pages
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # Rotate 90 degrees clockwise
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### pdfplumber - Text and Table Extraction

#### Extract Text with Layout
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

#### Extract Tables
```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

#### Advanced Table Extraction
```python
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # Check if table is not empty
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# Combine all tables
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

### reportlab - Create PDFs

#### Basic PDF Creation
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

# Add text
c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "This is a PDF created with reportlab")

# Add a line
c.line(100, height - 140, 400, height - 140)

# Save
c.save()
```

#### Create PDF with Multiple Pages
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Add content
title = Paragraph("Report Title", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("This is the body of the report. " * 20, styles['Normal'])
story.append(body)
story.append(PageBreak())

# Page 2
story.append(Paragraph("Page 2", styles['Heading1']))
story.append(Paragraph("Content for page 2", styles['Normal']))

# Build PDF
doc.build(story)
```

#### Subscripts and Superscripts

**IMPORTANT**: Never use Unicode subscript/superscript characters (₀₁₂₃₄₅₆₇₈₉, ⁰¹²³⁴⁵⁶⁷⁸⁹) in ReportLab PDFs. The built-in fonts do not include these glyphs, causing them to render as solid black boxes.

Instead, use ReportLab's XML markup tags in Paragraph objects:
```python
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

# Subscripts: use <sub> tag
chemical = Paragraph("H<sub>2</sub>O", styles['Normal'])

# Superscripts: use <super> tag
squared = Paragraph("x<super>2</super> + y<super>2</super>", styles['Normal'])
```

For canvas-drawn text (not Paragraph objects), manually adjust font the size and position rather than using Unicode subscripts/superscripts.

## Command-Line Tools

### pdftotext (poppler-utils)
```bash
# Extract text
pdftotext input.pdf output.txt

# Extract text preserving layout
pdftotext -layout input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt  # Pages 1-5
```

### qpdf
```bash
# Merge PDFs
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split pages
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf --pages . 6-10 -- pages6-10.pdf

# Rotate pages
qpdf input.pdf output.pdf --rotate=+90:1  # Rotate page 1 by 90 degrees

# Remove password
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

### pdftk (if available)
```bash
# Merge
pdftk file1.pdf file2.pdf cat output merged.pdf

# Split
pdftk input.pdf burst

# Rotate
pdftk input.pdf rotate 1east output rotated.pdf
```

## Common Tasks

### Extract Text from Scanned PDFs
```python
# Requires: pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

# Convert PDF to images
images = convert_from_path('scanned.pdf')

# OCR each page
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

### Add Watermark
```python
from pypdf import PdfReader, PdfWriter

# Create watermark (or load existing)
watermark = PdfReader("watermark.pdf").pages[0]

# Apply to all pages
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### Extract Images
```bash
# Using pdfimages (poppler-utils)
pdfimages -j input.pdf output_prefix

# This extracts all images as output_prefix-000.jpg, output_prefix-001.jpg, etc.
```

### Password Protection
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# Add password
writer.encrypt("userpassword", "ownerpassword")

with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

## Quick Reference

| Task | Best Tool | Command/Code |
|------|-----------|--------------|
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Split PDFs | pypdf | One page per file |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Create PDFs | reportlab | Canvas or Platypus |
| Command line merge | qpdf | `qpdf --empty --pages ...` |
| OCR scanned PDFs | pytesseract | Convert to image first |
| Fill PDF forms | pdf-lib or pypdf (see FORMS.md) | See FORMS.md |

## Next Steps

- For advanced pypdfium2 usage, see REFERENCE.md
- For JavaScript libraries (pdf-lib), see REFERENCE.md
- If you need to fill out a PDF form, follow the instructions in FORMS.md
- For troubleshooting guides, see REFERENCE.md

---

# 中文快速使用指南

## 常用操作速查

| 操作 | 推荐工具 | 说明 |
|------|----------|------|
| 合并 PDF | pypdf | 多个 PDF 合并为一个 |
| 拆分 PDF | pypdf | 将 PDF 按页拆分 |
| 提取文本 | pdfplumber | 保留格式的文本提取 |
| 提取表格 | pdfplumber | 提取表格数据到 Excel |
| 创建 PDF | reportlab | 从零创建新 PDF |
| 命令行合并 | qpdf | 快速命令行操作 |
| 扫描版 OCR | pytesseract | 识别扫描文档文字 |
| 填写表单 | pypdf/pdf-lib | 填写 PDF 表单 |

## 快速代码示例

### 读取 PDF 基本信息
```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
print(f"总页数: {len(reader.pages)}")
print(f"标题: {reader.metadata.title}")
print(f"作者: {reader.metadata.author}")
```

### 提取文本内容
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        print(f"=== 第 {i+1} 页 ===")
        print(text)
```

### 提取表格到 Excel
```python
import pdfplumber
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

if all_tables:
    result = pd.concat(all_tables, ignore_index=True)
    result.to_excel("提取的表格.xlsx", index=False)
```

### 合并多个 PDF
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for file in ["文件1.pdf", "文件2.pdf", "文件3.pdf"]:
    reader = PdfReader(file)
    for page in reader.pages:
        writer.add_page(page)

with open("合并结果.pdf", "wb") as output:
    writer.write(output)
```

### 拆分 PDF 为单页
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"第{i+1}页.pdf", "wb") as output:
        writer.write(output)
```

### 旋转页面
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.rotate(90)  # 顺时针旋转90度
    writer.add_page(page)

with open("旋转后.pdf", "wb") as output:
    writer.write(output)
```

### 添加水印
```python
from pypdf import PdfReader, PdfWriter

# 读取水印（需要提前准备水印PDF）
watermark = PdfReader("水印.pdf").pages[0]

reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("加水印后.pdf", "wb") as output:
    writer.write(output)
```

### 加密 PDF
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# 设置密码
writer.encrypt("用户密码", "所有者密码")

with open("加密后.pdf", "wb") as output:
    writer.write(output)
```

### 扫描版 PDF OCR 识别
```python
# 需要安装: pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

images = convert_from_path('扫描文档.pdf')

for i, image in enumerate(images):
    text = pytesseract.image_to_string(image, lang='chi_sim')  # 中文
    print(f"=== 第 {i+1} 页 ===")
    print(text)
```

### 创建新 PDF
```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 注册中文字体（需要字体文件）
pdfmetrics.registerFont(TTFont('SimHei', 'simhei.ttf'))

c = canvas.Canvas("新建文档.pdf", pagesize=A4)
c.setFont('SimHei', 24)
c.drawString(100, 750, "这是标题")
c.setFont('SimHei', 12)
c.drawString(100, 700, "这是正文内容")
c.save()
```

## 命令行工具速查

### pdftotext - 提取文本
```bash
pdftotext input.pdf output.txt           # 基本提取
pdftotext -layout input.pdf output.txt   # 保留布局
pdftotext -f 1 -l 5 input.pdf out.txt    # 只提取第1-5页
```

### qpdf - 合并/拆分/旋转
```bash
qpdf --empty --pages a.pdf b.pdf -- merged.pdf   # 合并
qpdf input.pdf --pages . 1-5 -- output.pdf       # 提取第1-5页
qpdf input.pdf output.pdf --rotate=+90:1         # 第1页旋转90度
qpdf --password=密码 --decrypt 加密.pdf 解密.pdf  # 解密
```

### pdfimages - 提取图片
```bash
pdfimages -j input.pdf img   # 提取所有图片为 img-000.jpg, img-001.jpg...
```

## 注意事项

1. **中文支持**：使用 reportlab 创建 PDF 时，需要注册中文字体才能正确显示中文
2. **扫描版 PDF**：扫描的图片型 PDF 需要先用 OCR 工具识别文字
3. **加密 PDF**：处理加密 PDF 时需要先提供密码解密
4. **表格提取**：复杂表格可能提取不完整，建议手动检查结果
