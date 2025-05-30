import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from guide import (
    get_rom_timeline_assessment,
    get_pain_timeline_assessment,
    get_weight_bearing_timeline_assessment
)
from colorama import Fore, Style

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

# Worksheet names
WORKSHEET_USERS = "users"
WORKSHEET_USERDATA = "userdata"

SPACE = "\n"
DASH = Fore.BLUE + "-" * 50
CENTER_WIDTH = 50
NOT_VALID = (
    '!', '?', '@', '*', '^', '.', '£', '$', '%', ',', '~', '`',
    '+', '=', '<', '>', '|', '\\', '/', '[', ']', '{', '}', '#'
)

# ROM (Range of Motion) conversion
ROM_CONVERSION = {
    "a": "Less than 45°",
    "b": "Less than 90°",
    "c": "Approximately 90°",
    "d": "Greater than 100°",
    "e": "Greater than 120",
}

ROM_DEGREES = {
    "a": 45,
    "b": 89,
    "c": 90,
    "d": 100,
    "e": 120
}

# Weight Bearing conversion
WEIGHT_BEARING_CONVERSION = {
    "a": "0-25% weight-bearing",
    "b": "50-75% weight-bearing",
    "c": "75%+ weight-bearing",
    "d": "100% weight-bearing"
}

DISCLAIMER = Fore.YELLOW + (
    "\nDISCLAIMER:\n"
    "This tool is for educational and self-tracking purposes only.\n"
    "It does not provide medical advice, diagnosis, or treatment.\n"
    "If you are experiencing complications or severe symptoms,\n"
    "please consult your healthcare professional.\n"
) + Style.RESET_ALL


def welcome_user():
    """
    This function displays a welcome message and requests a username input.
    It also checks if the username is valid and if it already exists.
    It then asks for a password and updates the users worksheet.
    A try block is used to catch any unexpected errors.
    """
    welcome_messages = [
        "Welcome, new user!",
        "This tool has been developed to help you track",
        "your recovery after a knee replacement.",
        "",
        "Please enter a username to begin your journey.",
        "You'll be guided through a few short questions.",
        "Each answer will be saved to help monitor your progress.",
        "You can type 'quit' at any time to exit the program.",
        "To review your recovery progress in the future,",
        "you can log in using your username and password.",
        ""
    ]

    print(DASH)
    print(SPACE)
    for message in welcome_messages:
        print(message.center(CENTER_WIDTH))
    print(SPACE)
    print(DASH)
    print(DISCLAIMER)

    print(DASH)
    while True:
        user_name = input(Style.RESET_ALL + "Please enter your username: ")
        user_name = user_name.strip()
        if user_quit(user_name):
            return None
        is_valid, error_message = validate_user(user_name)
        if not is_valid:
            print(Fore.RED + error_message + Style.RESET_ALL)
            continue
        if check_existing_username(user_name):
            print(Fore.RED +
                  "This username already exists. " +
                  "Please choose another." +
                  Style.RESET_ALL)
            continue
        password = user_password()
        if password == "quit":
            return None
        update_user_worksheet(user_name, password)
        print(f"\nHello, {user_name}! Please answer the following questions "
              f"so we can find out more about your recovery.")
        return user_name


def validate_user(input_str):
    """
    Validates username and name inputs:
    - Must be 2-10 characters long
    - Must not contain special characters
    """
    if len(input_str) < 2 or len(input_str) > 10:
        return False, (
            Fore.RED +
            "Username must be between 2 and 10 characters." +
            Style.RESET_ALL
        )
    for char in NOT_VALID:
        if char in input_str:
            return False, (
                Fore.RED +
                "Invalid name. Please avoid special characters." +
                Style.RESET_ALL
            )
    return True, ""


def user_password():
    """
    This function handles password input and validation.
    It checks if the password is at least 6 characters long.
    It checks if the password contains spaces.
    """
    while True:
        password = input("Please enter a password (minimum 6 characters): ")
        if user_quit(password):
            return "quit"
        is_valid_pass, pass_error = validate_password(password)
        if is_valid_pass:
            return password
        else:
            print(Fore.RED + pass_error + Style.RESET_ALL)


def validate_password(password):
    """
    This function validates the password.
    It ensures it is at least 6 characters long.
    This will also check for white spaces.
    """
    if len(password) < 6:
        return False, (
            Fore.RED +
            "Password must be at least 6 characters long." +
            Style.RESET_ALL
        )
    if ' ' in password:
        return False, (
            Fore.RED +
            "Password cannot contain spaces." +
            Style.RESET_ALL
        )
    return True, ""


