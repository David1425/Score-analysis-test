"""David Wang

Module Description
==================
This module contains classes that will be used to create and analyse student data.

Copyright and Usage Information
===============================

This file is Copyright (c) 2024 David Wang
"""
from __future__ import annotations

from typing import Any, Optional, Union
from dataclasses import dataclass


@dataclass
class Node:
    """
    A dataclass used to represent each node in a tree.

    Instance Attributes:
        - item: the contents in this node
        - type: used to identify if the node is a factor or a list of students

    Representation Invariants:
        - type == 'factor' or type == 'students'
    """
    item: Optional[Any]
    type: str


@dataclass
class Factor:
    """
    A dataclass used to represent a factor that affects the students.

    Instance Attributes:
        - label: labels what factor is considered here
        - outcomes: contains the results of the factor

    Representation Invariants:
        - len(label) > 0
        - len(outcomes) > 0
    """
    label: str
    outcomes: set[Any]

    def get_outcome(self) -> Any:
        """
        Used for in the Student class to return the only outcome.
        """
        return next(iter(self.outcomes))


@dataclass
class Student:
    """
    A dataclass used to contain the information of a student.

    Instance Attributes:
        - factor_list:
            contains the factors that possibly affected the student's score and the
            outcome of the factor
        - score:
            represents the academic performance of the student
            is -1 if the score is not known

    Representation Invariants:
        - len(factor_list) > 0
        - all({len(x) == 1 for x in factor_list})
        - score >= -1
    """
    factor_list: list[Factor]
    score: int

    def __str__(self) -> str:
        result = ''
        for factor in self.factor_list:
            result += factor.label + ': ' + str(factor.get_outcome()) + '\n'
        result += 'Score: ' + str(self.score)
        return result


class FactorsTree:
    """
    Contain all the information about the dataset, each layer is branched based on a certain factor.
    The last layer should contain information about the students.

    Private Instance Attributes:
        - _root: is a Node when the tree is non-empty and is None if the tree is empty
        - _subtrees:
            contains smaller trees branching off based on the outcomes of the factor Node,
            empty when _root is a student Node

    Representation Invariants:
        - _root is not None or len(_subtrees) == 0
    """
    _root: Optional[Node]
    _subtrees: dict[any, FactorsTree]

    def __init__(self, root: Optional[Node], subtrees: dict[any, FactorsTree]) -> None:
        """
        Initialize a new FactorsTree.
        Subtrees should be empty when root is None (empty tree).
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """
        Return whether this tree is empty.
        """
        return self._root is None

    def add_student(self, student: Student, index: int) -> None:
        """
        Add a given student's information to the tree.
        """
        if index == len(student.factor_list):
            if self._root is None:
                self._root = Node([], 'students')

            self._root.item.append(student)
        else:
            curr_factor = student.factor_list[index]

            if self._root is None:
                self._root = Node(curr_factor, 'factor')

            result = curr_factor.get_outcome()
            self._root.item.outcomes.add(result)

            if result not in self._subtrees:
                self._subtrees[result] = FactorsTree(None, {})

            self._subtrees[result].add_student(student, index + 1)

    def get_score_by_factor(self, factor: str, curr_outcome: Optional[Any]) -> dict[str, list[Any]]:
        """
        Return a dict that contains two list, one is the score and one is the outcome
        of the given factor.
        A ValueError is raised if the given factor is not in the students' data.

        >>> student_a = Student([Factor('some_factor', {'result 1'})], 80)
        >>> student_b = Student([Factor('some_factor', {'result 1'})], 75)
        >>> student_c = Student([Factor('some_factor', {'result 2'})], 90)
        >>> tree = FactorsTree(None, {})
        >>> tree.add_student(student_a, 0)
        >>> tree.add_student(student_b, 0)
        >>> tree.add_student(student_c, 0)
        >>> tree.get_score_by_factor('some_factor', None)
        {'score': [80, 75, 90], 'factor': ['result 1', 'result 1', 'result 2']}
        """
        result = {'score': [], 'factor': []}
        if self._root.type == 'students':
            if curr_outcome is None:
                raise ValueError
            else:
                for student in self._root.item:
                    result['score'].append(student.score)
                    result['factor'].append(curr_outcome)
                return result
        elif self._root.item.label == factor:
            for outcome in self._subtrees:
                tmp = self._subtrees[outcome].get_score_by_factor(factor, outcome)
                result['score'] += tmp['score']
                result['factor'] += tmp['factor']
        else:
            for outcome in self._subtrees:
                tmp = self._subtrees[outcome].get_score_by_factor(factor, curr_outcome)
                result['score'] += tmp['score']
                result['factor'] += tmp['factor']

        return result

    def get_score_by_outcome(self, factor: str, outcome: str) -> list[int]:
        """
        Return a list of scores of students whose factor matches the target_outcome

        >>> student_a = Student([Factor('some_factor', {'result 1'})], 80)
        >>> student_b = Student([Factor('some_factor', {'result 1'})], 70)
        >>> student_c = Student([Factor('some_factor', {'result 2'})], 90)
        >>> tree = FactorsTree(None, {})
        >>> tree.add_student(student_a, 0)
        >>> tree.add_student(student_b, 0)
        >>> tree.add_student(student_c, 0)
        >>> tree.get_score_by_outcome('some_factor', 'result 1')
        [80, 70]
        """
        if self._root.type == 'students':
            return [x.score for x in self._root.item]
        elif self._root.item.label == factor and outcome in self._subtrees:
            return self._subtrees[outcome].get_score_by_outcome(factor, outcome)
        elif self._root.item.label != factor:
            result = []
            for tmp in self._subtrees:
                result += self._subtrees[tmp].get_score_by_outcome(factor, outcome)
            return result
        else:
            return []

    def get_average(self) -> Union[float, int]:
        """
        Return the average score of all students.

        Precondition:
            - not self.is_empty()

        >>> student_a = Student([Factor('some_factor', {'result 1'})], 80)
        >>> student_b = Student([Factor('some_factor', {'result 1'})], 70)
        >>> student_c = Student([Factor('some_factor', {'result 2'})], 90)
        >>> tree = FactorsTree(None, {})
        >>> tree.add_student(student_a, 0)
        >>> tree.add_student(student_b, 0)
        >>> tree.add_student(student_c, 0)
        >>> tree.get_average()
        80.0
        """
        (tot, cnt) = self.get_sum_and_cnt()
        return round(tot / cnt, 2)

    def get_sum_and_cnt(self) -> (int, int):
        """
        Return a pair with the sum of student scores and
        the number of stundents in this tree.
        """
        if self._root.type == 'students':
            return (sum([x.score for x in self._root.item]), len(self._root.item))
        else:
            tot = 0
            cnt = 0
            for outcome in self._subtrees:
                tmp = self._subtrees[outcome].get_sum_and_cnt()
                tot += tmp[0]
                cnt += tmp[1]
            return (tot, cnt)


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
        'extra-imports': ['typing', 'dataclasses'],
        'max-nested-blocks': 4
    })
