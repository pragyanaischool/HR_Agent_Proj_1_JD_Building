import streamlit as st
import groq
from fpdf import FPDF
from io import BytesIO
from PIL import Image
import tempfile
import requests
import os

# Initialize Streamlit app
st.title("Job Description Generator - Application")
st.image("PragyanAI_Transperent_github.png")
# Initialize LLM
API_KEY = "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"  # Replace with actual API key
#llm = groq.Groq(model="llama3-8b-8192", api_key=API_KEY)
llm_client = groq.Client(api_key=API_KEY)

# Job Title
job_title = st.text_input("Enter Job Title")

# Download and use a Unicode font
FONT_URL = "https://github.com/dejavu-fonts/dejavu-fonts/blob/master/ttf/DejaVuSans.ttf?raw=true"
FONT_PATH = "DejaVuSans.ttf"

if not os.path.exists(FONT_PATH):
    response = requests.get(FONT_URL)
    with open(FONT_PATH, "wb") as f:
        f.write(response.content)

# Education
education_required = st.checkbox("Require Education Qualification?")
education_details = st.multiselect(
    "Select Education Qualification: Minimum Education Skill", 
    [ "10th","12th","BE", "BCA", "M.E", "MCA", "PhD", "Post Doc"]
)
# Experience
experience = st.slider("Years of Experience", 0.0, 20.0, 2.0)

# Key Skills
key_skills = st.multiselect(
    "Select Key Skills", 
    ["Python", "Machine Learning", "Data Science", "Cloud Computing", "Cyber Security", "AI Development", "Software Engineering"]
)

# Other Skills
other_skills = st.multiselect(
    "Select Other Skills", 
    ["Problem Solving", "Communication", "Leadership", "Time Management", "Critical Thinking"]
)

# Special Mandatory & Desirable Skills
mandatory_skills = st.text_area("Special Mandatory Skills")
desirable_skills = st.text_area("Desirable Skills")
good_to_have = st.text_area("Good to Have Skills")

# Company Information
company_name = st.text_input("Company Name")
company_description = st.text_area("Company Description")
role_responsibility = st.text_area("Role & Responsibilities")
location = st.text_input("Job Location")
salary_range = st.text_input("Salary Range")
company_logo = st.file_uploader("Upload Company Logo", type=["png", "jpg", "jpeg"])

# Generate Job Description
if st.button("Generate Job Description"):
    prompt = f"""
    Generate a detailed Job Description for the following:
    Job Title: {job_title}
    Education: {education_details if education_required else "Not Mandatory"}
    Experience: {str(experience)} years
    Key Skills: {', '.join(key_skills)}
    Other Skills: {', '.join(other_skills)}
    Mandatory Skills: {mandatory_skills}
    Desirable Skills: {desirable_skills}
    Good to Have: {good_to_have}
    Company: {company_name}
    Company Description: {company_description}
    Role & Responsibilities: {role_responsibility}
    Location: {location}
    Salary Range: {salary_range}
    """
    
    # Call to GROQ Llama Model
    response = llm_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "system", "content": "You are a helpful AI assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=500
    )
    llm_response = response.choices[0].message.content if response.choices else "Generated Job Description based on inputs. (Replace with LLM API Response)"
    
    st.subheader("Generated Job Description")
    st.write(llm_response)
    
    if company_logo:
        st.image(company_logo, caption="Company Logo")

    # PDF Generation
    def generate_pdf():
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        pdf.add_font("DejaVu", "", FONT_PATH, uni=True)  # Use Unicode font
        pdf.set_font("DejaVu", size=12)
        
        if company_logo:
            img = Image.open(company_logo)
            img = img.convert("RGB")  # Ensure image compatibility
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                img.save(tmpfile.name, format="PNG")
                pdf.image(tmpfile.name, x=10, y=8, w=30)
        
        pdf.ln(35)
        pdf.set_font("DejaVu", style='B', size=16)
        pdf.cell(200, 10, job_title, ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("DejaVu", size=12)
        pdf.multi_cell(0, 10, f"Company: {company_name}\nLocation: {location}\nSalary Range: {salary_range}\n\n{llm_response}")
        
        pdf_output = BytesIO()
        pdf.output(pdf_output, 'F')
        pdf_output.seek(0)
        return pdf_output.getvalue()
    
    pdf_data = generate_pdf()
    st.download_button(
        label="Download Job Description PDF",
        data=pdf_data,
        file_name=f"{job_title}_Job_Description.pdf",
        mime="application/pdf"
    )

