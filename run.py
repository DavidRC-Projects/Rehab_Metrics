import gspread
from google.oauth2.service_account import Credentials
import re

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

def welcome_user():
    """ 
    This function displays a welcome message and requests a username.
    """
    print(DASH)
    print(SPACE)
    print("Welcome to Rehab Metrics!".center(50))
    print(SPACE)
    print(DASH)

    user_name = input("Please enter your username: ")
    print(f"\nHello, user {user_name}!, please answer the questions, if you want to quit at any time please enter 'quit'")

def validate_questions():
    questions = [
        "What is your name?",
        "When did you have your surgery? (DD--MM--YYYY)",
        "Have you had any complications since your surgery? (Yes/No)"
    ]
    
    for question in questions:
        while True:
            answer = input(question + " ")
            if answer.lower() == "quit":
                print("You chose to Quit and will return to the start")
                return
            if len(answer) < 2 or len(answer) > 10:
                print("Name must be atleast 2-10 characters.")
            if not str(answer):
                print("Name must be characters.")
            elif not answer.strip():
                print("Please provide a valid answer.")
            else:
                print(f"Your answer: {answer}\n")
                break

def main():
    welcome_user()
    validate_questions()

main()