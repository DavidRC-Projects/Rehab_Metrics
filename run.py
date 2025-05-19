import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from guide import get_rom_timeline_assessment, get_pain_timeline_assessment, get_weight_bearing_timeline_assessment

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
NOT_VALID = (
    '!', '?', '@', '*', '^', '.', '£', '$', '%', ',', '~', '`',
    '+', '=', '<', '>', '|', '\\', '/', '[', ']', '{', '}', '#'
)


def welcome_user():
    """
    This function displays a welcome message and requests a username input.
    """
    print(DASH)
    print(SPACE)
    print("Welcome, new user!".center(50))
    print("This tool has been developed to help you track".center(50))
    print("your recovery after a knee replacement.".center(50))
    print("".center(50))
    print("Please enter a username to begin your journey.".center(50))
    print("You'll be guided through a few short questions.".center(50))
    print("Each answer will be saved to help monitor your progress.".center(50))
    print("You can type 'quit' at any time to exit the program.".center(50))
    print("To review your recovery progress in the future,".center(50))
    print("you can log in using your username and password.".center(50))
    print("".center(50))
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
        if user_quit(user_name):
            return None
        is_valid, error_message = validate_user(user_name)
        if not is_valid:
            print(error_message)
            continue
            
        if check_existing_username(user_name):
            print("This username already exists. Please choose another.")
            continue
            
        password = user_password()
        if password == "quit":
            return None
        update_user_worksheet(user_name, password)
        print(f"\nHello, {user_name}! Please answer the following questions "
              f"so we can find out more about your recovery.")
        break


def validate_user(input_str):
    """
    Validates username and name inputs:
    - Must be 2-10 characters long
    - Must not contain special characters
    """
    if len (input_str) < 2 or len(input_str) > 10:
        return False, "Username must be between 2 and 10 characters."
    for char in NOT_VALID:
        if char in input_str:
            return False, "Invalid name. Please avoid special characters."
    return True, ""


def user_password():
    """
    This function handles password input and validation.
    """
    while True:
        password = input("Please enter a password (minimum 6 characters): ")
        if user_quit(password):
            return "quit"
        is_valid_pass, pass_error = validate_password(password)
        if is_valid_pass:
            return password
        else:
            print(pass_error)


