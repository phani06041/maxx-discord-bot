import os
import pdfplumber
import zipfile
import re
import xml.etree.ElementTree as ET
from docx import Document


# ---------- BASIC LOADERS ----------

def load_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_md(path):
    return load_txt(path)


def load_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def load_docx(path):
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs if p.text)


# ---------- APPLE PAGES LOADER ----------

def load_pages(path):
    """
    Extract text from Apple .pages files by reading index.xml
    """
    text_content = ""

    try:
        with zipfile.ZipFile(path, "r") as z:
            if "index.xml" not in z.namelist():
                return ""

            with z.open("index.xml") as f:
                tree = ET.parse(f)
                root = tree.getroot()

                for elem in root.iter():
                    if elem.text:
                        text_content += elem.text + " "

        # Clean excessive whitespace
        text_content = re.sub(r"\s+", " ", text_content)

    except Exception as e:
        print(f"⚠️ Failed to read Pages file {os.path.basename(path)}: {e}")

    return text_content


# ---------- MASTER LOADER ----------

def load_manual_file(path):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".txt":
        return load_txt(path)
    elif ext == ".md":
        return load_md(path)
    elif ext == ".pdf":
        return load_pdf(path)
    elif ext == ".docx":
        return load_docx(path)
    elif ext == ".pages":
        return load_pages(path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")


def load_all_manuals(folder="manuals"):
    combined_text = ""

    if not os.path.exists(folder):
        print(f"⚠️ Manuals folder '{folder}' not found")
        return combined_text

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        if not os.path.isfile(path):
            continue

        try:
            content = load_manual_file(path)
            print(f"📄 Reading file: {file}")
            print(f"📏 Extracted length: {len(content) if content else 0}")

            if content:
                combined_text += content.lower() + "\n"
        except Exception as e:
            print(f"⚠️ Skipped {file}: {e}")

    return combined_text


def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks

def summarize_manual(chunks, max_chunks=3, max_lines=6):
    selected = chunks[:max_chunks]
    lines = []

    for chunk in selected:
        for line in chunk.split("\n"):
            line = line.strip()
            if line and len(line) > 40:
                lines.append(line)
            if len(lines) >= max_lines:
                break
        if len(lines) >= max_lines:
            break

    return "\n".join(lines)


# ---------- QUESTION MATCHING ----------

def find_answer(question, manual_text):
    question = question.lower()
    keywords = question.split()

    for line in manual_text.split("\n"):
        if any(word in line for word in keywords):
            return line.strip()

    return "❌ This information is not available in the manuals."
