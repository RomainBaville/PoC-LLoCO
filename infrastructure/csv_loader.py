# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import csv


def load_ip_csv(path: str):
    employees = []
    skills = []
    skill_matrix = {}

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Skills = all columns except Nom / Prenom
        fieldnames = reader.fieldnames
        skills = [c for c in fieldnames if c not in ("Nom", "Prenom")]

        for row in reader:
            employee = f"{row['Prenom']} {row['Nom']}"
            employees.append(employee)

            for skill in skills:
                level = int(row[skill])
                skill_matrix[(employee, skill)] = level

    return employees, skills, skill_matrix


def load_project_csv(path: str):
    projects = []
    requirements = {}

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        skills = [c for c in reader.fieldnames if c != "Project"]

        for row in reader:
            project = row["Project"]
            projects.append(project)

            for skill in skills:
                requirements[(project, skill)] = int(row[skill])

    return projects, requirements
