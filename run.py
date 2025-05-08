import gspread
from google.oauth2.service_account import Credentials

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

# Welcome message
def validate_questions():
    questions = [
        "What is your name?",
        "When did you have your surgery?",
        "Have you had any complications since your surgery?"
    ]

    print("Welcome to Rehab Metrics!\n")
    user_name = input("Please enter your name: ")
    print(f"\nHello, {user_name}!, please answer the questions, if you want to quit please enter 'quit'")


    for question in questions:
        while True:
            answer = input(question + " ")
            if answer.lower() == "quit":
                print("You chose to Quit and will return to the start")
                return
            elif not answer.strip():
                print("Please provide a valid answer.")
            else:
                print(f"Your answer: {answer}\n")
                break

validate_questions()