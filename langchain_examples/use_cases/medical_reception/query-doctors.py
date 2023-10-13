import sqlite3

# Connect to the SQLite database (replace 'your_database_name.db' with your database file)
conn = sqlite3.connect('doctors.db')
cursor = conn.cursor()

def query_doctors(department=None, availability_days=None, start_time=None, end_time=None):
    query = "SELECT * FROM doctors WHERE 1=1 "
    params = []

    if department:
        query += "AND department = ? "
        params.append(department)
    if availability_days:
        query += "AND availability_days LIKE ? "
        params.append('%' + availability_days + '%')
    if start_time:
        query += "AND availability_from >= ? "
        params.append(start_time)
    if end_time:
        query += "AND availability_to <= ? "
        params.append(end_time)

    cursor.execute(query, tuple(params))
    return cursor.fetchall()


print("Doctors available in 'Cardiology' department:")
print(query_doctors(department='Cardiology'))

print("\nDoctors available on 'Monday':")
print(query_doctors(availability_days='Monday'))

print("\nDoctors available between 10:00 AM and 4:00 PM:")
print(query_doctors(start_time=600, end_time=960))

print("\nDoctors available in 'Dental' department on 'Tuesday':")
print(query_doctors(department='Dental', availability_days='Tuesday'))


# Complex test cases
print("Doctors available in 'Cardiology' department on 'Monday' between 10:00 AM and 4:00 PM:")
print(query_doctors(department='Cardiology', availability_days='Monday', start_time=600, end_time=960))

print("\nDoctors available in 'Dental' or 'Orthopedics' department on 'Tuesday' between 9:00 AM and 5:00 PM:")
print(query_doctors(department='Dental', availability_days='Tuesday', start_time=540, end_time=1020) +
      query_doctors(department='Orthopedics', availability_days='Tuesday', start_time=540, end_time=1020))

print("\nDoctors available in 'Gynecology' department on any day between 9:00 AM and 4:00 PM:")
print(query_doctors(department='Gynecology', start_time=540, end_time=960))

# Close the connection
conn.close()






# import sqlite3

# def find_doctor(department, **kwargs):
#     conn = sqlite3.connect('doctors.db')
#     cursor = conn.cursor()
    
#     query = "SELECT doctor_name, availability_days, availability_hours FROM doctors WHERE department=?"
#     values = (department,)

#     if 'date' in kwargs:
#         query += " AND ? IN (availability_days)"
#         values += (kwargs['date'],)

#     if 'time' in kwargs:
#         query += " AND ? BETWEEN SUBSTR(availability_hours, 1, 8) AND SUBSTR(availability_hours, -8)"
#         values += (kwargs['time'],)

#     cursor.execute(query, values)
#     doctors = cursor.fetchall()

#     conn.close()
#     return doctors

# # Example usage of the function
# # department = 'General Physician'
# # date = 'Monday'
# # time = '10:00 AM'

# # matching_doctors = find_doctor(department, date=date, time=time)

# # if matching_doctors:
# #     for doctor in matching_doctors:
# #         print(f"Doctor: {doctor[0]}")
# #         print(f"Available Days: {doctor[1]}")
# #         print(f"Available Hours: {doctor[2]}")
# #         print("--------")
# # else:
# #     print("No matching doctors found.")


# # Test Case 1: Find a General Physician available on Monday at 10:00 AM
# matching_doctors_1 = find_doctor('General Physician', date='Monday', time='10:00 AM')
# print("Test Case 1:")
# print(matching_doctors_1)
# print("--------")

# # Test Case 2: Find a Dermatologist available on Tuesday
# matching_doctors_2 = find_doctor('Dermatologist', date='Tuesday')
# print("Test Case 2:")
# print(matching_doctors_2)
# print("--------")

# # Test Case 3: Find an Orthopedic doctor available on Friday at 2:00 PM
# matching_doctors_3 = find_doctor('Orthopedics', date='Friday', time='2:00 PM')
# print("Test Case 3:")
# print(matching_doctors_3)
# print("--------")

# # Test Case 4: Find a Pediatrician available on Wednesday
# matching_doctors_4 = find_doctor('Pediatrics', date='Wednesday')
# print("Test Case 4:")
# print(matching_doctors_4)
# print("--------")

# # Test Case 5: Find a Gynecologist available on Thursday at 4:00 PM
# matching_doctors_5 = find_doctor('Gynecology', date='Thursday', time='4:00 PM')
# print("Test Case 5:")
# print(matching_doctors_5)
# print("--------")



