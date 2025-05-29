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

