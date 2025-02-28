import re
from langchain_community.llms import Ollama
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

def generate_resume(name, contact, summary, experience, education, skills, additional_info=None):
    formatted_experience = experience.replace(" * ", " • ")
    
    prompt = f"""
Generate a professional resume based on the following details:

Name: {name}

Contact Information: {contact}

Professional Summary: {summary}

Work Experience: {formatted_experience}

Education: {education}

Skills: {skills}

additional_info: {additional_info}

Do not say anything except the resume contents. Please output the resume in a clear, modern format with sections and bullet points where appropriate.
Use '-' instead of '*' or '•' for bullet points.
"""
    llm = Ollama(model="llama3.2:1b")
    resume = llm.invoke(prompt)
    return resume

def save_resume_to_pdf(resume_text, title="Resume", filename="resume.pdf"):
    pdf = ResumePDF('P', 'mm', 'A4')
    
    try:
        pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
        pdf.add_font('DejaVu', 'B', 'DejaVuSans-Bold.ttf', uni=True)
        pdf.add_font('DejaVu', 'I', 'DejaVuSans-Oblique.ttf', uni=True)
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
    
    resume_text = resume_text.replace('•', '-')
    
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
            is_bullet_point = clean_line.startswith('- ')
            indentation = 0
            if is_bullet_point:
                indentation = 5
                
            clean_line = re.sub(r'\*\*(.*?)\*\*', lambda m: f'<b>{m.group(1)}</b>', clean_line)
            clean_line = re.sub(r'\*(.*?)\*', lambda m: f'<i>{m.group(1)}</i>', clean_line)
            
            if is_bullet_point:
                pdf.set_x(pdf.get_x() + indentation)
                
            if '<b>' not in clean_line and '<i>' not in clean_line:
                pdf.multi_cell(0, 10, txt=clean_line)
            else:
                parts = re.split(r'(<b>|</b>|<i>|</i>)', clean_line)
                current_x = pdf.get_x()
                line_started = False
                
                for part in parts:
                    if part == '<b>':
                        pdf.set_font(body_font, 'B', 12)
                    elif part == '</b>':
                        pdf.set_font(body_font, '', 12)
                    elif part == '<i>':
                        pdf.set_font(body_font, 'I', 12)
                    elif part == '</i>':
                        pdf.set_font(body_font, '', 12)
                    elif part:
                        if not line_started:
                            pdf.multi_cell(0, 10, txt=part)
                            line_started = True
                        else:
                            pdf.write(10, part)
    
    pdf.output(filename)
    print(f"Resume saved to {filename}")
