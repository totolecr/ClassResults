import asyncio
import json
import mounette
import requests
import xlsxwriter

from mounette.modules.operator_api import fetch_traces
from mounette.config.models.operator_api import ActivityQueryParams
from mounette.modules.stats import get_activity_uri, create_filter
from typing import Any

def recreate_trace_url(activity: str, id: str) -> str:
    """
    Assembles the operator's trace url from activity and trace id
    """
    return f"https://operator.forge.epita.fr/epita-prepa-computer-science/{activity}/traces/{id}"


def recreate_impersonate_url(activity: str, login: str, id: str) -> str:
    """
    Assembles the intranet's impersonate url from activity and trace id
    """
    return f"https://intra.forge.epita.fr/epita-prepa-computer-science/{activity}/root/{activity}/{id}?login={login}"


def to_student_trace(studentdata: list[dict[str, Any]], activity: str) -> list[list]:
    """
    Returns a list with all useful data extracted from each trace data
    """
    studentTraces = []
    for student in studentdata:
        # s = studentTrace(student["author"], student["currentJob"]["successPercent"], student["currentJob"]["traceUrl"])
        login = student["author"]
        percent = student["currentJob"]["successPercent"]
        studentTraces.append([login, percent, recreate_trace_url(activity, student["id"]),
                              recreate_impersonate_url(activity, login, student["id"])])

    return studentTraces

def add_unsubmitted_students(traces: list[list], students: list[str]) -> list[list]:
    """
    Addes all student whose submission was not found as 'Did not submit' students
    """
    logins = list(map(lambda r: r[0], traces))

    for student in students:
        if student not in logins:
            traces.append([student, "Did not submit", "Did not submit", "Did not submit"])

    traces.sort(key=lambda r: r[0])
    print(f"Added {len(traces) - len(logins)} students that did not submit")
    return traces

def to_xlsx(traces, filename):
    workbook = xlsxwriter.Workbook(filename)
    sheet = workbook.add_worksheet()
    sheet.write(0, 0, "login")
    sheet.write(0, 1, "percent")
    sheet.write(0, 2, "operator trace url")
    sheet.write(0, 3, "impersonate url")
    sheet.write(0, 4, "Did submit")

    for row, (login, percent, url, impersonate) in enumerate(traces):
        row += 1
        sheet.write(row, 0, login)
        if percent != "Did not submit":
            sheet.write(row, 1, percent / 100)
            sheet.write_url(row, 2, url, string="operator url")
            sheet.write_url(row, 3, impersonate, string="impersonate url")
            sheet.write(row, 4, 1)
        else:
            sheet.write(row, 1, 0)
            sheet.write(row, 4, 0)

    bad_grade = workbook.add_format({'bg_color': '#FF6D6D', 'num_format': 9})
    low_grade = workbook.add_format({'bg_color': '#FFA365', 'num_format': 9})
    mid_grade = workbook.add_format({'bg_color': '#FFFF8F', 'num_format': 9})
    high_grade = workbook.add_format({'bg_color': '#A3FFA3', 'num_format': 9})
    full_grade = workbook.add_format({'bg_color': '#57FF57', 'num_format': 9})
    percent = workbook.add_format({'num_format': 9})

    # Add conditionals
    sheet.conditional_format(1, 1, len(traces), 1,
                             {"type": "cell", "criteria": "=", "value": 1, "format": full_grade})
    sheet.conditional_format(1, 1, len(traces), 1,
                             {"type": "cell", "criteria": ">=", "value": .75, "format": high_grade})
    sheet.conditional_format(1, 1, len(traces), 1,
                             {"type": "cell", "criteria": ">=", "value": .50, "format": mid_grade})
    sheet.conditional_format(1, 1, len(traces), 1,
                             {"type": "cell", "criteria": ">=", "value": .25, "format": low_grade})
    sheet.conditional_format(1, 1, len(traces), 1,
                             {"type": "cell", "criteria": "<", "value": .25, "format": bad_grade})

    sheet.write(8, 8, "Moyenne des derniers submits: ")
    sheet.write_formula(8, 9,
                              f"=AVERAGE(FILTER(B2:B{len(traces) + 1},E2:E{len(traces) + 1}))")
    # Add conditionals
    sheet.conditional_format(8, 9, 8, 9,
                             {"type": "cell", "criteria": "=", "value": 1, "format": full_grade})
    sheet.conditional_format(8, 9, 8, 9,
                             {"type": "cell", "criteria": ">=", "value": .75, "format": high_grade})
    sheet.conditional_format(8, 9, 8, 9,
                             {"type": "cell", "criteria": ">=", "value": .50, "format": mid_grade})
    sheet.conditional_format(8, 9, 8, 9,
                             {"type": "cell", "criteria": ">=", "value": .25, "format": low_grade})
    sheet.conditional_format(8, 9, 8, 9,
                             {"type": "cell", "criteria": "<", "value": .25, "format": bad_grade})

    sheet.write(9, 8, "Nombre d'élèves ayant au moins 1 submit: ")
    sheet.write_formula(9, 9, f"=SUM(E2:E{len(traces) + 1})")

    sheet.write(10, 8, "Pourcentage des élèves ayant au moins 1 submit: ")
    sheet.write_formula(10, 9, f"=ROUND(J10/COUNT(E2:E{len(traces) + 1}),2)", percent)

    sheet.autofit()

    workbook.close()

    print(f"Wrote data to {filename}")


def get_data(activity: str, students: list[str]):
    activity_uri = get_activity_uri(activity)
    params = ActivityQueryParams()
    data = asyncio.run(fetch_traces(activity_uri, params))
    filter = create_filter("submit", ",".join(students), None)
    filtered = [d for d in data if filter(d)]
    filtered_json = json.dumps(filtered)
    traces = to_student_trace(filtered, activity)
    traces = add_unsubmitted_students(traces, students)
    to_xlsx(traces, "students.xlsx")
