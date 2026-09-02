import streamlit as st
from datetime import datetime, timedelta
from graph.state import MedicalState
from graph.workflow import medical_workflow
from utils.pdf_parser import PDFParser
from utils.image_parser import ImageParser
from agents.scheduler_agent import scheduler_agent
from agents.notifier_agent import notifier_agent

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Medical Assistant AI",
    page_icon="🏥",
    layout="wide"
)

# ============================================================================
# MINIMAL CSS
# ============================================================================
st.markdown("""
<style>
    .severity-normal {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        color: #155724;
    }

    .severity-mild {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        color: #856404;
    }

    .severity-critical {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================
if 'state' not in st.session_state:
    st.session_state.state = None
if 'extracted_patient_info' not in st.session_state:
    st.session_state.extracted_patient_info = None

# ============================================================================
# HEADER
# ============================================================================
st.title(" Medical Assistant AI ")
st.caption(" Multi-Agent System powered by LangGraph & Gemini 2.5 Flash ")

if st.button(" Start New Analysis "):
    st.session_state.state = None
    st.session_state.extracted_patient_info = None
    st.rerun()

st.divider()

# ============================================================================
# TABS
# ============================================================================
tab1, tab2, tab3 = st.tabs(["1️⃣ Upload Report", "2️⃣ View Analysis", "3️⃣ Book Appointment"])

# ============================================================================
# TAB 1: UPLOAD REPORT
# ============================================================================
with tab1:
    st.header("Upload Medical Report")

    input_method = st.radio("Choose input method:", ["Text", "PDF", "Image"])

    raw_input = None
    input_type = None

    if input_method == "Text":
        raw_input = st.text_area(
            "Enter report text:",
            height=300,
            placeholder="Paste your complete medical report here...\n\nExample:\nPatient: John Doe\nAge: 45\nDate: 2024-12-20\n\nTest Results:\nHemoglobin: 10.2 g/dL..."
        )
        if raw_input and raw_input.strip():
            input_type = "text"
            st.success(f" Text received ({len(raw_input)} characters) ")

    elif input_method == "PDF":
        pdf_file = st.file_uploader("Upload PDF report", type=['pdf'])
        if pdf_file:
            try:
                with st.spinner("Extracting text from PDF..."):
                    raw_input = PDFParser.extract_text(pdf_file)
                    input_type = "pdf"

                if raw_input:
                    st.success(f" PDF processed ({len(raw_input)} characters) ")
                    with st.expander("Preview extracted text"):
                        st.text(raw_input[:500] + ("..." if len(raw_input) > 500 else ""))
                else:
                    st.warning("No text found in PDF")
            except Exception as e:
                st.error(f"Error processing PDF: {str(e)}")

    elif input_method == "Image":
        image_file = st.file_uploader("Upload image of report", type=['jpg', 'jpeg', 'png'])
        if image_file:
            try:
                st.image(image_file, caption="Uploaded Image", width=400)

                with st.spinner("Performing OCR..."):
                    raw_input = ImageParser.extract_text(image_file)
                    input_type = "image"

                if raw_input and len(raw_input.strip()) > 10:
                    st.success(f" Text extracted ({len(raw_input)} characters) ")
                    with st.expander("Preview extracted text"):
                        st.text(raw_input[:500] + ("..." if len(raw_input) > 500 else ""))
                else:
                    st.warning(" No text detected. Ensure image is clear and text is visible. ")
            except Exception as e:
                st.error(f"Error processing image: {str(e)}")

    st.divider()

    # Analyze Button
    if st.button(" Analyze Report ", type="primary", disabled=not raw_input):

        with st.spinner(" AI agents analyzing report..."):

            # Create initial state without patient details (will be extracted from report)
            initial_state: MedicalState = {
                "input_type": input_type,
                "raw_input": raw_input,
                "patient_name": None,  # Will be extracted if present
                "patient_email": "",
                "patient_phone": "",
                "patient_location": None,  # Default location
                "report_summary": None,
                "severity": None,
                "identified_conditions": None,
                "department": None,
                "key_findings": None,
                "recommended_doctors": None,
                "selected_doctor": None,
                "appointment_details": None,
                "email_sent": None,
                "notification_status": None,
                "workflow_stage": "started",
                "timestamp": datetime.now().isoformat(),
                "error_message": None
            }

            try:
                result = medical_workflow.invoke(initial_state)
                st.session_state.state = result
                st.session_state.workflow_stage = result.get("workflow_stage", "complete")
                st.success(" Analysis complete! ")
                st.info(" Go to **'View Analysis'** tab to see results ")
            except Exception as e:
                st.error(f" Analysis error: {str(e)}")
                with st.expander("Error details"):
                    st.code(str(e))

# ============================================================================
# TAB 2: VIEW ANALYSIS
# ============================================================================
with tab2:
    st.header("Analysis Results")

    if st.session_state.state is None:
        st.info(" Please upload and analyze a report in Step 1 first ")
    else:
        state = st.session_state.state

        if state.get("error_message"):
            st.error(f"Error: {state['error_message']}")
            st.stop()

        # Show extracted patient information
        st.subheader("📋 Extracted Information")
        col_info1, col_info2 = st.columns(2)

        with col_info1:
            st.write(f"**Patient Name:** {state.get('patient_name', 'Not found')}")

        with col_info2:
            st.write(f"**Location:** {state.get('patient_location', 'Not found')}")

        st.divider()

        # Severity Display
        severity = state.get("severity", "unknown")
        severity_text = {
            "normal": "✅ NORMAL - No Immediate Concern",
            "mild": "⚠️ MILD - Medical Consultation Recommended",
            "critical": "🚨 CRITICAL - Urgent Medical Attention Required"
        }

        st.markdown(
            f'<div class="severity-{severity}"><h2>{severity_text.get(severity, "Unknown")}</h2></div>',
            unsafe_allow_html=True
        )

        st.divider()

        # Summary
        st.subheader(" Report Summary ")
        st.info(state.get("report_summary", "No summary available"))

        # Two columns for conditions and department
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(" Identified Conditions ")
            conditions = state.get("identified_conditions", [])
            if conditions:
                for idx, condition in enumerate(conditions, 1):
                    st.write(f"{idx}. {condition}")
            else:
                st.write(" No specific conditions identified ")

        with col2:
            st.subheader(" Recommended Department ")
            dept = state.get("department", "General Medicine")
            st.write(f"**{dept.replace('_', ' ').title()}**")

        # Key Findings
        st.subheader(" Key Findings ")
        findings = state.get("key_findings", {})
        if findings:
            for key, value in findings.items():
                st.write(f"**{key}:** {value}")
        else:
            st.write("No specific findings")

        st.divider()

        # Doctor Recommendations
        if severity == "normal":
            st.success(" **Great News!** Your report shows normal results. ")
            st.write("**Recommendations:**")
            st.write("• Maintain a healthy lifestyle")
            st.write("• Regular check-ups as advised")
            st.write("• Contact a doctor if you experience symptoms")
        else:
            st.subheader(" Recommended Doctors ")
            doctors = state.get("recommended_doctors", [])

            if doctors:
                for idx, doc in enumerate(doctors):
                    with st.expander(f" Dr. {doc['name']} - {doc['specialization'].title()}"):
                        col_a, col_b = st.columns(2)

                        with col_a:
                            st.write(f"**Hospital:** {doc['hospital']}")
                            st.write(f"**Location:** {doc['location']}")
                            st.write(f"**Experience:** {doc['experience_years']} years")

                        with col_b:
                            st.write(f"**Rating:** {doc['rating']}/5.0")
                            st.write(f"**Consultation Fee:** ₹{doc['consultation_fee']}")
                            st.write(f"**Phone:** {doc['phone']}")

                        if st.button(f" Select Dr. {doc['name']}", key=f"select_doc_{idx}"):
                            st.session_state.state["selected_doctor"] = doc
                            st.success(f" Selected Dr. {doc['name']} ")
                            st.info(" Go to **'Book Appointment'** tab ")
            else:
                st.warning("No doctors found for this specialization")

# ============================================================================
# TAB 3: BOOK APPOINTMENT
# ============================================================================
with tab3:
    st.header("Book Appointment")

    if st.session_state.state is None:
        st.info(" Complete Steps 1 & 2 first ")
    elif st.session_state.state.get("severity") == "normal":
        st.success("✅ Your report is normal. No appointment needed at this time.")
    elif not st.session_state.state.get("selected_doctor"):
        st.warning("⚠️ Please select a doctor from the 'View Analysis' tab")
    else:
        doctor = st.session_state.state["selected_doctor"]

        # Show selected doctor
        st.success(f" Booking with: **Dr. {doctor['name']}** ")
        st.write(f"**Hospital:** {doctor['hospital']} | **Location:** {doctor['location']}")
        st.write(f"**Consultation Fee:** ₹{doctor['consultation_fee']}")

        st.divider()

        # In TAB 3, update the contact information section:

        st.subheader("Contact Information")
        st.caption("Required for appointment confirmation")

        # Get extracted info from state
        extracted_name = st.session_state.state.get("patient_name", "")
        extracted_location = st.session_state.state.get("patient_location", "Bangalore")

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            patient_name = st.text_input(
                "Your Name",
                value=extracted_name if extracted_name != "Patient" else "",
                placeholder="John Doe"
            )
            patient_email = st.text_input("Your Email", placeholder="john@example.com")
        with col_p2:
            patient_phone = st.text_input("Your Phone", placeholder="+91-9876543210")

            # Pre-select the extracted location
            cities = ["Bangalore", "Chennai", "Delhi", "Mumbai", "Hyderabad", "Pune"]
            default_index = cities.index(extracted_location) if extracted_location in cities else 0

            patient_location = st.selectbox(
                "Your City",
                cities,
                index=default_index,
                help="Pre-filled from your report"
            )

        st.info(f" Location auto-detected from report: **{extracted_location}**")

        st.divider()

        # Appointment Details
        st.subheader("📅 Appointment Details")

        col1, col2 = st.columns(2)

        with col1:
            min_date = datetime.now().date() + timedelta(days=1)
            max_date = min_date + timedelta(days=30)
            appointment_date = st.date_input("Select Date", min_value=min_date, max_value=max_date)

        with col2:
            time_slots = [
                "09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM",
                "11:00 AM", "11:30 AM", "02:00 PM", "02:30 PM",
                "03:00 PM", "03:30 PM", "04:00 PM", "04:30 PM"
            ]
            appointment_time = st.selectbox("Select Time", time_slots)

        reason = st.text_area(
            "Reason for visit (optional)",
            value=st.session_state.state.get("report_summary", ""),
            height=100
        )

        st.divider()

        # Confirmation
        terms = st.checkbox(" I confirm the appointment details are correct ")

        if st.button("📅 Confirm Booking", type="primary",
                     disabled=not (terms and patient_name and patient_email and patient_phone)):

            # Update state with contact info
            st.session_state.state["patient_name"] = patient_name
            st.session_state.state["patient_email"] = patient_email
            st.session_state.state["patient_phone"] = patient_phone
            st.session_state.state["patient_location"] = patient_location
            st.session_state.state["appointment_date"] = str(appointment_date)
            st.session_state.state["appointment_time"] = appointment_time

            with st.spinner("📅 Booking appointment and sending confirmations..."):

                # Schedule appointment
                state_after_schedule = scheduler_agent.schedule(st.session_state.state)

                # Send email notifications
                final_state = notifier_agent.notify(state_after_schedule)

                st.session_state.state = final_state

                if final_state.get("email_sent"):
                    appointment = final_state["appointment_details"]

                    st.success("**Appointment Booked Successfully!**")

                    # Show appointment details
                    st.subheader(" Booking Confirmation ")
                    st.write(f"**Appointment ID:** `{appointment['appointment_id']}`")
                    st.write(f"**Patient:** {appointment['patient_name']}")
                    st.write(f"**Doctor:** Dr. {appointment['doctor']['name']}")
                    st.write(f"**Hospital:** {appointment['doctor']['hospital']}")
                    st.write(f"**Date:** {appointment['date']}")
                    st.write(f"**Time:** {appointment['time']}")
                    st.write(f"**Fee:** ₹{appointment['doctor']['consultation_fee']}")

                    st.divider()

                    st.info(
                        f" Confirmation emails sent to:\n- Patient: {appointment['patient_email']}\n- Doctor: {appointment['doctor']['email']}")

                    st.write("**Next Steps:**")
                    st.write("• Check your email for confirmation")
                    st.write("• Arrive 15 minutes early")
                    st.write("• Bring relevant medical documents")

                else:
                    st.error("Appointment created but email sending failed")
                    st.warning("Please check your SMTP configuration in .env file")

                    if final_state.get("appointment_details"):
                        apt_id = final_state["appointment_details"]["appointment_id"]
                        st.info(
                            f"**Appointment ID:** {apt_id}\n\nPlease note this ID and contact the hospital directly.")