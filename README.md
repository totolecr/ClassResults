# Install
To install this package, use:  
	`pip install classresults`
This package needs poulpy, to install poulpy do:  
	`pip install poulpy --index-url https://gitlab.cri.epita.fr/api/v4/projects/8706/packages/pypi/simple`
For more information on poulpy, see https://docs.forge.epita.fr/services/poulpy

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

