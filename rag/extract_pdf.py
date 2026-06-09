import pypdf
import os

# Path to your downloaded PDF
pdf_path = r"C:\Users\ACER\Downloads\Catechism of the Catholic Church - USCCB.pdf"
output_path = "data/catechism_full.txt"

print("Extracting text from Catechism PDF...")

text_pages = []

with open(pdf_path, "rb") as f:
    reader = pypdf.PdfReader(f)
    total_pages = len(reader.pages)
    print(f"Total pages: {total_pages}")
    
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            text_pages.append(text)
        if i % 50 == 0:
            print(f"Processing page {i}/{total_pages}...")

full_text = "\n\n".join(text_pages)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(full_text)

print(f"Done! Extracted {len(text_pages)} pages")
print(f"Saved to {output_path}")
print(f"File size: {os.path.getsize(output_path):,} bytes") 
