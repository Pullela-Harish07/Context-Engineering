# AI-Powered Career Roadmap Generator

An intelligent web application that generates personalized career roadmaps using Google's Gemini AI. This tool helps students and professionals plan their career journey by providing structured guidance on skills, learning stages, tools, projects, and timelines tailored to their experience level and career goals.

## Features

- **Personalized Roadmap Generation**: Creates customized career plans based on your current experience level, target role, and career goals
- **Structured Output**: Organizes roadmap into clear sections including skills, learning stages, tools/technologies, recommended projects, and timeline
- **Interactive UI**: Built with Streamlit for an intuitive and user-friendly experience
- **AI-Powered**: Leverages Google's Gemini 2.5 Flash model for intelligent career guidance
- **Expandable Sections**: View roadmap details in collapsible sections for easy navigation

## Use Cases

- **Students**: Undergraduate and graduate students planning their career path
- **Career Switchers**: Professionals transitioning to new roles or industries
- **Skill Development**: Individuals seeking structured guidance on what to learn next
- **Career Planning**: Anyone looking for a clear roadmap to achieve specific career goals
- **Job Seekers**: Candidates preparing for target roles with actionable learning plans

## Libraries & Technologies Used

- **Streamlit**: Web application framework for creating the interactive UI
- **LangChain**: Framework for building LLM-powered applications
- **LangChain Google GenAI**: Integration for Google's Gemini AI models
- **Python RE (Regular Expressions)**: Text parsing and formatting
- **Google Gemini 2.5 Flash**: Large language model for generating career guidance

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key

## Installation


1. Install required dependencies:
```bash
pip install streamlit langchain langchain-google-genai
```

2. Set up your Google Gemini API key:
   - Open the `app.py` file
   - Replace `___YOUR-GEMINI-API-KEY___` with your actual API key

## Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the URL shown (typically `http://localhost:8501`)

3. Fill in the required information:
   - **Name**: Your name
   - **Current Experience Level**: Select from undergraduate to experienced professional
   - **Target Job Role**: The role you're aiming for (e.g., Data Scientist, Software Engineer)
   - **Career Goal**: Your specific career objective

4. Click "Generate Roadmap for desired role and career"

5. View your personalized roadmap with expandable sections for each component

## How It Works

1. **User Input Collection**: The app collects information about the user's current experience level, target job role, and career goals through an intuitive form interface

2. **Prompt Construction**: User inputs are formatted into a structured prompt template that instructs the AI on what information to generate

3. **AI Processing**: The prompt is sent to Google's Gemini 2.5 Flash model via LangChain, which analyzes the inputs and generates a comprehensive career roadmap

4. **Response Parsing**: The AI-generated response is parsed using regular expressions to separate different sections of the roadmap

5. **Interactive Display**: The parsed roadmap is displayed in expandable sections using Streamlit's expander component for easy navigation

## Roadmap Components

The generated roadmap includes:

1. **Skill-building Guidance**: Specific technical and soft skills to acquire
2. **Learning Stages**: Step-by-step phases to progress through
3. **Tools/Technologies**: Essential tools and platforms to master
4. **Recommended Projects**: Hands-on projects to build practical experience
5. **Timeline**: Suggested duration for each stage and overall completion

## Configuration

You can customize the AI model parameters in the code:

```python
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  # Model version
    temperature=0.7,            # Creativity level (0.0 - 1.0)
    google_api_key=GOOGLE_API_KEY
)
```

```python
import os
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
```

Then set the environment variable before running:
```bash
export GOOGLE_API_KEY="your-api-key-here"
streamlit run app.py
```

e