from toPDF import generate_resume, save_resume_to_pdf


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