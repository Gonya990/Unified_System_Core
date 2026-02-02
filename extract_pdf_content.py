import os

from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"Error: File not found at {pdf_path}")
        return

    try:
        reader = PdfReader(pdf_path)
        print(f"Number of pages: {len(reader.pages)}")

        full_text = ""
        for _, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                full_text += text + "\n"

        # Save to a text file for easy reading
        output_path = pdf_path.replace(".pdf", ".txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        print(f"Successfully extracted text to {output_path}")
        # Print first 2000 chars to stdout for immediate context
        print("--- Start of Content ---")
        print(full_text[:2000])
        print("--- End of Preview ---")

    except Exception as e:
        print(f"Error reading PDF: {e}")


if __name__ == "__main__":
    pdf_path = "/Users/macbook/Documents/Unified_System/conversation(1).pdf"
    extract_text_from_pdf(pdf_path)
