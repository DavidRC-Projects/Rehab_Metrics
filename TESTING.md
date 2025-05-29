# Manual Testing

## User Authentication Testing

| Feature | Testing Performed | Result | Pass/Fail |
|---------|------------------|---------|-----------|
| Username Length (Too Short) | Entered username "a" | Error message: "Username must be between 2 and 10 characters" | Pass |
| Username Length (Too Long) | Entered username "abcdefghijk" | Error message: "Username must be between 2 and 10 characters" | Pass |
| Username Length (Valid) | Entered username "testuser" | Username accepted and prompted for password | Pass |
| New User Registration | Entered new username and password | Successfully created new user account | Pass |
| Returning User Login | Entered existing username and password | Successfully logged in | Pass |
| Invalid Username (Special Characters) | Entered username "test@user" during registration | Error message: "Invalid name. Please avoid special characters" displayed | Pass |
| New User Password (Too Short) | Entered password "12345" during registration | Error message: "Password must be at least 6 characters long" displayed | Pass |
| New User Password (With Spaces) | Entered password "pass word" during registration | Error message: "Password cannot contain spaces" displayed | Pass |
| New User Password (Valid) | Entered password "password123" during registration | Password accepted | Pass |
| Returning User (Invalid Password) | Entered incorrect password for existing user | Error message: "Incorrect username or password" displayed | Pass |
| Quit During New User Registration | Entered 'quit' during new user username/password input | Program exited | Pass |
| Quit During Returning User Login | Entered 'quit' during returning user username/password input | Program exited | Pass |

## Data Input Testing

### Pain Assessment
| Feature | Testing Performed | Result | Pass/Fail |
|---------|------------------|---------|-----------|
| Pain Scale Input (0-10) | Entered various numbers within range | Correctly accepted valid inputs | Pass |
| Invalid Pain Input | Entered numbers outside 0-10 range | Error message displayed | Pass |
| Non-numeric Input | Entered letters/special characters | Error message displayed | Pass |
| Pain Level 10/10 | Entered maximum pain level | Warning message displayed about pausing assessment and exits | Pass |

### ROM Assessment
| Feature | Testing Performed | Result | Pass/Fail |
|---------|------------------|---------|-----------|
| ROM Input (0-120) | Entered various numbers within range | Correctly accepted valid inputs | Pass |
| Invalid ROM Input | Enter option F | No Error message displayed and repeated the question | Failed |
| Non-numeric Input | Entered letters/special characters | No error message displayed and repeated the question | Failed |
| ROM Choice Selection | Selected different ROM measurement types | Correctly recorded selected type | Pass |

### Weight Bearing Assessment
| Feature | Testing Performed | Result | Pass/Fail |
|---------|------------------|---------|-----------|
| Weight Bearing Options | Selected different weight bearing levels | Correctly recorded selection | Pass |
| Medical Review Option | Selected 'a' for medical review | Appropriate warning displayed | Pass |
| Invalid Selection | Entered invalid option | No error message displayed and repeated the question | Failed |

## Progress Assessment Testing

| Feature | Testing Performed | Result | Pass/Fail |
|---------|------------------|---------|-----------|
| Pain Progress Timeline | Entered pain levels for different weeks | Correct assessment displayed | Pass |
| ROM Progress Timeline | Entered ROM measurements for different weeks | Correct assessment displayed | Pass |
| Weight Bearing Progress | Entered weight bearing status option c | Displayed Unable to assess weight bearing status: Invalid data format | Failed |
| Early Stage Assessment | Entered data for weeks 0-2 for pain assessment | Incorrect data displayed for week 0-2 | Failed |

## Fixes
| Feature | Fix | Result | Pass/Fail |
|---------|------------------|---------|-----------|
| Weight Bearing Progress | Removed prefix in validate_weight_bearing function | Correct assessment displayed | Passed |
| Early Stage Assessment | Fix logic error in get_pain_timeline_assessment | Correct assessment data displayed for weeks 0-2 | Passed |