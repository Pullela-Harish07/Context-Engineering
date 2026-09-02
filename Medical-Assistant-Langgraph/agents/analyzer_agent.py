# import json
# from typing import Dict
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import ChatPromptTemplate
# from config.settings import settings
# from graph.state import MedicalState
#
#
# class MedicalAnalyzerAgent:
#     """
#     Agent 1: Analyzes medical reports and classifies severity
#
#     Why separate agent?
#     - Specialized medical knowledge domain
#     - Complex extraction and classification logic
#     - Can be upgraded with medical-specific models later
#     """
#
#     def __init__(self):
#         self.llm = ChatGoogleGenerativeAI(
#             model=settings.MODEL_NAME,
#             temperature=settings.TEMPERATURE,
#             google_api_key=settings.GOOGLE_API_KEY
#         )
#
#         self.analysis_prompt = ChatPromptTemplate.from_messages([
#             ("system", """You are an expert medical report analyzer. Your role is to:
#                 1. Read and understand medical reports (lab results, imaging reports, clinical notes)
#                 2. Identify key findings and abnormalities
#                 3. Classify severity level
#                 4. Recommend appropriate medical department
#
#             IMPORTANT GUIDELINES:
#                 - Be conservative in severity classification
#                 - Look for critical indicators: extremely abnormal values, urgent keywords
#                 - Normal: All values within reference ranges, no concerns
#                 - Mild: Slightly abnormal values, non-urgent conditions
#                 - Critical: Severely abnormal values, emergency keywords, life-threatening indicators
#
#             Output ONLY valid JSON with this exact structure:
#             {{
#                  "summary": "Brief 2-3 sentence summary in simple language",
#                  "severity": "normal|mild|critical",
#                  "identified_conditions": ["condition1", "condition2"],
#                  "department": "cardiology|neurology|orthopedics|general_medicine|emergency|etc",
#                  "key_findings": {{ "finding1": "value/description", "finding2": "value/description"
#             }},"reasoning": "Why this severity classification"
#         }}"""),
#             ("user", "Analyze this medical report:\n\n{report_text}")
#         ])
#
#     def analyze(self, state: MedicalState) -> MedicalState:
#         """
#         Input: raw_input (text extracted from PDF/image/text)
#         Output: Updates state with analysis results
#         """
#         try:
#             report_text = state["raw_input"]
#
#             # Call Gemini for analysis
#             chain = self.analysis_prompt | self.llm
#             response = chain.invoke({"report_text": report_text})
#
#             # Parse JSON response
#             # Remove markdown code blocks if present
#             content = response.content.strip()
#             if content.startswith("```json"):
#                 content = content[7:]
#             if content.endswith("```"):
#                 content = content[:-3]
#
#             analysis = json.loads(content.strip())
#
#             # Update state
#             state["report_summary"] = analysis["summary"]
#             state["severity"] = analysis["severity"]
#             state["identified_conditions"] = analysis["identified_conditions"]
#             state["department"] = analysis["department"]
#             state["key_findings"] = analysis["key_findings"]
#             state["workflow_stage"] = "analysis_complete"
#
#             return state
#
#         except Exception as e:
#             state["error_message"] = f"Analysis error: {str(e)}"
#             state["workflow_stage"] = "error"
#             return state
#
#
# # Instantiate agent
# analyzer_agent = MedicalAnalyzerAgent()


import json
from typing import Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from config.settings import settings
from graph.state import MedicalState


class MedicalAnalyzerAgent:
    """
    Agent 1: Analyzes medical reports and classifies severity
    NOW ALSO EXTRACTS: Patient name, location from report
    """

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            google_api_key=settings.GOOGLE_API_KEY
        )

        self.analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert medical report analyzer. Your role is to:
                1. Read and understand medical reports (lab results, imaging reports, clinical notes)
                2. Extract patient information (name, location/city)
                3. Identify key findings and abnormalities
                4. Classify severity level
                5. Recommend appropriate medical department
            
            LOCATION EXTRACTION RULES:
                 - Look for: "Hospital:", "Lab:", "Location:", "City:", "Address:", "Branch:"
                 - Extract the city name (e.g., "Apollo Hospital, Bangalore" → extract "Bangalore")
                 - Common cities: Bangalore, Chennai, Delhi, Mumbai, Hyderabad, Pune, Kolkata
                 - If no city found, use "Bangalore" as default
            
            SEVERITY CLASSIFICATION:
                 - Normal: All values within reference ranges, no concerns
                 - Mild: Slightly abnormal values, non-urgent conditions
                 - Critical: Severely abnormal values, emergency keywords, life-threatening indicators
            
            Output ONLY valid JSON with this exact structure:
            {{
                 "patient_name": "extracted name or 'Patient' if not found",
                 "patient_location": "extracted city or 'Bangalore' if not found",
                 "summary": "Brief 2-3 sentence summary in simple language",
                 "severity": "normal|mild|critical",
                 "identified_conditions": ["condition1", "condition2"],
                 "department": "cardiology|neurology|orthopedics|general_medicine|emergency|hematology|etc",
                 "key_findings": {{
                      "finding1": "value/description",
                      "finding2": "value/description"
                }},
                "reasoning": "Why this severity classification"
            }}"""),
            ("user", "Analyze this medical report and extract patient name and location:\n\n{report_text}")
        ])

    def analyze(self, state: MedicalState) -> MedicalState:
        """
        Main analysis function
        NOW EXTRACTS: patient_name, patient_location from report
        """
        try:
            report_text = state["raw_input"]

            # Call Gemini for analysis
            chain = self.analysis_prompt | self.llm
            response = chain.invoke({"report_text": report_text})

            # Parse JSON response
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]

            analysis = json.loads(content.strip())

            # Update state with EXTRACTED information
            state["patient_name"] = analysis.get("patient_name", "Patient")
            state["patient_location"] = analysis.get("patient_location", "Bangalore")
            state["report_summary"] = analysis["summary"]
            state["severity"] = analysis["severity"]
            state["identified_conditions"] = analysis["identified_conditions"]
            state["department"] = analysis["department"]
            state["key_findings"] = analysis["key_findings"]
            state["workflow_stage"] = "analysis_complete"

            return state

        except Exception as e:
            state["error_message"] = f"Analysis error: {str(e)}"
            state["workflow_stage"] = "error"
            return state


# Instantiate agent
analyzer_agent = MedicalAnalyzerAgent()