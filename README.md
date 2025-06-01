# Rebab Metrics

![Welcome to Rehab Metrics](assets/rehab-metrics.jpeg)

Rehab Metrics is a post-surgery tracking tool that helps users monitor their recovery progress, with a particular focus on knee recovery. Built in Python and deployed via Code Institute's Heroku terminal, the app features secure user registration and login with validation for usernames and passwords. Users enter their details, and the app calculates their stage in the recovery journey, providing feedback on pain levels, knee range of motion, and weight bearing status. All data is securely stored using Google Sheets integration. Rehab Metrics is intended as a supportive self-monitoring tool and includes prompts to consult a healthcare professional when needed, as it does not provide medical advice.

## Project Plan

### Project Goals
I developed Rehab Metrics inspired by a close relative who recently underwent a knee replacement surgery. They had many questions about their recovery, particularly around the expected timeline and what level of movement and activity they should be achieving in the first few months. This app aims to provide clear, stage appropriate guidance to help users monitor their progress and feel more confident during their recovery. From this experience, I realised I could create a project that collects user data and provides advice on key areas of recovery, helping users understand their progress and what to expect during recovery.

## User Stories

### Target Audience

The target audience for Rehab Metrics is people who have recently undergone knee surgery and want to track their recovery progress.

### First Time Visitor Goals

As a first-time user, I want to:

* Easily navigate the application and understand its purpose.
* Enter my personal details related to recovery.
* Have a record of my details that provides feedback on my progress.

### Returning Visitor Goals

As a returning user, I want to:

* Log in securely with my username.
* Enter my password to protect my information.
* Review my previously entered details and progress.

### Site Owner Goals
As the creator of Rehab Metrics, my goal is to develop an intuitive and accessible post operation tracking tool for individuals recovering from knee surgery. I aim to:

* Create a user-friendly interface that avoids medical jargon.
* Ask clear, structured questions that users can easily understand and respond to.
* Convert the user's input into meaningful feedback to give guidance on their stage of recovery.
* Store data securely using Google Sheets.
* Allow returning users to retrieve their previous entries by logging in with a username and password.
* The focus is to provide reassurance and progress tracking during a crucial recovery period.

### Structure of the program
At the start of the project, I created a draft flowchart to visualise the program's intended structure. I had a clear end goal in mind, outlining the key questions and the type of data I aimed to collect and store using Google Sheets.

The early flow focused on capturing user information and guiding them through recover related questions:

![Draft algorithm](assets/draftalgorithm.png)
     
As the project progressed, I refined the flow to include input validation and safety checks to improve the user experience. The final algorithm shows the outcome for new and existing users:

![Algorithm](assets/algorithm.png)

## Features

### Welcome Message and User Status Check

The application launches via python3 run.py. A welcome message with a disclaimer will appear and will ask the user if they are a new user. The main function will be called first and will use the check_user_status function before calling the welcome_user function.

The check_user_status function will ask if the user is a new or an existing user.  

![User check](assets/welcome.png)

The welcome_user function works together with the functions validate_user, check_existing_username, user_password and update_user_worksheet to guide the new user through the sign-up process. After the user inputs their data it will then be saved new to a Google Sheet (users worksheet).

![New user welcome](assets/welcome2.png)

From the image above you can see there is a welcome message displayed with instructions and a disclaimer. If the user enters 'yes' for a new user then the program will then prompt the user to enter their username and validate this. Validation also includes checking the google sheet for usernames that already exist. After entering the username a prompt will appear to input a password. Both the username and password will be saved in Google sheets if the credentials are valid.

![Google worksheet users](assets/googleusers.png)

![Google worksheet users](assets/googleuserdata.png)


### New User Journey

![Questions and assessment](assets/questions.png)

The questions() function guides the user through a structured assessment consisting of six simple questions. These questions are designed to collect relevant post-operative information following a knee replacement surgery. The collected data contributes to a personalised log of their data.