def questions():
    """
    This function asks the user a series of questions.
    It validates the answers and updates the worksheet.
    Returns the valid answer or None if the user quits.
    """
    responses = {}
    question_set = [
        (
            "What is your name?",
            validate_user,
            (Fore.RED +
             "Invalid name, please enter a name between 2-10 characters." +
             Style.RESET_ALL)
        ),
        (
            "When did you have your surgery? (DD/MM/YYYY)",
            validate_date,
            (Fore.RED +
             "Date must be in DD/MM/YYYY format and must be a valid date." +
             Style.RESET_ALL)
        ),
        (
            "Have you had any complications since your surgery? (Yes/No)",
            validate_complications,
            (Fore.RED +
             "Please answer with 'Yes' or 'No'." +
             Style.RESET_ALL)
        ),
        (
            "On a scale of 0-10, what is your current pain level?\n"
            "0 = No pain, 10 = Worst imaginable pain",
            validate_pain_scale,
            (Fore.RED +
             "Please enter a number between 0 and 10." +
             Style.RESET_ALL)
        ),
        (
            "How far can you currently bend your knee?\n"
            "A: I struggle to bend it and have minimal movement\n"
            "B: I can bend it a little but my heel is in front\n"
            "C: I can bend it so my heel is roughly in line\n"
            "D: I can bend it well as my heel goes behind\n"
            "E: The heel is a few inches behind the knee when i bend",
            validate_rom,
            "Please choose A, B, C, D or E."
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
                msg = (
                    validation_message
                    if validation_message
                    else f"Your answer: {answer}"
                )
                print(f"{msg}\n")
                responses[question] = answer
                break
            else:
                msg = (
                    validation_message
                    if validation_message
                    else error_message
                )
                print(msg)
    if answer.lower() in ("yes", "y", 'yep'):
        print("Please consult a healthcare professional about your "
              "complications.")
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
        return False, (
            "The surgery date cannot be in the future. "
            "Please check and try again."
        )
    if days_ago > 730:
        return False, (
            Fore.RED +
            "Surgery date should be within 2 years for tracking. " +
            "Please consult your healthcare provider." +
            Style.RESET_ALL
        )
    return True, f"Surgery was {days_ago} days ago on {date_str}."


def validate_complications(answer):
    """
    This function accepts only 'yes' or 'no' answers.
    It removes whitespace and converts to lowercase.
    Uses a conditional statement to allow similar responses
    to yes and no.
    """
    if answer.lower() in ("yes", "no", 'y', 'n', 'yep', 'nope'):
        return True, ""
    return False, ""


def validate_pain_scale(pain):
    """
    This function validates the pain scale.
    It checks if the input is a number between 0 and 10.
    If the input is 10, it will print a message and exit.
    """
    try:
        num = int(pain)
        if 0 <= num <= 10:
            if num == 10:
                print(
                    "Your pain level is 10/10. That sounds very uncomfortable "
                    "and would recommend consulting a healthcare professional "
                    "for advice."
                )
                print(
                    "We recommend pausing the assessment for now. "
                    "Take care.\n"
                )
                exit()
            return True, f"Your pain level is {num}/10."
        else:
            return False, (
                Fore.RED +
                "Please enter a number between 0 and 10." +
                Style.RESET_ALL
            )
    except ValueError:
        return False, (
            Fore.RED +
            "Pain level must be a whole number" +
            Style.RESET_ALL
        )


def validate_rom(answer):
    """
    This function validates range of motion (ROM) input.
    This will remove whitespace and converts to lowercase.
    It then checks if the input matches the valid options.
    If valid, it returns True and prints the message.
    If invalid, it returns False and prompts the user
    to enter a valid choice.
    """
    choice = answer.lower().strip()
    if choice in ROM_CONVERSION:
        base_message = f"Knee bend: {ROM_CONVERSION[choice]}"
        return True, base_message
    return False, (
        Fore.RED +
        "Please choose A, B, C, D or E." +
        Style.RESET_ALL
    )


def validate_weight_bearing(answer):
    """
    This function validates the weight bearing status.
    Returns a tuple (is_valid, message).
    If the input is 'a', recommends medical review and exits.
    """
    if answer is None:
        return False, "Please choose A, B, C or D."
    selection = answer.lower().strip()
    if selection in WEIGHT_BEARING_CONVERSION:
        if selection == "a":
            print(
                "This sounds very uncomfortable and would recommend "
                "consulting a healthcare professional for advice."
            )
            print(
                "We recommend pausing the assessment for now. "
                "Take care.\n"
            )
            exit()
        base_message = (
            f"{WEIGHT_BEARING_CONVERSION[selection]}"
        )
        return True, base_message
    return False, (
        Fore.RED +
        "Please choose A, B, C or D.\n" +
        Style.RESET_ALL
    )


def assess_rom_progress(metric_data):
    """
    Assesses user's Range of Motion (ROM) progress using their metric data.
    It returns True if it successfully provides an assessment.
    It checks what ROM was recorded and converts it to a choice.
    Converts the number of days since surgery to an integer.
    It uses conditional statements to determine the ROM choice.
    A try block is used to catch any unexpected errors.
    """
    try:
        if not metric_data[3]:
            print(
                "\nCannot perform ROM assessment: "
                "Days since surgery not available"
            )
            return False
        days_since_surgery = int(metric_data[3])
        rom_data = metric_data[6].split('\n')[0]
        rom_choice = None
        if "Less than 45°" in rom_data:
            rom_choice = "a"
        elif "Less than 90°" in rom_data:
            rom_choice = "b"
        elif "Approximately 90°" in rom_data:
            rom_choice = "c"
        elif "Greater than 100°" in rom_data:
            rom_choice = "d"
        elif "Greater than 120°" in rom_data:
            rom_choice = "e"
        if rom_choice:
            assessment = get_rom_timeline_assessment(
                ROM_DEGREES,
                rom_choice,
                days_since_surgery
            )
            print(Fore.YELLOW + "\nROM Assessment:")
            print("-" * 50)
            print(Fore.BLUE + assessment)
            print(Fore.YELLOW + "-" * 50 + Style.RESET_ALL)
            return True
    except Exception as e:
        print(f"Error performing ROM assessment: {e}")
        return False


def assess_pain_progress(metric_data):
    """
    Assesses user's pain level progress using their metric data.
    It returns True if it successfully provides and assessment.
    It checks if the days since surgery is availiable.
    It checks if the pain level is availiable.
    A try block is used to catch any unexpected errors.
    It uses the get_pain_timeline_assessment function to
    get the assessment.
    """
    try:
        if not metric_data[3]:
            print(
                "\nCannot perform pain assessment: "
                "Days since surgery not available"
            )
            return False
        days_since_surgery = int(metric_data[3])
        pain_level = metric_data[5]
        if not pain_level:
            print(
                "\nCannot perform pain assessment: "
                "Pain level data not available"
            )
            return False
        assessment = get_pain_timeline_assessment(
            pain_level,
            days_since_surgery
        )
        print(Fore.YELLOW + "\nPain Level Assessment:")
        print("-" * 50)
        print(Fore.BLUE + assessment)
        print(Fore.YELLOW + "-" * 50 + Style.RESET_ALL)
        return True
    except Exception as e:
        print(f"Error performing pain assessment: {e}")
        return False


def assess_weight_bearing_progress(metric_data):
    """
    Assesses user's weight bearing progress using their metric data.
    It returns True if it successfully provides an assessment.
    It checks if the days since surgery is availiable.
    It checks if the weight bearing status is availiable.
    A try block is used to catch any unexpected errors.
    It uses the get_weight_bearing_timeline_assessment function
    to get the assessment.
    """
    try:
        if not metric_data[3]:
            print(
                "\nCannot perform weight bearing assessment: "
                "Days since surgery not available"
            )
            return False
        days_since_surgery = int(metric_data[3])
        metrics = format_user_data(metric_data)
        wb_status = metrics["weight_bearing"]
        if not wb_status:
            print(
                "\nCannot perform weight bearing assessment: "
                "Weight bearing status not available"
            )
            return False
        assessment = get_weight_bearing_timeline_assessment(
            wb_status,
            days_since_surgery
        )
        print(Fore.YELLOW + "\nWeight Bearing Assessment:")
        print("-" * 50)
        print(Fore.BLUE + assessment)
        print(Fore.YELLOW + "-" * 50 + Style.RESET_ALL)
        return True
    except Exception as e:
        print(f"Error performing weight bearing assessment: {e}")
        return False


def update_rehab_metrics_worksheet(data):
    """
    This function updates the worksheet with user data.
    It checks if the worksheet is empty.
    If it is, it will add the headers.
    It then appends the data to the worksheet.
    A try block is used to catch any unexpected errors.
    """
    try:
        metric_worksheet = SPREADSHEET.worksheet(WORKSHEET_USERDATA)
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
    """
    This function updates the users worksheet with the
    username and password.
    A try block is used to catch any unexpected errors.
    """
    try:
        user_worksheet = SPREADSHEET.worksheet(WORKSHEET_USERS)
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
    print("Welcome to Rehab Metrics!".center(CENTER_WIDTH))
    print(SPACE)
    print(DASH)
    print(DISCLAIMER)
    print(Fore.BLUE + "\nAre you a new user?" + Style.RESET_ALL)
    status = input("Please enter (Y) for Yes or (N) for No: ")
    return status.lower() == 'y'


def check_existing_username(username):
    """
    Check if a username already exists in the users worksheet.
    Returns True if username exists, False otherwise.
    A try block is used to catch any unexpected errors.
    """
    try:
        user_worksheet = SPREADSHEET.worksheet(WORKSHEET_USERS)
        usernames = user_worksheet.col_values(1)[1:]
        return username in usernames
    except Exception as e:
        print(f"Error checking username: {e}")
        return False


def get_user_row(username, worksheet):
    """
    This finds the row number in Google Sheets
    where the username is stored in 'userdata'.
    This will skip the header row and start at
    row 1 where it loops through the usernames.
    It returns None if the username is not found.
    """
    try:
        usernames = worksheet.col_values(1)
        if len(usernames) <= 1:
            print("No user data found.")
            return None
        for index in range(1, len(usernames)):
            if usernames[index] == username:
                return index + 1
        return None
    except Exception as e:
        print(f"Error getting user row: {e}")
        return None


def get_user_metric_data(username, metric_worksheet):
    """
    Retrieves the metric data for a given username.
    Skips the header row and returns the matching entry.
    Returns None if data is not found.
    """
    all_metric_data = metric_worksheet.get_all_values()
    for row in all_metric_data[1:]:
        if row and row[0] == username:
            return row
    print(f"No data found for {username}.")
    return None


def format_user_data(metric_data):
    """
    Format the metric data for display.
    This function takes a row of metric data from the userdata worksheet.
    It formats the data into a structured dictionary.
    It removes whitespace and converts to lowercase.
    Replaces the label for pain level and weightbearing status.
    """
    metrics = {
        "username": metric_data[0],
        "name": metric_data[1],
        "surgery_date": metric_data[2],
        "days_since_surgery": metric_data[3],
        "complications": metric_data[4],
        "pain_level": metric_data[5].strip(),
        "rom": (
            metric_data[6]
            .split('\n')[0]
            .replace("Knee bend: ", "")
            .strip()
        ),
        "weight_bearing": (
            metric_data[7]
            .replace("Weight bearing status: ", "")
            .strip()
        )
    }
    return metrics


def display_user_metrics(metrics):
    """
    Display the formatted user metrics from the worksheet.
    It uses the metrics dictionary to print the data.
    """
    print(Fore.YELLOW + "\nYour Profile and Rehabilitation Data:")
    print("-" * 50 + Style.RESET_ALL)
    print(f"Username: {metrics['username']}")
    print(f"Name: {metrics['name']}")
    print(f"Surgery Date: {metrics['surgery_date']}")
    print(f"Days Since Surgery: {metrics['days_since_surgery']}")
    print(f"Complications Reported: {metrics['complications']}")
    print(f"Pain Level (0-10): {metrics['pain_level']}")
    print(f"Knee Range of Motion: {metrics['rom']}")
    print(f"Weight Bearing Status: {metrics['weight_bearing']}")
    print(Fore.YELLOW + "-" * 50 + Style.RESET_ALL)


def get_user_data(username):
    """
    Retrieve and display user data from users and userdata worksheet.
    It checks if the username is found in the users worksheet.
    It checks if the metric data is found in the userdata worksheet.
    It formats the data into a dictionary and displays it.
    It then assesses the ROM, pain and weight bearing progress.
    A try block is used to catch any unexpected errors.
    """
    try:
        user_worksheet = SPREADSHEET.worksheet(WORKSHEET_USERS)
        username_row = get_user_row(username, user_worksheet)
        if username_row is None:
            print(f"Username '{username}' not found.")
            return False
        metric_worksheet = SPREADSHEET.worksheet(WORKSHEET_USERDATA)
        metric_data = get_user_metric_data(username, metric_worksheet)
        if metric_data is None:
            print("No rehabilitation data found for this user.")
            return False
        metrics = format_user_data(metric_data)
        display_user_metrics(metrics)
        assess_rom_progress(metric_data)
        assess_pain_progress(metric_data)
        assess_weight_bearing_progress(metric_data)
        return True
    except Exception as e:
        print(f"Error retrieving user data: {e}")
        return False


def verify_password(username, password):
    """
    Connects to the users worksheet and checks if the username
    is found in the worksheet.
    Finds the index of the username and returns the password.
    Returns True if password matches the stored password.
    """
    try:
        user_worksheet = SPREADSHEET.worksheet(WORKSHEET_USERS)
        usernames = user_worksheet.col_values(1)
        if username not in usernames:
            return False
        row_idx = usernames.index(username) + 1
        stored_password = user_worksheet.cell(row_idx, 2).value
        return password == stored_password.strip()
    except Exception:
        print("Error verifying password")
        return False


def handle_returning_user():
    """
    Handle the login process for returning users.
    It checks if the username and password are valid.
    Also checks if the worksheet is empty.
    This uses a while loop to allow the user to try again.
    It also checks if the user wants to quit the program.
    """
    print(
        Fore.BLUE +
        "\nWelcome back! Please login to view your data." +
        Style.RESET_ALL
    )
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
            print(
                Fore.RED +
                "\nIncorrect username or password." +
                Style.RESET_ALL
            )
        retry = input(
            Fore.BLUE +
            "\nWould you like to try again? (Y/N): "
        ).lower()
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


def process_new_user():
    """
    Handle the registration and data collection for a new user.
    It checks if the username is valid and if it already exists.
    It converts the surgery date to a date object.
    It works out the number of days since surgery.
    It then updates the worksheet.
    """
    username = welcome_user()
    if username is None:
        return
    responses = questions()
    if responses is None:
        return
    surgery_date_str = responses.get(
        "When did you have your surgery? (DD/MM/YYYY)",
        ""
    )
    try:
        surgery_date = datetime.strptime(
            surgery_date_str,
            "%d/%m/%Y"
        ).date()
    except ValueError:
        print("Invalid surgery date format. Please use DD/MM/YYYY.")
        return
    current_date = datetime.today().date()
    days_since_surgery = (current_date - surgery_date).days
    rom_q = (
        "How far can you currently bend your knee?\n"
        "A: I struggle to bend it and have minimal movement\n"
        "B: I can bend it a little but my heel is in front\n"
        "C: I can bend it so my heel is roughly in line\n"
        "D: I can bend it well as my heel goes behind\n"
        "E: The heel is a few inches behind the knee when i bend"
    )
    wb_q = (
        "Weight bearing on operated leg?\n"
        "A: I struggle to put any weight\n"
        "B: I can partially weight bear with aid\n"
        "C: Most weight with aid but have limp\n"
        "D: Full weight bearing without aids\n"
    )
    rom_valid, _ = validate_rom(responses.get(rom_q, ""))
    wb_valid, _ = validate_weight_bearing(responses.get(wb_q, ""))
    if not (rom_valid and wb_valid):
        print("Invalid ROM or weight-bearing input. Please try again.")
        return
    rom = ROM_CONVERSION[responses.get(rom_q, "").lower().strip()]
    wb = WEIGHT_BEARING_CONVERSION[responses.get(wb_q, "").lower().strip()]
    complications_q = (
        "Have you had any complications since your surgery? "
        "(Yes/No)"
    )
    pain_q = (
        "On a scale of 0-10, what is your current pain level?\n"
        "0 = No pain, 10 = Worst imaginable pain"
    )
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


def display_update_options():
    """
    Display the available options for updating user data.
    Returns the user's choice.
    """
    print(Fore.BLUE + "\nWould you like to update any of your data?")
    print("Available options:")
    print("1. Update Pain Level")
    print("2. Update Knee Range of Motion")
    print("3. Update Weight Bearing Status")
    print("4. No updates needed")
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        if choice in ['1', '2', '3', '4']:
            return choice
        print(
            Fore.RED +
            "Please enter a number between 1 and 4" +
            Style.RESET_ALL
        )


def main():
    """
    This is the start of the program.
    Handles both new and returning users.
    """
    is_new_user = check_user_status()
    if is_new_user:
        process_new_user()
    else:
        handle_returning_user()
        display_update_options()


main()
