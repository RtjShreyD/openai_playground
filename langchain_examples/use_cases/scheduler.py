import argparse
import json
import os

def book_patient_appointment(details):
    # Create the directory if it doesn't exist
    if not os.path.exists('appointments'):
        os.makedirs('appointments')

    # Define the file path
    file_path = 'appointments/appointments.json'

    # Load existing data if the file exists, or create an empty list
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            appointments_list = json.load(file)
    else:
        appointments_list = []

    # Add the new appointment details to the list
    appointments_list.append(details)

    # Write the updated list back to the file
    with open(file_path, 'w') as file:
        json.dump(appointments_list, file, indent=4)

    # Return a success message
    return "Appointment booked successfully!"

def main():
    parser = argparse.ArgumentParser(description='Book a patient appointment.')
    parser.add_argument('-n', '--patient_name', required=True, help='Patient name')
    parser.add_argument('-e', '--patient_email', required=True, help='Patient email')
    parser.add_argument('-p', '--patient_phone', required=True, help='Patient phone number')
    parser.add_argument('-c', '--patient_case', required=True, help='Patient case description')
    parser.add_argument('-d', '--doctor_name', required=True, help='Doctor to visit')
    parser.add_argument('-dept', '--department_name', required=True, help='Department name')
    parser.add_argument('-a', '--appointment_date', required=True, help='Date of appointment in dd/mm/yy format')
    parser.add_argument('-t', '--appointment_time', required=True, help='Time of appointment in hh:mm am/pm format')
    parser.add_argument('-se', '--send_email', required=True, type=bool, help='Whether to send email or not (True/False)')
    parser.add_argument('-ss', '--send_sms', required=True, type=bool, help='Whether to send SMS or not (True/False)')

    args = parser.parse_args()

    appointment_details = {
        'patient_name': args.patient_name,
        'patient_email': args.patient_email,
        'patient_phone': args.patient_phone,
        'patient_case': args.patient_case,
        'doctor_name': args.doctor_name,
        'department_name': args.department_name,
        'appointment_date': args.appointment_date,
        'appointment_time': args.appointment_time,
        'send_email': args.send_email,
        'send_sms': args.send_sms
    }

    result = book_patient_appointment(appointment_details)
    print(result)

if __name__ == "__main__":
    main()

# python scheduler.py -n "Mark Johanson" -e "markjoan@example.com" -p "555-6321" -c "Dental Checkup" -d "Dr. Joseph" -dept "Dental" -a "01/10/23" -t "3:00 pm" -se True -ss False
