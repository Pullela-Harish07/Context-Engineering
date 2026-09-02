import json
from typing import List
from graph.state import MedicalState, DoctorInfo


class DoctorRecommenderAgent:
    """
    Agent 2: Recommends doctors based on department and location

    Why separate agent?
    - Domain-specific logic (matching, ranking, filtering)
    - Can integrate with real hospital APIs later
    - Isolated testing of recommendation algorithm
    """

    def __init__(self, doctors_db_path: str = "data/doctors_database.json"):
        with open(doctors_db_path, 'r') as f:
            self.doctors_db = json.load(f)["doctors"]

    def recommend(self, state: MedicalState) -> MedicalState:
        """
        Find and rank doctors based on: 1. Specialization match, 2. Location match, 3. Experience and rating
        """
        try:
            department = state.get("department", "general_medicine")
            location = state.get("patient_location", "Bangalore")

            # Filter by specialization
            matching_doctors = [
                doc for doc in self.doctors_db
                if doc["specialization"].lower() == department.lower()
            ]

            # If no exact match, fallback to general medicine
            if not matching_doctors:
                matching_doctors = [
                    doc for doc in self.doctors_db
                    if doc["specialization"].lower() == "general_medicine"
                ]

            # Prefer doctors in patient's location
            local_doctors = [
                doc for doc in matching_doctors
                if doc["location"].lower() == location.lower()
            ]

            # If no local doctors, show all matching
            final_doctors = local_doctors if local_doctors else matching_doctors

            # Sort by rating (desc) then experience (desc)
            final_doctors.sort(
                key=lambda x: (x["rating"], x["experience_years"]),
                reverse=True
            )

            # Take top 5
            recommended = final_doctors[:5]

            state["recommended_doctors"] = recommended
            state["workflow_stage"] = "doctors_recommended"

            return state

        except Exception as e:
            state["error_message"] = f"Recommendation error: {str(e)}"
            state["workflow_stage"] = "error"
            return state


# Instantiate agent
recommender_agent = DoctorRecommenderAgent()