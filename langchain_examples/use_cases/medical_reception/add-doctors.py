import sqlite3

# Connect to SQLite database (or create it if not exists)
conn = sqlite3.connect('doctors.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create doctors table
cursor.execute('''
    CREATE TABLE doctors (
        doctor_id INTEGER PRIMARY KEY,
        doctor_name TEXT,
        department TEXT,
        availability_days TEXT,
        availability_from INT,
        availability_to INT
    )
''')

# Sample data for doctors
doctors_data = [
    (1, 'Dr. Ananya Sharma', 'General Physician', 'Monday, Wednesday, Friday', 540, 1080),
    (2, 'Dr. Rahul Gupta', 'Dental', 'Tuesday, Thursday, Saturday', 480, 960),
    (3, 'Dr. Priya Kapoor', 'Pediatrics', 'Monday, Thursday, Saturday', 600, 1080),
    (4, 'Dr. Sanjay Verma', 'Orthopedics', 'Tuesday, Friday', 540, 1020),
    (5, 'Dr. Nisha Singh', 'ENT', 'Wednesday, Saturday', 780, 1140),
    (6, 'Dr. Vikram Sharma', 'Cardiology', 'Monday, Thursday', 600, 960),
    (7, 'Dr. Meera Reddy', 'Gynecology', 'Tuesday, Friday', 540, 1020),
    (8, 'Dr. Karan Kapoor', 'Neurology', 'Wednesday, Saturday', 660, 1140),
    (9, 'Dr. Anjali Singhania', 'Dermatologist', 'Monday, Thursday, Saturday', 840, 1200),
    (10, 'Dr. Arjun Mehra', 'Ophthalmology', 'Tuesday, Friday', 600, 1020),
    (11, 'Dr. Priyanka Chopra', 'Psychiatry', 'Wednesday, Saturday', 540, 960),
    (12, 'Dr. Vikas Khanna', 'Urology', 'Monday, Thursday', 660, 1080),
    (13, 'Dr. Ayesha Ahmed', 'Endocrinology', 'Tuesday, Friday', 600, 960),
    (14, 'Dr. Sameer Khan', 'Nephrology', 'Wednesday, Saturday', 540, 1020),
    (15, 'Dr. Anjali Verma', 'Pulmonology', 'Monday, Thursday', 480, 900),
    (16, 'Dr. Rohit Kapoor', 'Gastroenterology', 'Tuesday, Friday', 600, 1080),
    (17, 'Dr. Natasha Singh', 'Rheumatology', 'Wednesday, Saturday', 540, 1020),
    (18, 'Dr. Rahul Sharma', 'Plastic Surgery', 'Monday, Thursday', 780, 1140),
    (19, 'Dr. Pooja Mehra', 'Hematology', 'Tuesday, Friday', 600, 1020),
    (20, 'Dr. Raj Verma', 'Neurosurgery', 'Wednesday, Saturday', 540, 960),
    (21, 'Dr. Anushka Singh', 'Infectious Diseases', 'Monday, Thursday', 600, 1080),
    (22, 'Dr. Karan Kapoor', 'Allergy and Immunology', 'Tuesday, Friday', 840, 1200),
    (23, 'Dr. Anjali Chopra', 'Pediatric Surgery', 'Wednesday, Saturday', 540, 960),
    (24, 'Dr. Vikram Khanna', 'Cardiac Surgery', 'Monday, Thursday', 600, 1080),
    (25, 'Dr. Aisha Ahmed', 'Physical Medicine and Rehabilitation', 'Tuesday, Friday', 540, 960),
    (26, 'Dr. Deepak Kumar', 'General Physician', 'Monday, Tuesday, Thursday', 480, 960),
    (27, 'Dr. Reena Singh', 'Internal Medicine', 'Wednesday, Friday, Saturday', 540, 1020),
    (28, 'Dr. Anil Kapoor', 'Family Medicine', 'Monday, Wednesday, Saturday', 600, 1080),
    (29, 'Dr. Reena Singh', 'Internal Medicine', 'Monday, Wednesday, Saturday', 540, 1020),
    (30, 'Dr. Anil Kapoor', 'Family Medicine', 'Tuesday, Thursday, Saturday', 600, 1080),
    (31, 'Dr. Sunil Sharma', 'Gastroenterology', 'Monday, Wednesday, Friday', 600, 1080),
    (32, 'Dr. Radha Patel', 'Pulmonology', 'Tuesday, Thursday, Saturday', 540, 1020),
    (33, 'Dr. Manish Verma', 'Oncology', 'Monday, Wednesday, Friday', 540, 1020),
    (34, 'Dr. Sheetal Gupta', 'Rheumatology', 'Tuesday, Thursday, Saturday', 600, 1080),
    (35, 'Dr. Ajay Mehra', 'Radiology', 'Monday, Wednesday, Friday', 540, 1020),
    (36, 'Dr. Deepika Singh', 'Dermatologist', 'Tuesday, Thursday, Saturday', 840, 1200),
    (37, 'Dr. Vikrant Khanna', 'Neurology', 'Monday, Wednesday, Friday', 600, 1080),
    (38, 'Dr. Neha Sharma', 'Endocrinology', 'Tuesday, Thursday, Saturday', 540, 1020),
    (39, 'Dr. Anurag Patel', 'Nephrology', 'Monday, Wednesday, Friday', 600, 1080),
    (40, 'Dr. Priya Mehra', 'Gynecology', 'Tuesday, Thursday, Saturday', 540, 1020),
    (41, 'Dr. Karan Verma', 'Orthopedics', 'Monday, Wednesday, Friday', 600, 1080),
    (42, 'Dr. Anjali Kapoor', 'ENT', 'Tuesday, Thursday, Saturday', 540, 1020),
    (43, 'Dr. Rajeev Singh', 'Cardiology', 'Monday, Wednesday, Friday', 600, 1080),
    (44, 'Dr. Deepa Sharma', 'Pediatrics', 'Tuesday, Thursday, Saturday', 540, 1020),
    (45, 'Dr. Amit Mehra', 'Psychiatry', 'Monday, Wednesday, Friday', 600, 1080),
    (46, 'Dr. Anjali Singhania', 'Urology', 'Tuesday, Thursday, Saturday', 540, 1020),
    (47, 'Dr. Sameer Khan', 'Dental', 'Monday, Wednesday, Friday', 600, 1080),
    (48, 'Dr. Anushka Sharma', 'Gastroenterology', 'Tuesday, Thursday, Saturday', 540, 1020),
    (49, 'Dr. Varun Kapoor', 'Oncology', 'Monday, Wednesday, Friday', 600, 1080),
    (50, 'Dr. Priyanka Verma', 'Rheumatology', 'Tuesday, Thursday, Saturday', 540, 1020),
    (51, 'Dr. Rohit Sharma', 'Radiology', 'Monday, Wednesday, Friday', 600, 1080),
]


# Insert data into the doctors table
cursor.executemany('INSERT INTO doctors VALUES (?, ?, ?, ?, ?, ?)', doctors_data)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Doctors' data has been successfully inserted into the database.")
