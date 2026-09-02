import uuid
from datetime import datetime
from graph.state import MedicalState, AppointmentInfo


class AppointmentSchedulerAgent:
    """
    Agent 3: Books appointments with selected doctors

    Why separate agent?
    - Handles temporal logic (dates, time slots)
    - Can integrate with real calendar APIs (Google Calendar, hospital systems)
    - Validates scheduling constraints
    """

    def __init__(self):
        # In production, this would connect to a real calendar system
        self.booked_appointments = []

    def schedule(self, state: MedicalState) -> MedicalState:
        """
        Input: selected_doctor, patient details, preferred date/time
        Output: Appointment confirmation with unique ID
        """
        try:
            doctor = state.get("selected_doctor")
            if not doctor:
                raise ValueError("No doctor selected")

            # Generate unique appointment ID
            appointment_id = f"APT-{uuid.uuid4().hex[:8].upper()}"

            # Create appointment record
            appointment: AppointmentInfo = {
                "appointment_id": appointment_id,
                "doctor": doctor,
                "patient_name": state.get("patient_name", "Unknown"),
                "patient_email": state.get("patient_email", ""),
                "patient_phone": state.get("patient_phone", ""),
                "date": state.get("appointment_date", ""),
                "time": state.get("appointment_time", ""),
                "reason": state.get("report_summary", "Medical consultation")
            }

            # Store booking
            self.booked_appointments.append(appointment)

            state["appointment_details"] = appointment
            state["workflow_stage"] = "appointment_scheduled"

            return state

        except Exception as e:
            state["error_message"] = f"Scheduling error: {str(e)}"
            state["workflow_stage"] = "error"
            return state

    def check_availability(self, doctor_id: str, date: str, time: str) -> bool:
        """
        Check if slot is available
        """
        # Simulate availability check
        for apt in self.booked_appointments:
            if (apt["doctor"]["doctor_id"] == doctor_id and
                    apt["date"] == date and
                    apt["time"] == time):
                return False
        return True


# Instantiate agent
scheduler_agent = AppointmentSchedulerAgent()