The six questions include:
1. First Name
The user is prompted to enter their first name to make the tool more personalised.
2. Surgery Date
The user inputs the date of their knee replacement surgery. This information is used to calculate how many days have passed since the procedure.
3. Complications
The User will answer 'yes' or 'no' to indicate if they had any complications. If "yes" is selected, the assessment ends immediately with advice to consult a healthcare professional, ensuring a safety-first approach as using the tool.
4. Pain Level
A numeric pain rating is collected on a scale of 0-10 to help gauge their discomfort level. While this value is subjective and can vary significantly between users, it remains a critical data point. A high pain score may indicate underlying issues that could require attention from a healthcare professional.
5. Knee Bend Assessment
The user selects from one of the four options that best describes their ability to bend their knee. This selection is internally converted to an estimated knee flexion value and displayed back to the user.
6. Weight Bearing Status
The user selects one of four options to describe their current weight bearing status. This input is also converted into a weight bearing status and shown back to the user.

The answers provided by the user are stored. This is then displayed later for existing users for progress tracking.


### Returning User Journey

![Questions and assessment](assets/existing_user.png) 

Returning users begin by entering their previously registered username and password. The tool then verifies the credentials to ensure the user is authenticated before proceeding. Upon successful login, users are guided through the assessment questions to update their recovery timeline.

This uses the functions handle_returning_user(), which works by prompting the user to input their username and password. It will then check if the username exists. The tool will then call verify_password() to authenticate the user. If authentication is successful, it loads the user's existing data from 'userdata' worksheet in Google Sheets. If login fails (due to incorrect credentials or non-existent username), the user is informed and given the option to retry or return to the main menu. Please see [Validation](#validation) for further details.

