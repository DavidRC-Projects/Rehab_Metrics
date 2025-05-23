# Rebab Metrics

Rehab Metrics is a post-surgery rehabilitation tracking tool that helps patients monitor their recovery progress, with a particular focus on knee rehabilitation. Built in Python and deployed via Code Institute's Heroku terminal, the app features secure user registration and login with validation for usernames and passwords. Users enter their details, and the app calculates their stage in the rehabilitation journey, providing feedback on pain levels, knee range of motion, and weight bearing status. All data is securely stored using Google Sheets integration. Rehab Metrics is intended as a supportive self-monitoring tool and includes prompts to consult a healthcare professional when needed, as it does not provide medical advice.

## Project Plan

### Project Goals
I developed Rehab Metrics inspired by a close relative who recently underwent a knee replacement. They had many questions about their recovery, particularly around the expected timeline and what level of movement and activity they should be achieving in the first few months. This app aims to provide clear, stage appropriate guidance to help users monitor their progress and feel more confident during their recovery. From this experience, I realised I could create a project that collects user data and provides advice on key areas of recovery, helping patients understand their progress and what to expect during rehabilitation.

## User Stories

### Target Audience

The target audience for Rehab Metrics is people who have recently undergone knee surgery and want to track their recovery progress.

### First Time Visitor Goals

As a first-time user, I want to:

* Easily navigate the application and understand its purpose
* Enter my personal and surgery details
* Have a record of my details that provides feedback on my progress

### Returning Visitor Goals

As a returning user, I want to:

* Log in securely with my username
* Enter my password to protect my information
* Review my previously entered details and progress

### Site Owner Goals
As the creator of Rehab Metrics, my goal is to develop an intuitive and accessible rehabilitation tracking tool for individuals recovering from knee surgery. I aim to:

* Create a user-friendly interface that avoids medical jargon.
* Ask clear, structured questions that users can easily understand and respond to.
* Convert the user's input into approximate, meaningful feedback about their stage of recovery.
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

1. Program Start
The application launches via python3 run.py. A welcome message with a disclaimer will appear and will ask the user if they are a new user. At this point the application will follow two paths. Both paths will display another welcome message with additonal information on how to use the app and the disclaimer. This is all handled via the welcome_user function.

Welcome user function:

Image

This function uses a while loop that will continue to ask the question unless the user inputs 'quit', which will exit the program. There are 2 inputs in this function to obtain the username and password. Conditional statements validate if the correct username and password have been entered.

When the user enters 'No' the program will request their username followed by their password. There are 2 functions called 'check_existing_user and get_user_data. The main function will call check_existing_user where it will review the google sheets work sheet named 'users' and interate through the user names to find a match. If an existing user is found the get user data function will retrieve the data from Google Sheets. 

3. New User Journey
User provides a username (validated to avoid duplicates).

Then creates a password (validated for security).

Credentials are stored in the "users" worksheet in Google Sheets.
Functions:

validate_user()

check_existing_username()

user_password()

validate_password()

update_user_worksheet()


b) Assessment Questions
The user is guided through 6 simple questions:

First name

Surgery date

Complications (Yes/No)

Pain level (scale of 0–10)

Knee bend assessment (options A–D)

Weight bearing status (options A–D)
Function: questions()

c) Data Processing
Calculates days since surgery.

Validates all responses.

Stores all responses in the "userdata" worksheet.
Function: update_rehab_metrics_worksheet()

4. Returning User Journey
a) Login
The user logs in with their username and password.

Credentials are verified.
Functions:

handle_returning_user()

verify_password()

b) Data Retrieval
The user's previous responses are retrieved from Google Sheets.
Function: get_user_data()

5. Assessment Feedback
Using the data collected, the app provides recovery feedback:

get_rom_timeline_assessment() – Assesses range of motion

get_pain_timeline_assessment() – Assesses pain levels

get_weight_bearing_timeline_assessment() – Assesses weight bearing

These are handled in guide.py.

6. Data Storage
All data is stored in Google Sheets using gspread.

Two worksheets:

"users" – stores login info.

"userdata" – stores recovery responses.

7. Safety Features
If pain level is 10, the program exits and advises medical review.

If weight bearing is severely impaired, the same applies.

Strong input validation prevents invalid data from being accepted.

8. Program Controls & Error Handling
Users can quit anytime by typing "quit".

All inputs are automatically validated.

Invalid entries trigger error messages and retry prompts.

The user receives clear feedback after each step.

## Future Features
* Provide assessment advice on all metrics 
* Questions on walking and climbing stairs to idetify any functional problems
* Provide advice and compare their walking and ability to climb stairs with expected data within a 12 week timelime
* Provide questions on swelling, fever and sudden worsening of symptoms to clear any red flags and to advise ther user to seek advice
* Returning users can input new data and then compare any changes from their previous data. This would be good for user experience.
* Provide more tailored advice for stage of recovery by asking more detailed questions 

## Technologies Used

## Python Version and Packages

## Bugs and Fixes

## Testing

## Deployment

## Forking and Cloning

## Credits

## Acknowledgements


