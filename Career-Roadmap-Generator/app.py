import streamlit as st
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

st.title('AI-Powered Career Roadmap Generator')
st.write('Welcome to the AI-Powered Career Roadmap Generator!')


st.header('Personal Information')

name = st.text_input('Name')

experience_level = st.selectbox(
    'Current Experience Level',
    ['Undergraduate Student (Like a B.tech student)', 'Graduate Student (Recent B.tech graduate)', 'Entry-Level Professional (1 - 2 years experience)', 'Mid-Career Professional (2 - 5 years experience)', 'Experienced Professional (5 - 10 years experience)']
)

target_jobrole = st.text_input('Target Job Role (e.g., Data Scientist, Software Engineer)')

career_goal = st.text_area('Career Goal (e.g., lead a team, excel in the particular role)')

GOOGLE_API_KEY = "___YOUR-GEMINI-API-KEY___"

# Gemini model via LangChain
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, google_api_key=GOOGLE_API_KEY)

# Button to generate roadmap
if st.button('Generate Roadmap for desired role and career'):
    if not name or not target_jobrole or not career_goal:
        st.warning('Please fill in all the required fields (Name, Target Job Role, Career Goal) to generate a roadmap.')
    else:
        st.write('Generating roadmap for:', name)

        # The prompt template
        prompt_template = ChatPromptTemplate.from_template("""
        Generate a structured career roadmap with the following details:
        Current Experience Level: {experience_level}
        Target Job Role: {target_jobrole}
        Career Goal: {career_goal}

        The roadmap should include:
        1. Skill-building guidance: Specific skills to acquire.
        2. Learning stages: A breakdown of the journey into distinct phases.
        3. Tools/Technologies to master: Essential tools and technologies to learn.
        4. Recommended Projects for Practical Knowledge: Practical projects to build experience.
        5. Timeline: A suggested duration for each stage or overall completion.
        

        Format the output clearly and concisely, using headings for each section.
        """)

        chain = prompt_template | llm

        try:
            roadmap_response = chain.invoke({
                "experience_level": experience_level,
                "target_jobrole": target_jobrole,
                "career_goal": career_goal
            })

            response_text = roadmap_response.content


            sections = re.split(r'\n(?=\d+\.)', response_text)

            st.subheader('Your Personalized Career Roadmap:')
            for section in sections:
                if section.strip():
                    title = "Career Roadmap"
                    content = section.strip()

                    with st.expander(title):
                        st.markdown(content)

        except Exception as e:
            st.error(f"An error occurred while generating the roadmap: {e}")