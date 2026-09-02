from typing import TypedDict, List, Optional, Dict, Literal
from datetime import datetime


class DoctorInfo(TypedDict):
    """Doctor information structure"""
    doctor_id: str
    name: str
    specialization: str
    hospital: str
    location: str
    experience_years: int
    rating: float
    email: str
    phone: str
    consultation_fee: int


class AppointmentInfo(TypedDict):
    """Appointment details structure"""
    appointment_id: str
    doctor: DoctorInfo
    patient_name: str
    patient_email: str
    patient_phone: str
    date: str
    time: str
    reason: str


class MedicalState(TypedDict):
    """
    Central state that flows through all agents
    This is the 'memory' of the system
    """
    # Input data
    input_type: Literal["text", "pdf", "image"]
    raw_input: str
    patient_name: Optional[str]
    patient_email: Optional[str]
    patient_phone: Optional[str]
    patient_location: Optional[str]

    # Agent 1 outputs
    report_summary: Optional[str]
    severity: Optional[Literal["normal", "mild", "critical"]]
    identified_conditions: Optional[List[str]]
    department: Optional[str]
    key_findings: Optional[Dict[str, str]]

    # Agent 2 outputs
    recommended_doctors: Optional[List[DoctorInfo]]
    selected_doctor: Optional[DoctorInfo]

    # Agent 3 outputs
    appointment_details: Optional[AppointmentInfo]

    # Agent 4 outputs
    email_sent: Optional[bool]
    notification_status: Optional[str]

    # Metadata
    workflow_stage: str
    timestamp: str
    error_message: Optional[str]