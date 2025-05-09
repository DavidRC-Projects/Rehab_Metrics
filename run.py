import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Required Google API scopes
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from the service account JSON key file
CREDS = Credentials.from_service_account_file("creds.json")

# Apply the necessary scopes to the credentials
SCOPED_CREDS = CREDS.with_scopes(SCOPE)

# Authorise gspread with the scoped credentials
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# Open the spreadsheet by name
SPREADSHEET = GSPREAD_CLIENT.open("rehab_metrics")

worksheet = SPREADSHEET.sheet1

SPACE = "\n"
DASH = "-" * 50
NOT_VALID = ('!', '?', '@', '*', '^', '.', '£', '$', '%', ',', '~', '`')

def welcome_user():
    """ 
    This function displays a welcome message and requests a username input.
    """
    print(DASH)
    print(SPACE)
    print("Welcome to Rehab Metrics!".center(50))
    print(SPACE)
    print(DASH)

    while True:
        user_name = input("Please enter your username: ")
        user_name = user_name.strip()
        is_valid, error_message = validate_user(user_name)
        if is_valid:
            print(f"\nHello, user {user_name}!, please answer the following questions so we can find out more about you")
            break
        else:
            print(error_message)

def validate_user(input_str):
    """
    This function validates the username and name inputs to ensure it is 2-10 characters long and does not allow special characters.
    """
    if len (input_str) <2 or len(input_str) > 10:
        return False, "Username must be between 2 and 10 characters."
    
    for char in NOT_VALID:
        if char in input_str:
            return False, "Invalid name, please enter a username that does not contain special characters."
    
    return True, ""

def questions():
    questions = [
        ("What is your name?", validate_user, "Invalid name, please enter a name between 2-10 characters and not contain special characters."),
        ("When did you have your surgery? (DD/MM/YYYY)", validate_date, "Date must be in DD/MM/YYYY format."),
        ("Have you had any complications since your surgery? (Yes/No)", validate_complications, "Please answer with 'Yes' or 'No'."),
        ("On a scale from 0 to 10, how would you rate your current pain?", validate_pain_scale, "Pain level must be between 0 and 10.")
    ]
    
    for question, validator, error_message in questions:
        while True:
            answer = input(question + " ").strip()
            if answer.lower() == "quit":
                print("You chose to Quit and will return to the start")
                return
            is_valid, validation_message = validator(answer)
            if is_valid:
                print(f"{validation_message}\n" if validation_message else f"Your answer: {answer}\n")
                break
            else:
                print(validation_message if validation_message else error_message)
            
def validate_date(date_str):
    """
    This function validates date in DD-MM-YYYY format and prints how many days since the surgery.
    """
    try:
        surgery_date = datetime.strptime(date_str, "%d/%m/%Y")
        today = datetime.today()
        days_ago = (today - surgery_date).days

        if days_ago < 0:
            return False, "The surgery date can't be in the future. Please check and try again."
        datetime.strptime(date_str, "%d/%m/%Y")
        
        return True, f"Your surgery was on {date_str}, which was {days_ago} days ago."
    except ValueError:
        return False, ""

def validate_complications(answer):
    """
    This function accepts only 'yes' or 'no' answers.
    """
    if answer.lower() in ("yes", "no"):
        return True, ""
    return False, ""

def validate_pain_scale(pain):
    try:
        num = int(pain)
        if 0 <= num <= 10:
            if num == 10:
                print("Your pain level is 10/10. That sounds very uncomfortable and would recommend consulting a healthcare professional for advice")
                print("We recommend pausing the assessment for now. Take care.\n")
                exit()
            return True, f"Your pain level is {num}/10."
        else:
            return False, "Please enter a number between 0 and 10."
    except ValueError:
        return False, "Pain level must be a whole number"
        
def main():
    welcome_user()
    questions()

main()