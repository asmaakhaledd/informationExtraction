import PyPDF2
import markdown
import re
import pdfreader

def extract_information_from_pdf(pdf_file_name):
    with open(pdf_file_name, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        page_text=''
        for  page in pdf_reader.pages:
          page_text += page.extract_text()

        name_pattern = r'[A-Z][a-z]+\s[A-Z][a-z]+'  
        names = re.findall(name_pattern, page_text, flags=re.MULTILINE)
        
        gpa_pattern = r'\d+\.\d+' 
        gpa = re.findall(gpa_pattern, page_text)[0]

    return page_text, names[0], gpa

def save_text(page_text, output_path):
    markdown_text = markdown.markdown(page_text)
    with open(output_path, 'w', encoding="utf-8") as f:
        f.write(markdown_text)
    
pdf_file_name = "resume.pdf"
markdown_output_path = 'file.md'
extracted_text, name, gpa = extract_information_from_pdf(pdf_file_name)
save_text(extracted_text, markdown_output_path)
print(f"Name: {name}")
print(f"GPA: {gpa}")

