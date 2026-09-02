# from graph.state import MedicalState
# from utils.email_sender import EmailService
#
#
# class NotificationAgent:
#     """
#     Agent 4: Sends confirmation emails to doctor and patient
#
#     Why separate agent?
#     - Isolated communication logic
#     - Can add SMS, WhatsApp notifications later
#     - Handles email formatting and delivery
#     """
#
#     def __init__(self):
#         self.email_service = EmailService()
#
#     def notify(self, state: MedicalState) -> MedicalState:
#         """Send appointment confirmations"""
#         try:
#             appointment = state.get("appointment_details")
#             if not appointment:
#                 raise ValueError("No appointment to notify")
#
#             # Send to patient
#             patient_success = self._send_patient_email(appointment)
#
#             # Send to doctor
#             doctor_success = self._send_doctor_email(appointment)
#
#             state["email_sent"] = patient_success and doctor_success
#             state["notification_status"] = "Emails sent successfully" if state["email_sent"] else "Email sending failed"
#             state["workflow_stage"] = "complete"
#
#             return state
#
#         except Exception as e:
#             state["error_message"] = f"Notification error: {str(e)}"
#             state["workflow_stage"] = "error"
#             return state
#
#     def _send_patient_email(self, appointment) -> bool:
#         """Format and send patient confirmation"""
#         subject = f"Appointment Confirmation - {appointment['appointment_id']}"
#
#         body = f"""
#         <html>
#         <body style="font-family: Arial, sans-serif;">
#             <h2 style="color: #2c3e50;">Appointment Confirmed ✅</h2>
#
#             <p>Dear {appointment['patient_name']},</p>
#
#             <p>Your appointment has been successfully booked.</p>
#
#             <div style="background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0;">
#                 <h3 style="color: #34495e;">Appointment Details:</h3>
#                 <p><strong>Appointment ID:</strong> {appointment['appointment_id']}</p>
#                 <p><strong>Doctor:</strong> {appointment['doctor']['name']}</p>
#                 <p><strong>Specialization:</strong> {appointment['doctor']['specialization'].title()}</p>
#                 <p><strong>Hospital:</strong> {appointment['doctor']['hospital']}</p>
#                 <p><strong>Date:</strong> {appointment['date']}</p>
#                 <p><strong>Time:</strong> {appointment['time']}</p>
#                 <p><strong>Consultation Fee:</strong> ₹{appointment['doctor']['consultation_fee']}</p>
#             </div>
#
#             <p><strong>Contact:</strong> {appointment['doctor']['phone']}</p>
#
#             <p style="color: #7f8c8d; font-size: 12px; margin-top: 30px;">
#                 Please arrive 15 minutes early and bring all relevant medical documents.
#             </p>
#
#             <p style="color: #e74c3c; font-size: 11px;">
#                 ⚠️ This is an automated message. For changes, contact the hospital directly.
#             </p>
#         </body>
#         </html>
#         """
#
#         return self.email_service.send_email(
#             appointment['patient_email'],
#             subject,
#             body
#         )
#
#     def _send_doctor_email(self, appointment) -> bool:
#         """Format and send doctor notification"""
#         subject = f"New Appointment - {appointment['appointment_id']}"
#
#         body = f"""
#         <html>
#         <body style="font-family: Arial, sans-serif;">
#             <h2 style="color: #2c3e50;">New Appointment Scheduled 📅</h2>
#
#             <p>Dear Dr. {appointment['doctor']['name'].split()[-1]},</p>
#
#             <p>A new appointment has been booked with you.</p>
#
#             <div style="background-color: #e8f5e9; padding: 15px; border-radius: 5px; margin: 20px 0;">
#                 <h3 style="color: #2e7d32;">Patient Information:</h3>
#                 <p><strong>Patient Name:</strong> {appointment['patient_name']}</p>
#                 <p><strong>Contact:</strong> {appointment['patient_phone']}</p>
#                 <p><strong>Email:</strong> {appointment['patient_email']}</p>
#                 <p><strong>Date:</strong> {appointment['date']}</p>
#                 <p><strong>Time:</strong> {appointment['time']}</p>
#             </div>
#
#             <div style="background-color: #fff3e0; padding: 15px; border-radius: 5px;">
#                 <h3 style="color: #e65100;">Reason for Visit:</h3>
#                 <p>{appointment['reason']}</p>
#             </div>
#
#             <p style="color: #7f8c8d; font-size: 12px; margin-top: 30px;">
#                 Appointment ID: {appointment['appointment_id']}
#             </p>
#         </body>
#         </html>
#         """
#
#         return self.email_service.send_email(
#             appointment['doctor']['email'],
#             subject,
#             body
#         )
#
#
# # Instantiate agent
# notifier_agent = NotificationAgent()


