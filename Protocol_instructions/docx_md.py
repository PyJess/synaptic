from docx import Document

# --- Funzione per ottenere la numerazione dal paragrafo ---
def get_numbering(paragraph, numbering_dict):
    """
    Restituisce la numerazione completa di un paragrafo numerato come stringa.
    """
    p = paragraph._p
    numPr = p.xpath('.//w:numPr')
    if not numPr:
        return ""
    
    numId_elem = numPr[0].xpath('./w:numId')
    ilvl_elem = numPr[0].xpath('./w:ilvl')
    if not numId_elem or not ilvl_elem:
        return ""
    
    ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    numId = numId_elem[0].get(ns + 'val')
    ilvl = int(ilvl_elem[0].get(ns + 'val'))

    # Inizializza dizionario dei contatori se necessario
    if numId not in numbering_dict:
        numbering_dict[numId] = {}
    if ilvl not in numbering_dict[numId]:
        numbering_dict[numId][ilvl] = 1
    else:
        numbering_dict[numId][ilvl] += 1

    # Reset dei livelli inferiori
    for lower in range(ilvl+1, 10):
        numbering_dict[numId][lower] = 0

    # Costruisci la stringa numerica tipo "2.1.3"
    num_str = '.'.join(str(numbering_dict[numId][i]) for i in range(ilvl+1) if numbering_dict[numId].get(i,0) > 0)
    return num_str

# --- Funzione principale di conversione ---
def heading_level_to_md(level):
    """Converte il livello di heading DOCX in # Markdown"""
    return '#' * level

def docx_to_markdown(docx_path):
    doc = Document(docx_path)
    md_lines = []
    numbering_dict = {}

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        style = para.style.name.lower()
        num_str = get_numbering(para, numbering_dict)

        if 'heading' in style:
            try:
                level = int(style.split('heading')[-1].strip())
            except ValueError:
                level = 1
            # Heading con numerazione
            if num_str:
                md_lines.append(f"{heading_level_to_md(level)} {num_str} {text}")
            else:
                md_lines.append(f"{heading_level_to_md(level)} {text}")
        else:
            # Paragrafo normale
            md_lines.append(text)

    return "\n\n".join(md_lines)

# --- Esempio di utilizzo ---
docx_path = "C:\\Users\\x.hita\\OneDrive - Reply\\Workspace\\SYNAPTIC\\synaptic\\Protocol_instructions\\CPT_CoreBWE_v010.docx"
md_path = "output.md"

markdown_text = docx_to_markdown(docx_path)
with open(md_path, "w", encoding="utf-8") as f:
    f.write(markdown_text)

print(f"Converted {docx_path} to {md_path}")