def validate_password(password):
    """
    This function validates the password to ensure it is at least 6 characters long.
    This will also check for white spaces
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if ' ' in password:
        return False, "Password cannot contain spaces."
    return True, ""


def questions():
    responses = {}
    surgery_info = {'days': None}
    question_set = [
    (
        "What is your name?",
        validate_user,
        "Invalid name, please enter a name between 2-10 characters."
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
        "B: I can bend it a little but my heel is in front\n"
        "C: I can bend it so my heel is roughly in line\n"
        "D: I can bend it well as my heel goes behind\n",
        lambda x: validate_rom(x, surgery_info['days']),
        "Please choose A, B, C or D."
    ),
    (
        "Weight bearing on operated leg?\n"
        "A: I struggle to put any weight\n"
        "B: I can partially weight bear with aid\n"
        "C: Most weight with aid but have limp\n"
        "D: Full weight bearing without aids\n",
        validate_weight_bearing,
        "Please choose A, B, C or D."
    )
    ]
    
    for question, validator, error_message in question_set:
        while True:
            answer = input(question + " ").strip()
            if user_quit(answer):
                return None
            is_valid, validation_message = validator(answer)
            if is_valid:
                msg = validation_message if validation_message else f"Your answer: {answer}"
                print(f"{msg}\n")
                responses[question] = answer
                
                # Update days_since_surgery after getting the surgery date
                if "surgery?" in question:
                    success, days = calculate_days_since_surgery(answer)
                    if success:
                        surgery_info['days'] = days
                break
            else:
                msg = validation_message if validation_message else error_message
                print(msg)
    if answer.lower() in ("yes", "y", 'yep'):
        print("Please consult a healthcare professional about your complications.")
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
        return False, ("Surgery date should be within 2 years for tracking. "
                      "Please consult your healthcare provider.")
    return True, f"Surgery was {days_ago} days ago on {date_str}."


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


def validate_rom(answer, days_since_surgery=None):
    """
    This function validates range of motion (ROM) input using multiple choice questions
    and provides basic assessment.
    """
    rom_conversion = {
        "a": "Less than 45°",
        "b": "Less than 90°",
        "c": "Approximately 90°",
        "d": "Greater than 100°"
    }
    
    rom_degrees = {
        "a": 45,    # "Less than 45°"
        "b": 90,    # "Less than 90°"
        "c": 90,    # "Approximately 90°"
        "d": 100    # "Greater than 100°"
    }
    
    choice = answer.lower().strip()
    if choice in rom_conversion:
        base_message = f"Knee bend: {rom_conversion[choice]}"
        if days_since_surgery is not None:
            assessment = get_rom_timeline_assessment(rom_degrees, choice, days_since_surgery)
            base_message += f"\n{assessment}"
        return True, base_message
    return False, "Please choose A, B, C or D."


def validate_weight_bearing(answer):
    """
    This function validates the weight bearing status using multiple choice questions.
    """
    if answer is None:
        return False, "Please choose A, B, C or D."
        
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


def assess_rom_progress(metric_data):
    """
    Assesses user's Range of Motion (ROM) progress using their metric data.
    """
    try:
        if not metric_data[3]:
            print("\nCannot perform ROM assessment: Days since surgery not available")
            return False
            
        days_since_surgery = int(metric_data[3])
        rom_data = metric_data[6].split('\n')[0]
        
        # Parse the ROM choice from the data
        rom_choice = None
        if "Less than 45°" in rom_data:
            rom_choice = "a"
        elif "Less than 90°" in rom_data:
            rom_choice = "b"
        elif "Approximately 90°" in rom_data:
            rom_choice = "c"
        elif "Greater than 100°" in rom_data:
            rom_choice = "d"
            
        # ROM degrees mapping for assessment
        rom_degrees = {
            "a": 45,    
            "b": 90,    
            "c": 90,    
            "d": 100    
        }
        
        if rom_choice:
            assessment = get_rom_timeline_assessment(rom_degrees, rom_choice, days_since_surgery)
            print("\nROM Assessment:")
            print("-" * 50)
            print(assessment)
            print("-" * 50)
            return True
    except Exception as e:
        print(f"Error performing ROM assessment: {e}")
        return False


def assess_pain_progress(metric_data):
    """
    Assesses user's pain level progress using their metric data.
    """
    try:
        if not metric_data[3]:
            print("\nCannot perform pain assessment: Days since surgery not available")
            return False
            
        days_since_surgery = int(metric_data[3])
        
        pain_level = metric_data[5]
        if not pain_level:
            print("\nCannot perform pain assessment: Pain level data not available")
            return False
            
        # Get and display assessment
        assessment = get_pain_timeline_assessment(pain_level, days_since_surgery)
        print("\nPain Level Assessment:")
        print("-" * 50)
        print(assessment)
        print("-" * 50)
        return True
        
    except Exception as e:
        print(f"Error performing pain assessment: {e}")
        return False
    

def assess_weight_bearing_progress(metric_data):
    """
    Assesses user's weight bearing progress using their metric data.
    """
    try:
        if not metric_data[3]:
            print("\nCannot perform weight bearing assessment: Days since surgery not available")
            return False
        
        days_since_surgery = int(metric_data[3])
        wb_status = metric_data[7]
        if not wb_status:
            print("\nCannot perform weight bearing assessment: Weight bearing status not available")
            return False
        
        assessment = get_weight_bearing_timeline_assessment(wb_status, days_since_surgery)
        print("\nWeight Bearing Assessment:")
        print("-" * 50)
        print(assessment)
        print("-" * 50)
        return True
    
    except Exception as e:
        print(f"Error performing weight bearing assessment: {e}")
        return False


def update_rehab_metrics_worksheet(data):
    """
    This function updates the worksheet with user data.
    """
    try:
        metric_worksheet = SPREADSHEET.worksheet("userdata")
        if not metric_worksheet.get_all_values():
            headers = [
                    "Username", "Name", "Surgery Date", "Days Since Surgery",
                    "Complications", "Pain Level", "Range of motion",
                    "Weight Bearing"
                ]
            metric_worksheet.append_row(headers)
        
        metric_worksheet.append_row(data)
        print("Updating your details...\n")
        print("Your details have been updated successfully!\n")
    except Exception as e:
        print(f"An error occurred while updating the worksheet: {e}")


def update_user_worksheet(username, password):
    try:
        user_worksheet = SPREADSHEET.worksheet("users")
        if not user_worksheet.row_values(1):
            headers = ["Username", "Password"]
            user_worksheet.append_row(headers)
        user_worksheet.append_row([username, password])
        print("Username and password added successfully!\n")
    except Exception as e:
        print(f"An error occurred while updating the users worksheet: {e}")


def check_user_status():
    """
    This function asks if the user is new or returning.
    """
    print(DASH)
    print(SPACE)
    print("Welcome to Rehab Metrics!".center(50))
    print(SPACE)
    print(DASH)
    print("\nAre you a new user?")
    status = input("Please enter (Y) for Yes or (N) for No: ")
    return status.lower() == 'y'


def check_existing_username(username):
    """
    Check if a username already exists in the users worksheet.
    Returns True if username exists, False otherwise.
    """
    try:
        user_worksheet = SPREADSHEET.worksheet("users")
        usernames = user_worksheet.col_values(1)[1:]
        return username in usernames
    except Exception as e:
        print(f"Error checking username: {e}")
        return False


def get_user_data(username):
    """
    Retrieve and display user data from both users and userdata worksheets.
    """
    try:
        # Get user data from users worksheet
        user_worksheet = SPREADSHEET.worksheet("users")
        usernames = user_worksheet.col_values(1)
        
        if len(usernames) <= 1:
            print("No user data found in the system.")
            return False
            
        # Find the row index for the username (case-sensitive match)
        username_row = None
        for idx, name in enumerate(usernames[1:], start=2):
            if name == username:
                username_row = idx
                break
                
        if username_row is None:
            print(f"Username '{username}' not found.")
            return False
            
        user_data = user_worksheet.row_values(username_row)
        
        # Get user metrics from userdata worksheet
        metric_worksheet = SPREADSHEET.worksheet("userdata")
        all_metric_data = metric_worksheet.get_all_values()
        
        # Find user entries by matching username in first column
        user_entries = [row for row in all_metric_data[1:] if row and row[0] == username]
        
        if not user_entries:
            print("No rehabilitation data found for this user.")
            return False
            
        # Use the most recent entry (last in the list)
        metric_data = user_entries[-1]

        # Display user data for existing users
        print("\nYour Profile and Rehabilitation Data:")
        print("-" * 50)
        print(f"Username: {metric_data[0]}")
        print(f"Name: {metric_data[1]}")
        print(f"Surgery Date: {metric_data[2]}")
        print(f"Days Since Surgery: {metric_data[3]}")
        print(f"Complications Reported: {metric_data[4]}")
        if not "Knee bend:" in metric_data[5]:
            print(f"Pain Level (0-10): {metric_data[5]}")
        if "Knee bend:" in metric_data[5]: 
            rom_value = metric_data[5].split('\n')[0].replace("Knee bend: ", "")
            wb_value = metric_data[6].replace("Weight bearing status: ", "")
            print(f"Knee Range of Motion: {rom_value}")
            print(f"Weight Bearing Status: {wb_value}")
        else:
            rom_value = metric_data[6].split('\n')[0].replace("Knee bend: ", "")
            wb_value = metric_data[7].replace("Weight bearing status: ", "")
            print(f"Knee Range of Motion: {rom_value}")
            print(f"Weight Bearing Status: {wb_value}")
        print("-" * 50)
        
        # Add assessment after displaying user data
        assess_rom_progress(metric_data)
        assess_pain_progress(metric_data)
        assess_weight_bearing_progress(metric_data)
        return True
    except Exception as e:
        print(f"Error retrieving user data: {e}")
        return False


def verify_password(username, password):
    """
    Verify the password for a given username.
    """
    user_worksheet = SPREADSHEET.worksheet("users")
    usernames = user_worksheet.col_values(1)
    
    if username not in usernames:
        return False
        
    row_idx = usernames.index(username) + 1
    stored_password = user_worksheet.cell(row_idx, 2).value
    
    return password == stored_password


def handle_returning_user():
    """
    Handle the login process for returning users.
    """
    print("\nWelcome back! Please login to view your data.")
    while True:
        username = input("\nPlease enter your username: ").strip()
        if user_quit(username):
            return
        password = input("Please enter your password: ").strip()
        if user_quit(password):
            return
        if verify_password(username, password):
            if get_user_data(username):
                break
        else:
            print("\nIncorrect username or password.")
        retry = input("\nWould you like to try again? (Y/N): ").lower()
        if retry != 'y':
            break


def user_quit(input_str):
    """
    Checks if the user wants to quit the program.
    Returns True if user wants to quit, False otherwise.
    """
    if input_str.lower() == "quit":
        print("You chose to Quit and will return to the start")
        return True
    return False

def main():
    is_new_user = check_user_status()
    if is_new_user:
        result = welcome_user()
        if result is None:
            return
        responses = questions()
        if responses is None: 
            return
        if responses: 
            surgery_date_str = responses.get(
                "When did you have your surgery? (DD/MM/YYYY)", ""
            )
            surgery_date = datetime.strptime(surgery_date_str, "%d/%m/%Y").date()
            current_date = datetime.today().date()
            days_since_surgery = (current_date - surgery_date).days

            rom_q = ("How far can you currently bend your knee?\n"
                    "A: I struggle to bend it and have minimal movement\n"
                    "B: I can bend it a little but my heel is in front\n"
                    "C: I can bend it so my heel is roughly in line\n"
                    "D: I can bend it well as my heel goes behind\n")
                    
            wb_q = ("Weight bearing on operated leg?\n"
                   "A: I struggle to put any weight\n"
                   "B: I can partially weight bear with aid\n"
                   "C: Most weight with aid but have limp\n"
                   "D: Full weight bearing without aids\n")

            rom_valid, rom = validate_rom(responses[rom_q], days_since_surgery)
            wb_valid, wb = validate_weight_bearing(responses[wb_q])

            if rom_valid and wb_valid:
                username = None
                user_worksheet = SPREADSHEET.worksheet("users")
                usernames = user_worksheet.col_values(1)
                if len(usernames) > 1:
                    username = usernames[-1]
                
                if username:
                    complications_q = "Have you had any complications since your surgery? (Yes/No)"
                    pain_q = "On a scale of 0-10, what is your current pain level?\n0 = No pain, 10 = Worst imaginable pain"
                    
                    data = [
                        username,
                        responses.get("What is your name?", ""),
                        surgery_date_str,
                        days_since_surgery,
                        responses.get(complications_q, ""),
                        responses.get(pain_q, ""),
                        rom,
                        wb
                    ]
                    assess_rom_progress(data)
                    assess_pain_progress(data)
                    assess_weight_bearing_progress(data)
                    update_rehab_metrics_worksheet(data)
                else:
                    print("Error: Could not retrieve username. Please try again.")
            else:
                print("Error: Invalid ROM or weight bearing responses. Try again.")
    else:
        handle_returning_user()

main()
