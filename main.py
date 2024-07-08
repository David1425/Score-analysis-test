"""David Wang

Module Description
==================
This module is the main file that will run all the analysis and testing.

Copyright and Usage Information
===============================

This file is Copyright (c) 2024 David Wang
"""
from project_functions import (load_students_tree, load_students,
                               graph_correlations, predict_score)

if __name__ == '__main__':
    # Orders colors when displaying plot
    factor_orders = {
        'gender': ['male', 'female'],
        'race/ethnicity': ['group A', 'group B', 'group C', 'group D', 'group E'],
        'parental level of education': ['some high school', 'high school', 'some college',
                                        'associate\'s degree', 'bachelor\'s degree',
                                        'master\'s degree'],
        'lunch': ['free/reduced', 'standard'],
        'test preparation course': ['none', 'completed']
    }

    # Reading data
    data_file = 'data/data_large.csv'
    math_data = load_students_tree(data_file, 'math score')
    reading_data = load_students_tree(data_file, 'reading score')
    writing_data = load_students_tree(data_file, 'writing score')
    data = {'math': math_data, 'reading': reading_data, 'writing': writing_data}

    # Graphing affect of gender
    graph_correlations(
        data,
        'gender',
        'Score vs gender',
        factor_orders
    )

    # Graphing affect of ethnicity
    graph_correlations(
        data,
        'race/ethnicity',
        'Score vs ethnicity',
        factor_orders
    )

    # Graphing affect of parents' education levels
    graph_correlations(
        data,
        'parental level of education',
        'Score vs parental level of education',
        factor_orders
    )

    # Graphing affect of lunch size on scores
    graph_correlations(
        data,
        'lunch',
        'Score vs lunch size',
        factor_orders
    )

    # Graphing affect of prep course on scores
    graph_correlations(
        data,
        'test preparation course',
        'Score vs completion of preparation course',
        factor_orders
    )

    # Testing score prediction
    err_tot = 0
    test_file = 'data/data_test.csv'
    test_data = load_students_tree(test_file, 'math score')
    test_students = load_students(test_file, 'math score')
    for student in test_students:
        predicted = predict_score(test_data, student)
        print(str(student))
        print('Predicted Score: ' + str(predicted) + '\n')
        err_tot += 100 * abs(predicted - student.score) / student.score
    print('Average absolute error: ' + str(round(err_tot / len(test_students), 2)) + '%')