The verify_password function checks whether the password entered by the user matches the stored password for that username. It retrieves the password from the 'users' worksheet in Google Sheets and performs a comparison of the entered password and the stored one. It will return True if the credentials match, allowing the user to proceed; otherwise, returns False, triggering an error message and prompting for re-entry. Please see [Validation](#validation)

Upon completing the assessment questions, the app evaluates recovery progress using the following functions (located in guide.py):
* get_rom_timeline_assessment() – Evaluates range of motion progress (e.g., knee bend).

* get_pain_timeline_assessment() – Evaluates reported pain levels and highlights any concerning scores.

* get_weight_bearing_timeline_assessment() – Evaluates weight-bearing progress.

### Data Storage

All user data is stored securely in Google Sheets using the gspread library:

* "users" worksheet – Stores login credentials (usernames and passwords).

* "userdata" worksheet – Stores each user's recovery progress that is from the answers to assessment questions.

* update_rehab_metrics_worksheet() is responsible for storing all validated assessment data.

### Data Processing and Retrival

* The app determines how many days have elapsed since the user’s recorded surgery date using the calculate_days_since_surgery() function. This value is essential for placing the user's progress in the correct timeframe and helps tailor the feedback they receive accordingly.
* The app retrieves the most recent user data from Google Sheets, allowing for comparison with current inputs.
* get_user_data() – This function fetches the user's previous entries from the "userdata" worksheet based on their username.

### Validation

All inputs are validated. Invalid entries trigger error messages in red coloured text and offer retry prompts.

The login process verifies both username and password before proceeding.

validate_user(input_str)
* Ensures that the username is between 2 and 10 characters long.
* Disallows special characters using a predefined NOT_VALID list.
* If the username is valid and unique, it is accepted.

![New User Validation](assets/new-user-validation.png)

user_password()
* Prompts the user to enter a password.
* Uses validate_password() for validation.
* Continues prompting until a valid password is entered or the user types 'quit'.

validate_password(password)
* Ensures the password is at least 6 characters long.
* Disallows spaces to prevent formatting issues.

![Password Validation](assets/password-validation.png)

Each assessment question has tailored validation to ensure data is appropriate.
* validate_date() - Checks if the surgery date is in the correct YYYY-MM-DD format and ensures the date is not in the future.
* validate_complications() - Accepts only "Yes", "No", or variations thereof (e.g., "Y", "N").
* validate_pain_scale() - Confirms that the pain input is a number between 0 and 10.
* validate_rom() - Accepts only choices A–E. 
* validate_weight_bearing() - Accepts only choices A–D.

### Update Menu options
The function display_update_options() was added to give the users a choice to restart the assessment process or exit the program.
In future updates, it will allow users to update individual metrics they previously entered.

### Safety Feature
The program includes built-in safety mechanisms to help protect users by identifying red flags that may require clinical attention:
* If a user reports a pain level of 10 (the maximum on the 0–10 scale), the program immediately terminates the session and advises the user to consult a healthcare professional. This serves as a safeguard against potentially serious complications.
* If the user's input indicates severely limited weight-bearing ability (e.g., unable to place any weight on the operated leg), the program also exits and directs the user to consult a healthcare professional for further assessment.
* If the user's input indicates complications (e.g., inputing 'yes'), the program exits and directs the user to consult a healthcare professional.
* There are warning messages for concerning symptoms.

Images for safety features************************************

### Program Controls & Error Handling
* Users can exit the program at any point by typing 'quit'. This allows for a user-friendly and accommodating interruptions or changes of mind without causing errors or data loss.
* After each input or action, the user receives immediate, clear feedback. This includes confirmation of successful entries, detailed error messages for invalid inputs, and instructions on how to proceed or correct mistakes.
* All inputs are monitored for validity. Invalid entries prompt user-friendly error messages and re-prompt the user to try again.

### Timeline Based Assessment
The program evaluates recovery progress across four key timeframes following knee replacement surgery:

* 0-2 weeks: Initial recovery phase
* 2-6 weeks: Early recovery phase
* 6-12 weeks: Mid-term recovery
* 12+ weeks: Long-term recovery

In guide.py, the program uses floor division (//) to convert the number of days into weeks. It then applies a series of conditional statements to assess the user’s input (e.g., range of motion, pain level, weight-bearing status) against clinically expected norms for each recovery stage. Each function generates customised feedback based on the user’s data, helping them understand whether their progress is poor, typical or above expectations.

The program automatically calculates the user's recovery stage based on their surgery date and provides stage-appropriate feedback for each metric. This timeline-based assessment helps users understand their progress and identify areas that may require attention or healthcare professional consultation.

## Future Features
* Provide assessment advice on all metrics.
* Include questions on walking and stair climbing to identify functional difficulties.
* Compare users’ walking ability and stair climbing with expected recovery data across a 12-week timeline.
* Add complication screening questions to identify red flags, such as swelling, fever, or sudden worsening of symptoms, and advise users to seek urgent medical attention if necessary.
* Enable returning users to view their previous entries, update their information, and modify data in the worksheet.
* Offer more tailored advice by introducing detailed questions relevant to the user's specific stage of recovery.

## Technologies Used
* Visual Studio Code with assistance of flake8 linter extension.
* [Github](https://github.com/) to host the repository.
* The [CI Python Linter](https://pep8ci.herokuapp.com/#) for validating the Python code.
* [Heroku](https://pep8ci.herokuapp.com/) for deploying the website.
* Flow charts from [Lucid Chart](https://lucid.app).

## Python Version, Packages and Libaries Used
The project was developed using Python 3.13.2.

The following Python packages and libaries were used:
* datetime - Used to work with date and time, particulary to calculate recovery timelines based on number of days since surgery.
* gspread - Used to interact with Google Sheets API for reading and writing data to a spreadsheet.
* google.oauth2.service_account.Credentials - Provides secure authentication for access to Google Sheets API.
* colorama - Used to add colour to the terminal output.

## Bugs and Fixes
Please see fixes in [TESTING.md](TESTING.md) for more details of bug fixes from manual testing.

During development, one recurring issue was encountering KeyErrors. These typically occurred when I modified the text within string-based questions but did not update corresponding keys in other parts of the program that relied on those exact strings (e.g., when storing or retrieving user responses from dictionaries).

Weight-bearing assessment bug - There was an issue with how weight-bearing status was formatted and assessed. This was due to the weight-bearing status being stored as a prefix. Therefore, it caused problems when trying to access the progress. The issue was resolved by using .replace() to strip the prefix and extract only the relevant weight-bearing value.

There was an indexing error when accessing the ROM data from the user’s dataset. The function was referencing a column index that was one position too low, causing incorrect data to be retrieved for the ROM metric. Another issue that arose were mismatched headers in Google Sheets. The logic was updated to skip the first column when reading data from Google Sheets and making sure the correct header columns aligned accurately with the values.

The ROM assessment function had a typo in the ROM_CONVERSION dictionary for option E missing a degrees symbol. This caused the ROM assessment not to appear when option E selected for new users. In addition, the assessment display required the validate_rom to store the ROM measurement and not the assessment message and adjusted format_user_data to display only the ROM measurement in the user profile.

A deprecation warning occured when i copied the spreadsheet initialisation from run.py to guide.py. Removing this in guide.py resolved the warning.

When the surgery date was entered as today's date, the program calculated days_since_surgery = 0, which evaluated as falsy in conditional checks. This incorrectly triggered error messages like:
Cannot perform ROM assessment: Days since surgery not available
To fix this i updated the logic in the validate_date() function to check if days_ago <= 0. Now, the program provides clear feedback and prompts the user to re-enter a valid surgery date instead of treating 0 as missing data.

There are currently no known bugs in the program. All previously identified issues related to data indexing, string mismatches, and weight-bearing status formatting have been resolved.

## Testing

### Manual Testing

See [TESTING.md](TESTING.md) for more details of manual testing.
Manual tests were carried out throughout the development process. Each feature was tested to ensure correct functionality, including error handling, user input validation, and support for multiple user accounts. This included:
- Username and Name Validation: Inputs were tested to confirm that whitespace and special characters were not allowed. The username was validated to accept only 2–10 characters.
- Password Validation: Password inputs were tested to ensure they were at least 6 characters long and contained no whitespace.
- New and Returning Users: Multiple scenarios were tested, including new user registration, returning user login, invalid entries, and quitting mid-process.

### Validation Testing

I used the [CI Python Linter](https://pep8ci.herokuapp.com/#) and followed the [PEP8 guidelines](https://peps.python.org/pep-0008/) to validate my code.

As a result of the linting process, I made the following adjustments:

1. Removed unnecessary blank lines and trailing white spaces.
2. Ensured that all lines are under 79 characters, and limited docstring lines to 72 characters as recommended.
3. Grouped imports in the correct order:
- Standard library imports
- Related third-party imports
- Local application imports

***** image on python linter run.py
***** image of python linter guide.py

## Deployment
This project was deployed using the Code Institute’s mock terminal for Heroku.

Steps for deployment:
1. Add the list of requirements by writing in the terminal "pip3 freeze > requirements.txt".
2. Log into Heroku.
4. Click "NEW" in the top right-hand corner and choos the option Create new app.
5. Input a unique app name.
6. Choose Region - Europe.
7. Choose "Settings" from the menu.
8. Go to section "Config Vars" and click button "Reveal Config Vars”.
9. Add key and value. For this project I added creds.json as the key and copied the contents of this into the value.
10. Go to section "Build packs" and click "Add build pack”.
11. Go to "Deploy" in the menu bar.
12. Go to section "deployment method", choose "GitHub".
13. New section will appear "Connect to GitHub".
14. Type the name of your repository and click "search".
15. Once Heroku finds your repository - click "connect".
16. Click "Enable automatic deploys" or manually deploy by choosing "Deploy branch".
17. Click "Deploy branch".

## Forking and Cloning
To fork this repository:

1. Log in to your Github account.
2. Navigate to the repository page.
3. Click the "Fork" button in the top-right corner.

To Clone:

1. Go to the forked repository on Github.
2. Click the green "Code" button.
3. Copy the HTTPS link: https://github.com/DavidRC-Projects/Rehab_Metrics.git.
4. Open your terminal and type: git clone https://github.com/DavidRC-Projects/Rehab_Metrics.git.

## Credits

https://www.canva.com/dream-lab

https://www.geeksforgeeks.org/hiding-and-encrypting-passwords-in-python/

## Acknowledgements


