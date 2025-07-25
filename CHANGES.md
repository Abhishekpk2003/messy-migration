# Refactor Summary

##  Major Issues Identified
- SQL injection vulnerability from string formatting in SQL queries
- Plaintext password storage
- No validation or error handling
- Mixed concerns (database, logic, routes all in one file)

##  Changes Made
- Reorganized code into modules: routes, utils, db
- Used bcrypt for password hashing
- Used parameterized SQL queries to prevent injection
- Added validation utilities and error checks
- Returned consistent JSON responses and proper status codes

## Trade-offs
- Kept error handling simple due to time limits
- Did not add test coverage (would be next priority)

##  AI Usage
Used ChatGPT to scaffold and refactor route logic, validation functions, and bcrypt integration.
