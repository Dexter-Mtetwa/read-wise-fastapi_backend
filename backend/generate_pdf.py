from pypdf import PdfWriter
from io import BytesIO

# Create a PDF file with a blank page
def create_pdf():
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    
    with open("test.pdf", "wb") as f:
        writer.write(f)
    print("Created test.pdf")

if __name__ == "__main__":
    create_pdf()
