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
        if validate_username(user_name):
            print(f"\nHello, user {user_name}!, please answer the following questions so we can find out more about you")
            break
        else:
            print("Invalid username, please enter a username between 2-10 characters and not contain special characters.")

def validate_username(user_name):
    """
    This function validates the username to ensure it is 2-10 characters long and does not allow special characters.
    """
    if len (user_name) <2 or len(user_name) > 10:
        return False
    
    for char in NOT_VALID:
        if char in user_name:
            return False
    return True

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