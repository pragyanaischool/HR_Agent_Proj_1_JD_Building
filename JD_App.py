import streamlit as st
import groq
from fpdf import FPDF
from io import BytesIO
from PIL import Image
import tempfile
import requests
import os
import markdown
import pdfkit

# Initialize Streamlit app
st.title("Job Description Generator - Application")
st.image("PragyanAI_Transperent_github.png")
# Initialize LLM
API_KEY = "Here API Key"  # Replace with actual API key
#llm = groq.Groq(model="llama3-8b-8192", api_key=API_KEY)
llm_client = groq.Client(api_key=API_KEY)

# Job Title
job_title = st.text_input("Enter Job Title: ")

# Education
education_required = st.checkbox("Require Education Qualification?")
education_details = st.multiselect(
    "Select Education Qualification: Minimum Education Skill", 
    [ "10th","12th","BE", "BCA", "M.E", "MCA", "PhD", "Post Doc"]
)
# Experience
experience = st.slider("Years of Experience", 0, 20, 2)

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
salary_range = st.text_input("Salary Range In Rupees")
company_logo = st.file_uploader("Upload Company Logo", type=["png", "jpg", "jpeg"])
contact_email = st.text_input("Enter the Email of recruiters:")
# Generate Company Description and Role & Responsibilities
if st.button("Generate Company Details"):
    prompt = f"""
    Generate a professional company description based on the company name: {company_name}.
    Also, generate role responsibilities based on the job title: {job_title} and the given key skills.
    """
    
    response = llm_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "system", "content": "You are a helpful AI assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=500
    )
    
    generated_text = response.choices[0].message.content if response.choices else "Could not generate details. Try again."
    
    st.subheader("Generated Company Description & Role Responsibilities")
    st.write(generated_text)
    
    company_description, role_responsibility = generated_text.split("\n\n", 1) if "\n\n" in generated_text else (generated_text, "")

# Generate Job Description
if st.button("Generate Job Description"):
    prompt = f"""
    Generate a detailed and refined Job Description based on the following information:
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
    Contact Details = {contact_email}

    Enhance and refine the JD with additional details where necessary.
    """
    
    # Call to GROQ Llama Model
    response = llm_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "system", "content": "You are a helpful AI assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=1000
    )
    llm_response = response.choices[0].message.content if response.choices else "Generated Job Description based on inputs. (Replace with LLM API Response)"
    
    st.subheader("Generated & Refined Job Description")
    st.write(llm_response)
    
    if company_logo:
        st.image(company_logo, caption="Company Logo")
    # Markdown File Generation
    def generate_md():
        md_output = f"""
        # {job_title}
        
        **Company:** {company_name}  
        **Location:** {location}  
        **Salary Range:** {salary_range}  
        
        ## Job Description  
        {llm_response}
        """
        return md_output
    md_data = generate_md()
    # Save the file locally
    md_file_name = f"{job_title}_Job_Description.md"
    with open(md_file_name, "w", encoding="utf-8") as file:
        file.write(md_data)
    # Streamlit UI to Download the File
    st.download_button(
        label="Download Job Description as Markdown",
        data=md_data,
        file_name=md_file_name,
        mime="text/markdown"
    )

    def md_to_pdf(md_file,name):
        st.write(md_file)
        st.write(name)
        # Read the Markdown file
        with open(md_file, "r", encoding="utf-8") as f:
            md_content = f.read()
    
        # Convert Markdown to HTML
        html_content = markdown.markdown(md_content)
        pdf_file=f"{name}_Job_Description.pdf"
        # Convert HTML to PDF
        pdfkit.from_string(html_content, pdf_file)
        print(f"Converted {md_file} to {pdf_file}")
        return pdf_file
    # Example usage
    pdf_file = md_to_pdf(md_file_name,job_title)
    # Read PDF as bytes for download
    with open(pdf_file, "rb") as pdf:
        pdf_data = pdf.read()
    st.download_button(
        label="Download Job Description PDF",
        data=pdf_data,
        file_name=pdf_file,
        mime="application/pdf"
    )
