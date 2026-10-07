# Install
To install this package, use:  
	`pip install classresults`

# Usage
The list of students should be stored in the `STUDENTS` environement variable. It is a space seperated list of the logins.  
To use the command, do `STUDENTS="<logins>" && classresults <activty code>` or ```bash
export STUDENTS="<logins>"
classresults <activity code>```.  
This will create a `students.xlsx` file with all the data.

