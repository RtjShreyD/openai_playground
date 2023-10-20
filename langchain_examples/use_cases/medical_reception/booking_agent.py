from datetime import datetime, timedelta
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
import json
import random

import os
import re
from dotenv import load_dotenv
import redis

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

llm = ChatOpenAI(model_name="gpt-4", temperature=0, verbose=True)

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def book_appointment(input_string):
    try:
        pattern = r"session_id=(\d+) doctor_name=(.*?) appointment_time=(\d{2}:\d{2}) appointment_day=(\w+)"
        match = re.search(pattern, input_string)
        
        if match:
            session_id = match.group(1)
            doctor_name = match.group(2)
            appointment_time = match.group(3)
            appointment_day = match.group(4)
        else:
            raise ValueError("Invalid input format")
        
        # Validate session_id, doctor_name, and appointment_time
        if not session_id or not doctor_name or not appointment_time:
            raise ValueError("Invalid session_id, doctor_name, or appointment_time")
        
        # Deduce appointment_day and appointment_date
        if not appointment_day:
            today = datetime.now().date()
            appointment_day = today.strftime("%A")
        
        # Calculate the appointment_date based on today's date and the appointment_day
        days_ahead = (datetime.strptime(appointment_day, "%A").weekday() - datetime.now().weekday()) % 7
        appointment_date = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        
        # Generate a random 4-digit number for booking ID
        booking_id = random.randint(1000, 9999)
        
        # Store appointment information in Redis
        appointment_info = {
            "session_id": session_id,
            "doctor_name": doctor_name,
            "appointment_time": appointment_time,
            "appointment_date": appointment_date,
            "booking_no": booking_id
        }
        redis_key = f"{session_id}_booking_info"
        json_data = json.dumps(appointment_info)
        redis_client.set(redis_key, json_data)
        
        return f"Appointment scheduled, booking_id is {booking_id}, date is {appointment_date}, time is {appointment_time}"
    
    except ValueError as e:
        return str(e) + ", please confirm the details from the user and try again later"
    
    except Exception as e:
        return "Some error occurred, please try again later"


book_appointment_tool = Tool(
    name="book_appointment",
    func=book_appointment,
    description="Takes an input string containing session_id, doctor_name, appointment_time, appointment_day and returns booking_id, appointment_time, appointment_day, appointment_date contained in a string"
)

agent = initialize_agent([book_appointment_tool], llm, verbose=True)

test_cases = [
    "book_appointment session_id=1234 doctor_name=Dr. Smith appointment_time=12:00 appointment_day=Monday",
    "book_appointment session_id=5678 doctor_name=Dr. Johnson appointment_time=14:30 appointment_day=Wednesday",
    "book_appointment session_id=9876 doctor_name=Dr. Brown appointment_time=10:00",
    "book_appointment session_id=1357 doctor_name=Dr. White appointment_time=5:00PM appointment_day=Friday",
    "book_appointment session_id=2468 doctor_name=Dr. Lee appointment_time=11:45 appointment_day=Saturday",
    "book_appointment session_id=8642 doctor_name=Dr. Davis appointment_time=15:20 appointment_day=Thursday"
]

for input_data in test_cases:
    output_data = agent.invoke({"input": input_data})
    print(output_data)
    print("\n================================")