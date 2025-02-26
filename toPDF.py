import re
from langchain.llms import Ollama
from fpdf import FPDF

class ResumePDF(FPDF):
    def header(self):
        self.set_fill_color(30, 144, 255)
        self.rect(0, 0, self.w, 40, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font(self.header_font, 'B', 24)
        self.cell(0, 20, self.title, border=0, ln=1, align='C')
        self.ln(5)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font(self.body_font, 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def generate_resume(name, contact, summary, experience, education, skills):
    formatted_experience = experience.replace(" * ", " • ")
    
    prompt = f"""
Generate a professional resume based on the following details:

Name: {name}

Contact Information: {contact}

Professional Summary: {summary}

Work Experience: {formatted_experience}

Education: {education}

Skills: {skills}

Please output the resume in a clear, modern format with sections and bullet points where appropriate.
Use '•' instead of '*' for bullet points.
"""
    llm = Ollama(model="llama3.2:1b")
    resume = llm(prompt)
    return resume

def save_resume_to_pdf(resume_text, title="Resume", filename="resume.pdf"):
    pdf = ResumePDF()

    try:
        pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
        body_font = 'DejaVu'
        header_font = 'DejaVu'
    except Exception as e:
        print("Custom font not found, falling back to Helvetica.")
        body_font = 'Helvetica'
        header_font = 'Helvetica'
    
    pdf.body_font = body_font
    pdf.header_font = header_font
    pdf.title = title
    
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font(body_font, size=12)
    
    pdf.ln(10)
    
    lines = resume_text.split('\n')
    for line in lines:
        clean_line = line.strip()
        
        clean_line = re.sub(r'^\s*\*\s+', '- ', clean_line)
        clean_line = clean_line.replace('•', '-')
        
        if not clean_line:
            pdf.ln(5)
        elif clean_line.endswith(":"):
            pdf.set_font(body_font, 'B', 14)
            pdf.set_text_color(0, 102, 204)
            pdf.cell(0, 10, clean_line, ln=1)
            pdf.set_font(body_font, size=12)
            pdf.set_text_color(0, 0, 0)
        else:
            pdf.multi_cell(0, 10, txt=clean_line)
    
    pdf.output(filename)
    print(f"Resume saved to {filename}")

if __name__ == '__main__':
    name = "Jane Doe"
    contact = "jane.doe@example.com | (555) 123-4567"
    summary = ("Dynamic and results-oriented professional with over 5 years of experience in software development, "
               "machine learning, and data analysis. Passionate about leveraging technology to solve real-world problems.")
    experience = (
        "Software Engineer at Tech Innovators Inc. (2018-2023):\n"
        " * Developed scalable web applications using Python and JavaScript.\n"
        " * Led a team of developers to design and implement microservices.\n\n"
        "Junior Developer at CodeWorks (2016-2018):\n"
        " * Assisted in developing mobile applications and improving legacy systems."
    )
    education = "B.Sc. in Computer Science, University of Technology (2012-2016)"
    skills = "Python, JavaScript, React, Docker, Kubernetes, Machine Learning, Agile Methodologies"

    resume_text = generate_resume(name, contact, summary, experience, education, skills)
    print("Generated Resume:\n")
    print(resume_text)
    
    save_resume_to_pdf(resume_text, title=name, filename="resume_template.pdf")
