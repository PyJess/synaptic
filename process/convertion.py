import fitz
import pdfplumber
import re
import os

# --- Config ---
pdf_path = "C:\\Users\\x.hita\\OneDrive - Reply\\Workspace\\SYNAPTIC\\synaptic\\process\\generated_protocol.pdf"
output_dir = "chapters_md"
os.makedirs(output_dir, exist_ok=True)

chapter_pattern = re.compile(r'^# \d+\.\s+.+')
subchapter_pattern = re.compile(r'^## \d+\.\d+\s+.+')
sanitize_pattern = re.compile(r'[\\/*?:"<>|]')

def sanitize_filename(name):
    return sanitize_pattern.sub("_", name)

def clean_line(line):
    line = line.strip()
    if line.startswith("Clinical Trial Protocol"):
        return ""
    if re.match(r'^Page \d+ of \d+', line):
        return ""
    return line

# --- Funzione per tabelle compatte ---
def table_to_markdown_compact(table):
    if not table:
        return ""
    
    # Sostituisce newline con <br>
    cleaned_table = []
    for row in table:
        cleaned_row = [cell.replace("\n", " <br> ").strip() if cell else "" for cell in row]
        cleaned_table.append(cleaned_row)

    # Rimuove colonne completamente vuote
    max_cols = max(len(r) for r in cleaned_table)
    remove_idx = [c for c in range(max_cols) if all((r[c] if c < len(r) else "") == "" for r in cleaned_table)]
    final_table = []
    for row in cleaned_table:
        new_row = [cell for i, cell in enumerate(row) if i not in remove_idx]
        final_table.append(new_row)

    # Unisce celle multi-periodo consecutive (se entrambe non vuote)
    merged_table = []
    for row in final_table:
        merged_row = []
        skip_next = False
        for i, cell in enumerate(row):
            if skip_next:
                skip_next = False
                continue
            if i < len(row)-1 and cell != "" and row[i+1] != "":
                merged_row.append(cell + " <br> " + row[i+1])
                skip_next = True
            else:
                merged_row.append(cell)
        merged_table.append(merged_row)

    # Uniforma tutte le righe allo stesso numero di colonne
    max_cols_final = max(len(r) for r in merged_table)
    for i in range(len(merged_table)):
        if len(merged_table[i]) < max_cols_final:
            merged_table[i] += [""] * (max_cols_final - len(merged_table[i]))

    # Costruisce Markdown
    md = []
    md.append("| " + " | ".join(merged_table[0]) + " |")
    md.append("| " + " | ".join(["---"]*max_cols_final) + " |")
    for row in merged_table[1:]:
        md.append("| " + " | ".join(row) + " |")
    return "\n".join(md)

# --- Step 1: Estrai testo completo con fitz ---
doc = fitz.open(pdf_path)
full_markdown_lines = []

for page in doc:
    blocks = page.get_text("dict")["blocks"]
    for block in blocks:
        if block['type'] == 0:
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue
                    if span["size"] > 16:
                        full_markdown_lines.append(f"# {text}")
                    elif span["size"] > 11:
                        full_markdown_lines.append(f"## {text}")
                    else:
                        clean = clean_line(text)
                        if clean:
                            full_markdown_lines.append(clean)

# Salva Markdown completo
full_md_path = os.path.join(output_dir, "full_output.md")
with open(full_md_path, "w", encoding="utf-8") as f:
    f.write("\n".join(full_markdown_lines))
print(f"Full Markdown saved to {full_md_path}")

# --- Step 2: Estrai tabelle con pdfplumber ---
chapter_tables = {}
with pdfplumber.open(pdf_path) as pdf:
    current_chapter_title = None
    for page in pdf.pages:
        page_tables = page.extract_tables()
        if page_tables and current_chapter_title:
            for table in page_tables:
                chapter_tables.setdefault(current_chapter_title, []).append(table)

        # Rileva capitoli
        text = page.extract_text()
        if not text:
            continue
        lines = [clean_line(l) for l in text.split("\n") if clean_line(l)]
        for line in lines:
            if re.match(r'^\d+\.\s+.+', line):
                current_chapter_title = f"# {line}"
                chapter_tables.setdefault(current_chapter_title, [])
                break

# --- Step 3: Salva capitoli separati con tabelle compatte ---
current_title = None
current_text = []
chapter_counter = 1
subchapter_counter = 1

for line in full_markdown_lines:
    line_stripped = line.strip()
    if not line_stripped:
        continue
    if chapter_pattern.match(line_stripped):
        if current_title:
            filename = f"{chapter_counter:03d}_{sanitize_filename(current_title)}.md"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f_out:
                f_out.write(f"{current_title}\n\n")
                f_out.write("\n".join(current_text))
                tables = chapter_tables.get(current_title, [])
                for idx, table in enumerate(tables):
                    f_out.write(f"\n\n=== TABLE {idx+1} ===\n")
                    f_out.write(table_to_markdown_compact(table))
        
        current_title = line_stripped
        current_text = []
        subchapter_counter = 1
        chapter_counter += 1
        
    elif subchapter_pattern.match(line_stripped):
        if current_title:  # Salva sottocapitolo precedente
            filename = f"{chapter_counter-1:03d}_{subchapter_counter:02d}_{sanitize_filename(current_title)}.md"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f_out:
                f_out.write(f"{current_title}\n\n")
                f_out.write("\n".join(current_text))
                tables = chapter_tables.get(current_title, [])
                for idx, table in enumerate(tables):
                    f_out.write(f"\n\n=== TABLE {idx+1} ===\n")
                    f_out.write(table_to_markdown_compact(table))
        # reset
        current_title = line_stripped
        current_text = []
        subchapter_counter += 1

    else:
        clean = clean_line(line_stripped)
        if clean:
            current_text.append(clean)

# --- Salva ultimo capitolo/sottocapitolo ---
if current_title:
    filename = f"{chapter_counter:03d}_{sanitize_filename(current_title)}.md"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f_out:
        f_out.write(f"{current_title}\n\n")
        f_out.write("\n".join(current_text))
        tables = chapter_tables.get(current_title, [])
        for idx, table in enumerate(tables):
            f_out.write(f"\n\n=== TABLE {idx+1} ===\n")
            f_out.write(table_to_markdown_compact(table))

print(f"Saved {chapter_counter} chapters in '{output_dir}' with compact, readable tables.")
