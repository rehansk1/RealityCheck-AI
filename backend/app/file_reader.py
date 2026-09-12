from pypdf import PdfReader
from docx import Document


def extract_text(file_path, extension):

    text = ""


    if extension == ".pdf":

        reader = PdfReader(file_path)

        for page in reader.pages:
            text += page.extract_text() or ""



    elif extension == ".docx":

        doc = Document(file_path)

        for para in doc.paragraphs:
            text += para.text + "\n"



    elif extension == ".txt":

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()



    return text