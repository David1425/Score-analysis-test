"""David Wang

Module Description
==================
This module contains functions that will be used in main.py.

Copyright and Usage Information
===============================

This file is Copyright (c) 2024 David Wang
"""
import csv
from typing import Union
import plotly.express as px
from project_classes import Factor, Student, FactorsTree


def load_students_tree(student_file: str, subject: str) -> FactorsTree:
    """
    Read the csv file from student_file and create a FactorsTree based on the
    given subject. Return ValueError if subject is not found in the csv.
    """

    result = FactorsTree(None, {})

    with open(student_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            factor_list = []
            for i in range(0, 5):
                factor_list.append(Factor(headers[i], {row[i]}))

            found = False
            for i in range(0, 3):
                if headers[5 + i] == subject:
                    found = True
                    result.add_student(Student(factor_list, int(row[5 + i])), 0)
                    break
            if not found:
                raise ValueError

    return result


def load_students(student_file: str, subject: str) -> list[Student]:
    """
    Read the csv file from student_file and create a list of students data based on the
    given subject. Return ValueError if subject is not found in the csv.
    """
    result = []

    with open(student_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            factor_list = []
            for i in range(0, 5):
                factor_list.append(Factor(headers[i], {row[i]}))

            found = False
            for i in range(0, 3):
                if headers[5 + i] == subject:
                    found = True
                    result.append(Student(factor_list, int(row[5 + i])))
                    break
            if not found:
                raise ValueError

    return result


def graph_correlations(trees: dict[str, FactorsTree], factor: str,
                       plot_title: str, orders: dict[str, list[str]]) -> None:
    """
    Creates a scatter graph of scores of various subjects vs the given factor.
    The FactorsTree should be non-empty

    Preconditions:
        - all({not trees[subject].is_empty() for subject in trees})
    """

    data = {'score': [], 'factor': [], 'subject': []}
    for label in trees:
        tree = trees[label]
        tmp = tree.get_score_by_factor(factor, None)

        data['score'] += tmp['score']
        data['factor'] += tmp['factor']
        for _i in range(0, len(tmp['score'])):
            data['subject'].append(label)

    # print(data)
    fig = px.box(data, y='subject', x='score', color='factor',
                 title=plot_title, category_orders={'factor': orders[factor]})
    fig.update_traces(orientation='h')
    fig.show()


def predict_score(tree: FactorsTree, student: Student) -> Union[float, int]:
    """
    Predict a new student's score based on past data collected in the FactorsTrees.
    This is done by finding the weighted average scores of past students based on
    how many of their factors have similar outcomes of this student.

    This is weighted because students that have more than one similar factor
    are counted multiple times.

    Return average of all scores if there are no similarities.

    >>> student_a = Student([Factor('some_factor', {'result 1'})], 80)
    >>> student_b = Student([Factor('some_factor', {'result 1'})], 70)
    >>> student_c = Student([Factor('some_factor', {'result 2'})], 90)
    >>> test_tree = FactorsTree(None, {})
    >>> test_tree.add_student(student_a, 0)
    >>> test_tree.add_student(student_b, 0)
    >>> test_tree.add_student(student_c, 0)
    >>> new_student = Student([Factor('some_factor', {'result 1'})], -1)
    >>> predict_score(test_tree, new_student)
    75.0
    >>> new_student2 = Student([Factor('some_factor', {'result 3'})], -1)
    >>> predict_score(test_tree, new_student2)
    80.0
    """

    tot = 0
    cnt = 0

    for factor in student.factor_list:
        scores = tree.get_score_by_outcome(factor.label, factor.get_outcome())
        tot += sum(scores)
        cnt += len(scores)

    if cnt == 0:
        return tree.get_average()
    else:
        return round(tot / cnt, 2)


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
        'extra-imports': ['csv', 'project_classes', 'plotly.express', 'typing'],
        'allowed-io': ['load_students_info'],
        'max-nested-blocks': 4
    })
