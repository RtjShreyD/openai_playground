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

def parse_time(appointment_time):
    # Regular expression to match various time formats
    time_pattern = r"(\d{1,2}):(\d{2})(AM|PM)?"
    match = re.match(time_pattern, appointment_time, re.IGNORECASE)
    
    if match:
        hours, minutes, period = match.groups()
        hours = int(hours)
        minutes = int(minutes)
        
        if period and period.lower() == 'pm' and hours != 12:
            hours += 12
        elif period and period.lower() == 'am' and hours == 12:
            hours = 0
        
        return f"{hours:02d}:{minutes:02d}"
    else:
        raise ValueError("Invalid appointment_time format")


def book_appointment(input_string):
    try:
        pattern = r"session_id=(\d+) doctor_name=(.*?) appointment_time=(.*?) appointment_day=(\w+)"
        match = re.search(pattern, input_string)
        
        if match:
            session_id = match.group(1)
            doctor_name = match.group(2)
            appointment_time = parse_time(match.group(3))
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


'''

OUTPUT_LOG - 

> Entering new AgentExecutor chain...
The user wants to book an appointment with Dr. Smith at 12:00 on Monday. I need to use the book_appointment tool to fulfill this request.
Action: book_appointment
Action Input: session_id=1234 doctor_name=Dr. Smith appointment_time=12:00 appointment_day=Monday
Observation: Appointment scheduled, booking_id is 3102, date is 2023-10-23, time is 12:00
Thought:The appointment has been successfully booked with Dr. Smith at 12:00 on Monday. The booking_id is 3102 and the date of the appointment is 2023-10-23.
Final Answer: Your appointment with Dr. Smith has been booked for 12:00 on Monday, 2023-10-23. Your booking ID is 3102.

> Finished chain.
{'input': 'book_appointment session_id=1234 doctor_name=Dr. Smith appointment_time=12:00 appointment_day=Monday', 'output': 'Your appointment with Dr. Smith has been booked for 12:00 on Monday, 2023-10-23. Your booking ID is 3102.'}

================================


> Entering new AgentExecutor chain...
The user wants to book an appointment with Dr. Johnson at 14:30 on Wednesday. I need to use the book_appointment tool to fulfill this request.
Action: book_appointment
Action Input: session_id=5678 doctor_name=Dr. Johnson appointment_time=14:30 appointment_day=Wednesday
Observation: Appointment scheduled, booking_id is 7294, date is 2023-10-23, time is 14:30
Thought:The appointment has been successfully booked with Dr. Johnson at 14:30 on Wednesday, 23rd October 2023. The booking ID for this appointment is 7294.
Final Answer: Your appointment with Dr. Johnson has been booked for 14:30 on Wednesday, 23rd October 2023. Your booking ID is 7294.

> Finished chain.
{'input': 'book_appointment session_id=5678 doctor_name=Dr. Johnson appointment_time=14:30 appointment_day=Wednesday', 'output': 'Your appointment with Dr. Johnson has been booked for 14:30 on Wednesday, 23rd October 2023. Your booking ID is 7294.'}

================================


> Entering new AgentExecutor chain...
The user wants to book an appointment with Dr. Brown at 10:00. I need to use the book_appointment tool to fulfill this request.
Action: book_appointment
Action Input: session_id=9876 doctor_name=Dr. Brown appointment_time=10:00
Observation: Invalid input format, please confirm the details from the user and try again later
Thought:The booking tool didn't accept the input. It seems I need to provide the appointment_day as well.
Final Answer: I'm sorry, but I need to know the day of your appointment as well. Could you please provide that?

> Finished chain.
{'input': 'book_appointment session_id=9876 doctor_name=Dr. Brown appointment_time=10:00', 'output': "I'm sorry, but I need to know the day of your appointment as well. Could you please provide that?"}

================================


> Entering new AgentExecutor chain...
The user wants to book an appointment with Dr. White at 5:00PM on Friday. I need to use the book_appointment tool to fulfill this request.
Action: book_appointment
Action Input: session_id=1357 doctor_name=Dr. White appointment_time=5:00PM appointment_day=Friday
Observation: Appointment scheduled, booking_id is 8471, date is 2023-10-23, time is 17:00
Thought:The appointment has been successfully booked. The booking_id is 8471, the appointment date is 2023-10-23 and the time is 17:00.
Final Answer: Your appointment with Dr. White has been booked for 5:00PM on Friday, 2023-10-23. Your booking ID is 8471.

> Finished chain.
{'input': 'book_appointment session_id=1357 doctor_name=Dr. White appointment_time=5:00PM appointment_day=Friday', 'output': 'Your appointment with Dr. White has been booked for 5:00PM on Friday, 2023-10-23. Your booking ID is 8471.'}

================================


> Entering new AgentExecutor chain...
The user wants to book an appointment with Dr. Lee at 11:45 on Saturday. I need to use the book_appointment tool to fulfill this request.
Action: book_appointment
Action Input: session_id=2468 doctor_name=Dr. Lee appointment_time=11:45 appointment_day=Saturday
Observation: Appointment scheduled, booking_id is 9034, date is 2023-10-23, time is 11:45
Thought:The appointment has been successfully booked with Dr. Lee at 11:45 on Saturday, 23rd October 2023. The booking ID for this appointment is 9034.
Final Answer: Your appointment with Dr. Lee has been booked for 11:45 on Saturday, 23rd October 2023. Your booking ID is 9034.

> Finished chain.
{'input': 'book_appointment session_id=2468 doctor_name=Dr. Lee appointment_time=11:45 appointment_day=Saturday', 'output': 'Your appointment with Dr. Lee has been booked for 11:45 on Saturday, 23rd October 2023. Your booking ID is 9034.'}

================================


> Entering new AgentExecutor chain...
The user wants to book an appointment with Dr. Davis at 15:20 on Thursday. I need to use the book_appointment tool to fulfill this request.
Action: book_appointment
Action Input: session_id=8642 doctor_name=Dr. Davis appointment_time=15:20 appointment_day=Thursday
Observation: Appointment scheduled, booking_id is 6234, date is 2023-10-23, time is 15:20
Thought:The appointment has been successfully booked. The booking_id is 6234, the date is 2023-10-23 and the time is 15:20.
Final Answer: Your appointment with Dr. Davis has been booked for 15:20 on 2023-10-23 (Thursday). Your booking ID is 6234.

> Finished chain.
{'input': 'book_appointment session_id=8642 doctor_name=Dr. Davis appointment_time=15:20 appointment_day=Thursday', 'output': 'Your appointment with Dr. Davis has been booked for 15:20 on 2023-10-23 (Thursday). Your booking ID is 6234.'}

'''