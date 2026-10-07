import click
import sys
import re
import os

from classresults.get_data import get_data

@click.command()
@click.argument('activity')
def main(activity: str):
    regex = re.compile("prog-[0-9]0[0-9]-[pe]-[0-9]{2}-[0-9]{4}")
    activity = sys.argv[1]

    if not regex.match(activity):
        print(f"Activity name does not match regular expression: {regex.pattern}")
        sys.exit(1)

    STUDENTS = os.getenv("STUDENTS")
    if STUDENTS is None:
        printf("STUDENTS environement variable MUST not be empty, it should contain the list of students' login seperated by spaces")
        sys.exit(2)
    
    students = STUDENTS.split(' ');

    get_data(sys.argv[1], students)

