import src.parse_data as parser
import copy
from src.route_time_helper import calc_time


class FullMatrix:
    def __init__(self, matrix, rows, cols):
        self.matrix = copy.deepcopy(matrix)
        self.rows = copy.deepcopy(rows)
        self.cols = copy.deepcopy(cols)
        self.additive_time = 0


def get_solution(conditions):
    solution = parser.decode_data('{ "bypass": [] }')
    solution.bypass.append({conditions.initial: conditions.time})
    answers = calculate(conditions)
    return get_best_answer(answers, solution, conditions)


def get_best_answer(answers, solution, conditions):
    answer = min(answers, key=lambda l: l['additive_time'])
    previous = conditions.vertices.index(conditions.initial)
    prev_time = list(solution.bypass[-1].values())[0]
    for i in range(len(answer) - 1):
        additive_time = calc_time(prev_time, conditions.graph[previous][answer[previous]])
        prev_time = additive_time
        solution.bypass.append({conditions.vertices[answer[previous]]: additive_time})
        previous = answer[previous]
    return solution


def calculate(data):
    return matrix_iteration(FullMatrix(data.graph, list(range(len(data.vertices))),
                                       list(range(len(data.vertices)))), [])


def matrix_iteration(initial_matrix, answers):
    if len(initial_matrix.matrix) < 2:
        return small_matrix_answer(initial_matrix, answers)
    full_matrix = copy.deepcopy(initial_matrix)
    prepare_matrix(full_matrix)
    return matrix_shrink(full_matrix, find_zeros(full_matrix.matrix), answers)


def small_matrix_answer(full_matrix, answers):
    if full_matrix.matrix[0][0] == float("Inf"):
        answers = []
        return answers
    solution = {full_matrix.rows[0]: full_matrix.cols[0]}
    for answer in answers:
        answer.update(solution)
    if not answers:
        answers = [solution]
    return answers


def prepare_matrix(full_matrix):
    # make sure that there won't be premature cycles and fix matrix, if it could be
    # (because it works and is easier, than make it when remove row and col)
    additive_time = 0
    matrix = full_matrix.matrix
    for i in range(len(matrix)):
        if max(matrix[i]) != float("Inf"):
            for j in range(len(matrix)):
                max_element = -1
                for k in range(len(matrix)):
                    if matrix[k][j] > max_element:
                        max_element = matrix[k][j]
                if max_element != float("Inf"):
                    matrix[i][j] = float("Inf")
    for row in matrix:
        min_element = min(row)
        additive_time = additive_time + min_element
        for i in range(len(row)):
            row[i] = row[i] - min_element
    for i in range(len(matrix)):
        col = []
        for j in range(len(matrix)):
            col.append(matrix[j][i])
        min_element = min(col)
        additive_time = additive_time + min_element
        for j in range(len(matrix)):
            matrix[j][i] = matrix[j][i] - min_element
    full_matrix.additive_time = full_matrix.additive_time + additive_time


def find_zeros(matrix):
    zeros = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                zeros.append((i, j))
    return zeros


def matrix_shrink(full_matrix, zeros, answers):
    coefficients = calculate_coefficients(full_matrix.matrix, zeros)
    max_coefficient = max(coefficients, key=lambda l: l[0])
    to_remove = [max_coefficient]
    for coefficient in coefficients:
        if coefficient[0] == max_coefficient[0] and coefficient != max_coefficient:
            to_remove.append(coefficient)
    new_answers = []
    for remove in to_remove:
        new_answers.extend(shrink_and_add(full_matrix, remove, answers))
    return new_answers


def shrink_and_add(full_matrix, remove, answers):
    copy_answers = copy.deepcopy(answers)
    copy_matrix = copy.deepcopy(full_matrix)
    if not copy_answers:
        copy_answers = [{'additive_time': 0, copy_matrix.rows[remove[1][0]]: copy_matrix.cols[remove[1][1]]}]
    else:
        for answer in copy_answers:
            answer[copy_matrix.rows[remove[1][0]]] = copy_matrix.cols[remove[1][1]]
            answer['additive_time'] = copy_matrix.additive_time
    del (copy_matrix.matrix[remove[1][0]])
    for row in copy_matrix.matrix:
        del (row[remove[1][1]])
    del (copy_matrix.rows[remove[1][0]])
    del (copy_matrix.cols[remove[1][1]])
    return matrix_iteration(copy_matrix, copy_answers)


def calculate_coefficients(matrix, zeros):
    coefficients = []
    for zero in zeros:
        first_min = second_min = float("Inf")
        for i in range(len(matrix[zero[0]])):
            if i != zero[1] and matrix[zero[0]][i] < first_min:
                first_min = matrix[zero[0]][i]
        for i in range(len(matrix)):
            if i != zero[0] and matrix[i][zero[1]] < second_min:
                second_min = matrix[i][zero[1]]
        if first_min == float("Inf"):
            first_min = 0
        if second_min == float("Inf"):
            second_min = 0
        coefficients.append((first_min + second_min, zero))
    return coefficients
