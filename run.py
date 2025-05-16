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
    print(
    "\nDISCLAIMER:\n"
    "This tool is for educational and self-tracking purposes only.\n"
    "It does not provide medical advice, diagnosis, or treatment.\n"
    "If you are experiencing complications or severe symptoms,\n"
    "please consult your healthcare professional.\n"
)
    print(DASH)
    while True:
        user_name = input("Please enter your username: ")
        user_name = user_name.strip()
        is_valid, error_message = validate_user(user_name)
        if is_valid:
            update_user_worksheet(user_name)
            print(f"\nHello, user {user_name}!, please answer the following questions so we can find out more about you")
            break
        else:
            print(error_message)


def validate_user(input_str):
    """
    This function validates the username and name inputs to ensure it is 2-10 characters long and does not allow special characters.
    """
    if len (input_str) < 2 or len(input_str) > 10:
        return False, "Username must be between 2 and 10 characters."
    for char in NOT_VALID:
        if char in input_str:
            return False, "Invalid name, please enter a username that does not contain special characters."
    return True, ""


def questions():
    responses = {}
    question_set = [
    (
        "What is your name?",
        validate_user,
        "Invalid name, please enter a name between 2-10 characters and not "
        "contain special characters."
    ),
    (
        "When did you have your surgery? (DD/MM/YYYY)",
        validate_date,
        "Date must be in DD/MM/YYYY format and must be a valid date."
    ),
    (
        "Have you had any complications since your surgery? (Yes/No)",
        validate_complications,
        "Please answer with 'Yes' or 'No'."
    ),
    (
        "On a scale of 0-10, what is your current pain level?\n"
        "0 = No pain, 10 = Worst imaginable pain",
        validate_pain_scale,
        "Please enter a number between 0 and 10."
    ),
    (
        "How far can you currently bend your knee?\n"
        "A: I struggle to bend it and have minimal movement\n"
        "B: I can bend it a little but my heel is still in front of my knee\n"
        "C: I can bend it so my heel is roughly in line with my knee\n"
        "D: I can bend it well as my heel goes behind my knee\n",
        validate_rom,
        "Please choose A, B, C or D."
    ),
    (
        "Are you currently able to put weight on your operated leg when standing or walking?\n"
        "A: I struggle to put any weight on my operated leg\n"
        "B: I can partially weight bear with a walking aid\n"
        "C: I can put most of my weight with a walking aid but still have a slight limp\n"
        "D: I can fully weight bear independently without any aids\n",
        validate_weight_bearing,
        "Please choose A, B, C or D."
    )
    ]
    
    for question, validator, error_message in question_set:
        while True:
            answer = input(question + " ").strip()
            if answer.lower() == "quit":
                print("You chose to Quit and will return to the start")
                return
            is_valid, validation_message = validator(answer)
            if is_valid:
                print(f"{validation_message}\n" if validation_message else f"Your answer: {answer}\n")
                responses[question] = answer
                break
            else:
                print(validation_message if validation_message else error_message)
    if answer.lower() in ("yes", "y", 'yep'):
        print("Please be aware that any serious complications should be addressed by a healthcare professional.")
    return responses

def calculate_days_since_surgery(date_str):
    try:
        surgery_date = datetime.strptime(date_str, "%d/%m/%Y")
        today = datetime.today()
        days_ago = (today - surgery_date).days
        return True, days_ago
    except ValueError:
        return False, 0


def validate_date(date_str):
    """
    This function validates the surgery date ensuring it:
    1. Is in DD/MM/YYYY format
    2. Is not in the future
    3. Is within the last 2 years
    """
    success, days_ago = calculate_days_since_surgery(date_str)
    if not success:
        return False, "Please enter your surgery date in DD/MM/YYYY format."
    if days_ago < 0:
        return False, "The surgery date cannot be in the future. Please check and try again."
    if days_ago > 730: 
        return False, "We recommend entering a surgery date within the last 2 years for more relevant tracking. If you had your surgery more than 2 years ago, you might want to consult with your healthcare provider for a current assessment."
    return True, f"Your surgery was on {date_str}, which was {days_ago} days ago."

def validate_complications(answer):
    """
    This function accepts only 'yes' or 'no' answers.
    """
    if answer.lower() in ("yes", "no", 'y', 'n', 'yep', 'nope'):
        return True, ""
    return False, ""

