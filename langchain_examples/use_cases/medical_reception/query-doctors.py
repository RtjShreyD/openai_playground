import sqlite3
from datetime import datetime

def time_to_minutes(time_str):
    # Function to convert time to minutes in 24-hour format
    time_obj = datetime.strptime(time_str, "%I:%M %p")
    return time_obj.hour * 60 + time_obj.minute

def query_doctors(department=None, availability_days=None, start_time=None, end_time=None):
    # Function to query doctors from SQLite database based on provided criteria
    conn = sqlite3.connect('doctors.db')
    cursor = conn.cursor()

    query = "SELECT * FROM doctors WHERE 1=1 "
    params = []

    if department:
        query += "AND department = ? "
        params.append(department)
    if availability_days:
        query += "AND availability_days LIKE ? "
        params.append('%' + availability_days + '%')
    if start_time:
        start_minutes = time_to_minutes(start_time)
        query += "AND availability_from >= ? "
        params.append(start_minutes)
    if end_time:
        end_minutes = time_to_minutes(end_time)
        query += "AND availability_to <= ? "
        params.append(end_minutes)

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()

    conn.close()
    return results

# Complex test cases
print("Doctors available in 'Cardiology' department on 'Monday' between 10:00 AM and 4:00 PM:")
print(query_doctors(department='Cardiology', availability_days='Monday', start_time='10:00 AM', end_time='4:00 PM'))

print("\nDoctors available in 'Dental' or 'Orthopedics' department on 'Tuesday' between 9:00 AM and 5:00 PM:")
print(query_doctors(department='Dental', availability_days='Tuesday', start_time='9:00 AM', end_time='5:00 PM') +
      query_doctors(department='Orthopedics', availability_days='Tuesday', start_time='9:00 AM', end_time='5:00 PM'))

print("\nDoctors available in 'Gynecology' department on any day between 9:00 AM and 4:00 PM:")
print(query_doctors(department='Gynecology', start_time='9:00 AM', end_time='4:00 PM'))
