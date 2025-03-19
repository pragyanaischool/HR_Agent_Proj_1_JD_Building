import streamlit as st
import groq

# Initialize Streamlit app
st.title("Job Description Generator")

# Job Title
job_title = st.text_input("Enter Job Title")

# Education
education_required = st.checkbox("Require Education Qualification?")
education_details = st.text_input("Specify Education Qualification", "Bachelors in Computer Science") if education_required else ""

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
    Experience: {experience} years
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
    
    # Call to GROQ or LLAMA API (Mockup, Replace with actual API call)
    llm_response = "Generated Job Description based on inputs. (Replace with LLM API Response)"
    
    st.subheader("Generated Job Description")
    st.write(llm_response)
    
    if company_logo:
        st.image(company_logo, caption="Company Logo")