def validate_pain_scale(pain):
    try:
        num = int(pain)
        if 0 <= num <= 10:
            if num == 10:
                print("Your pain level is 10/10. That sounds very uncomfortable and would recommend consulting a healthcare professional for advice.")
                print("We recommend pausing the assessment for now. Take care.\n")
                exit()
            return True, f"Your pain level is {num}/10."
        else:
            return False, "Please enter a number between 0 and 10."
    except ValueError:
        return False, "Pain level must be a whole number"


def validate_rom(answer):
    """
    This function validates range of motion (ROM) input using multiple choice questions. 
    """
    rom_conversion = {
        "a": "Less than 45°",
        "b": "Less than 90°",
        "c": "Approximately 90°",
        "d": "Greater than 100°"
    }
    choice = answer.lower().strip()
    if choice in rom_conversion:
        return True, f"Knee bend: {rom_conversion[choice]}"
    return False, "Please choose A, B, C or D."


def validate_weight_bearing(answer):
    """
    This function validates the weight bearing status using multiple choice questions.
    """
    weight_conversion = {
        "a": "0-25% weight-bearing",
        "b": "50-75% weight-bearing",
        "c": "75%+ weight-bearing",
        "d": "100% weight-bearing"
    }
    selection = answer.lower().strip()
    if selection in weight_conversion:
        if selection == "a":
                print("This sounds very uncomfortable and would recommend consulting a healthcare professional for advice.")
                print("We recommend pausing the assessment for now. Take care.\n")
                exit()
        return True, f"Weight bearing status: {weight_conversion[selection]}"
    return False, "Please choose A, B, C or D."


def update_rehab_metrics_worksheet(data):
    """
    This function updates the worksheet.
    """
    try:
        metric_worksheet = SPREADSHEET.worksheet("userdata")
        headers = [
                "Name", "Surgery Date", "Days Since Surgery",
                "Complications", "Pain Level", "Range of motion",
                "Weight Bearing"
            ]
        metric_worksheet.append_row(headers)
        metric_worksheet.append_row(data)
        print("Updating your details...\n")
        print("Your details have been updated successfully!\n")
    except Exception as e:
        print(f"An error occurred while updating the worksheet: {e}")


def update_user_worksheet(username):
        try:
        user_worksheet = SPREADSHEET.worksheet("users")
        headers = ["Username", "Password"]
        user_worksheet.append_row(headers)
        user_worksheet.append_row([username, ""])  # Empty password field for now
        print("Username added successfully!\n")
    except Exception as e:
        print(f"An error occurred while updating the users worksheet: {e}")


def main():
    welcome_user()
    responses = questions()
    if responses:
        surgery_date_str = responses.get("When did you have your surgery? (DD/MM/YYYY)", "")
        surgery_date = datetime.strptime(surgery_date_str, "%d/%m/%Y").date()
        current_date = datetime.today().date()
        days_since_surgery = (current_date - surgery_date).days

        rom_question = "How far can you currently bend your knee?\nA: I struggle to bend it and have minimal movement\nB: I can bend it a little but my heel is still in front of my knee\nC: I can bend it so my heel is roughly in line with my knee\nD: I can bend it well as my heel goes behind my knee\n"
        wb_question = "Are you currently able to put weight on your operated leg when standing or walking?\nA: I struggle to put any weight on my operated leg\nB: I can partially weight bear with a walking aid\nC: I can put most of my weight with a walking aid but still have a slight limp\nD: I can fully weight bear independently without any aids\n"

        rom_valid, rom = validate_rom(responses[rom_question])
        wb_valid, wb = validate_weight_bearing(responses[wb_question])

        if rom_valid and wb_valid:
            data = [
                responses.get("What is your name?", ""),
                surgery_date_str,
                days_since_surgery,
                responses.get("Have you had any complications since your surgery? (Yes/No)", ""),
                responses.get("On a scale of 0-10, what is your current pain level?\n0 = No pain, 10 = Worst imaginable pain", ""),
                rom,
                wb
            ]
            update_rehab_metrics_worksheet(data)
        else:
            print("Error: Invalid responses for ROM or weight bearing. Please try again.")

main()