from graph.state import MedicalState


class NotificationAgent:
    """
    Agent 4: Sends confirmation emails to doctor and patient
    DEMO MODE: Prints to console instead of sending real emails
    """

    def __init__(self):
        self.demo_mode = True  # Set to False when you have real SMTP

    def notify(self, state: MedicalState) -> MedicalState:
        """Send appointment confirmations"""
        try:
            appointment = state.get("appointment_details")
            if not appointment:
                raise ValueError("No appointment to notify")

            if self.demo_mode:
                # DEMO MODE: Just print instead of sending
                print("\n" + "=" * 70)
                print("EMAIL NOTIFICATION - DEMO MODE")
                print("=" * 70)

                print("\n PATIENT EMAIL:")
                print(f"To: {appointment['patient_email']}")
                print(f"Subject: Appointment Confirmation - {appointment['appointment_id']}")
                print(f"\nDear {appointment['patient_name']},")
                print(f"Your appointment is confirmed with Dr. {appointment['doctor']['name']}")
                print(f"Date: {appointment['date']} at {appointment['time']}")
                print(f"Hospital: {appointment['doctor']['hospital']}")
                print(f"Fee: ₹{appointment['doctor']['consultation_fee']}")

                print("\n" + "-" * 70)

                print("\n DOCTOR EMAIL:")
                print(f"To: {appointment['doctor']['email']}")
                print(f"Subject: New Appointment - {appointment['appointment_id']}")
                print(f"\nDear Dr. {appointment['doctor']['name']},")
                print(f"New appointment with {appointment['patient_name']}")
                print(f"Date: {appointment['date']} at {appointment['time']}")
                print(f"Contact: {appointment['patient_phone']}")

                print("\n" + "=" * 70)

                # Mark as sent (demo)
                state["email_sent"] = True
                state["notification_status"] = "Emails sent (DEMO MODE - Check console)"
            else:
                # Real email sending (when SMTP is configured)
                from utils.email_sender import EmailService
                email_service = EmailService()

                patient_success = self._send_patient_email(appointment, email_service)
                doctor_success = self._send_doctor_email(appointment, email_service)

                state["email_sent"] = patient_success and doctor_success
                state["notification_status"] = "Emails sent successfully" if state[
                    "email_sent"] else "Email sending failed"

            state["workflow_stage"] = "complete"
            return state

        except Exception as e:
            state["error_message"] = f"Notification error: {str(e)}"
            state["workflow_stage"] = "error"
            return state

    def _send_patient_email(self, appointment, email_service) -> bool:
        """Format and send patient confirmation"""
        subject = f"Appointment Confirmation - {appointment['appointment_id']}"
        body = f"""
        <html><body style="font-family: Arial;">
            <h2>Appointment Confirmed</h2>
            <p>Dear {appointment['patient_name']},</p>
            <p><strong>Appointment ID:</strong> {appointment['appointment_id']}</p>
            <p><strong>Doctor:</strong> {appointment['doctor']['name']}</p>
            <p><strong>Date:</strong> {appointment['date']}</p>
            <p><strong>Time:</strong> {appointment['time']}</p>
            <p><strong>Hospital:</strong> {appointment['doctor']['hospital']}</p>
            <p><strong>Fee:</strong> ₹{appointment['doctor']['consultation_fee']}</p>
        </body></html>
        """
        return email_service.send_email(appointment['patient_email'], subject, body)

    def _send_doctor_email(self, appointment, email_service) -> bool:
        """Format and send doctor notification"""
        subject = f"New Appointment - {appointment['appointment_id']}"
        body = f"""
        <html><body style="font-family: Arial;">
            <h2>New Appointment</h2>
            <p>Dear Dr. {appointment['doctor']['name']},</p>
            <p><strong>Patient:</strong> {appointment['patient_name']}</p>
            <p><strong>Date:</strong> {appointment['date']}</p>
            <p><strong>Time:</strong> {appointment['time']}</p>
            <p><strong>Phone:</strong> {appointment['patient_phone']}</p>
        </body></html>
        """
        return email_service.send_email(appointment['doctor']['email'], subject, body)


# Instantiate agent
notifier_agent = NotificationAgent()