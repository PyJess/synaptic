

# 1. Open PDF and extract text
pdf_path = "C:\\Users\\x.hita\\OneDrive - Reply\\Workspace\\SYNAPTIC\\synaptic\\process\\generated_protocol.pdf"
import pdfplumber
import os
import re
import pandas as pd

def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "_", name)[:50]

def table_to_markdown(table):
    if not table:
        return ""
    df = pd.DataFrame(table[1:], columns=table[0])
    return df.to_markdown(index=False)

# Percorso PDF
output_dir = "chapters_output"
os.makedirs(output_dir, exist_ok=True)
chapter_counter = 0
current_chapter_title = None
current_chapter_text = []
current_chapter_tables = []

# Regex for first-level chapters:
# - Starts with integer + dot
# - Space
# - Title is mostly uppercase (heuristic)
chapter_pattern = re.compile(r'^\d+\.\s+.+') # At least 3 uppercase letters

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        # --- Extract tables ---
        page_tables = page.extract_tables()
        if page_tables:
            current_chapter_tables.extend(page_tables)

        # --- Extract text ---
        text = page.extract_text()
        if not text:
            continue
        lines = text.split("\n")
        # Remove headers/footers
        lines = [l.strip() for l in lines if l.strip() and not l.startswith("Clinical Trial Protocol") and not re.match(r'^Page \d+ of \d+', l)]
        for line in lines:
            if chapter_pattern.match(line):
    # Save previous chapter if exists
                if current_chapter_title:
                    filename = f"{chapter_counter:03d}_{sanitize_filename(current_chapter_title)}.txt"
                    filepath = os.path.join(output_dir, filename)
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(f"# {current_chapter_title}\n\n")
                        f.write("\n".join(current_chapter_text))
                        for t_idx, table in enumerate(current_chapter_tables):
                            f.write(f"\n\n=== TABLE {t_idx+1} ===\n")
                            f.write(table_to_markdown(table))
                    chapter_counter += 1
                    current_chapter_text = []
                    current_chapter_tables = []

                # Start new chapter
                current_chapter_title = line
            else:
                # Append line to current chapter
                current_chapter_text.append(line)


# --- Save last chapter ---
if current_chapter_title:
    filename = f"{chapter_counter:03d}_{sanitize_filename(current_chapter_title)}.txt"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {current_chapter_title}\n\n")
        f.write("\n".join(current_chapter_text))
        for t_idx, table in enumerate(current_chapter_tables):
            f.write(f"\n\n=== TABLE {t_idx+1} ===\n")
            f.write(table_to_markdown(table))

print(f"Saved {chapter_counter+1} chapters in '{output_dir}'")