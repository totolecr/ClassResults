# Install
To install this package, use:  
	`pip install classresults`
This package needs mounette.
For more information on mounette, see https://gitlab.cri.epita.fr/prepa/ec/computer-science/programming/internal/tools/mounette/

# Usage
The list of students should be stored in the `STUDENTS` environement variable. It is a space seperated list of the logins.  
To use the command, do `STUDENTS="<logins>" classresults <activty code>` or 
```
export STUDENTS="<logins>"
classresults <activity code>
```
This will create a `students.xlsx` file with all the data.

# Source
This package's source code is on my github: https://github.com/totolecr/ClassResults

