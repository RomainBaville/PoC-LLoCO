# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

class AssignmentProblem:
    def __init__(
        self,
        employees,
        projects,
        skills,
        skill_matrix,
        requirements,
    ):
        self.employees = employees
        self.projects = projects
        self.skills = skills
        self.skill_matrix = skill_matrix
        self.requirements = requirements

    def validate(self):
        # Ensure every (employee, skill) exists
        for i in self.employees:
            for k in self.skills:
                self.skill_matrix.setdefault((i, k), 0)

        # Ensure every (project, skill) exists
        for j in self.projects:
            for k in self.skills:
                self.requirements.setdefault((j, k), 0)