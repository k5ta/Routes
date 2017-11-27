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
    answer = calculate(conditions)
    return get_answer(answer, solution, conditions)


def get_answer(answer, solution, conditions):
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
                                       list(range(len(data.vertices)))), {"current_bound": float("Inf")})


def matrix_iteration(initial_matrix, answer):
    if len(initial_matrix.matrix) < 2:
        solution = small_matrix_answer(initial_matrix)
        if solution and solution['current_bound'] < answer['current_bound']:
            answer.update(solution)
            return answer
    prepare_matrix(initial_matrix)
    if initial_matrix.additive_time >= answer['current_bound']:
        return {}
    return matrix_shrink(initial_matrix, find_zeros(initial_matrix.matrix), answer)


def matrix_shrink(full_matrix, zeros, answer):
    coefficients = calculate_coefficients(full_matrix.matrix, zeros)
    max_coefficient = max(coefficients, key=lambda l: l[0])
    to_remove = [max_coefficient]
    for coefficient in coefficients:
        if coefficient[0] == max_coefficient[0] and coefficient != max_coefficient:
            to_remove.append(coefficient)
    for remove in to_remove:
        matrix = full_matrix if len(to_remove) == 1 else copy.deepcopy(full_matrix)
        iteration_answer = shrink_and_add(matrix, remove, answer)
        if iteration_answer and iteration_answer['current_bound'] < answer['current_bound']:
            answer = iteration_answer
    return answer


def shrink_and_add(full_matrix, remove, answer):
    copy_matrix = full_matrix
    new_answer = {copy_matrix.rows[remove[1][0]]: copy_matrix.cols[remove[1][1]]}
    new_answer.update(answer)
    del (copy_matrix.matrix[remove[1][0]])
    for row in copy_matrix.matrix:
        del (row[remove[1][1]])
    del (copy_matrix.rows[remove[1][0]])
    del (copy_matrix.cols[remove[1][1]])
    return matrix_iteration(copy_matrix, new_answer)


def small_matrix_answer(full_matrix):
    if full_matrix.matrix[0][0] == float("Inf"):
        return {}
    solution = dict({full_matrix.rows[0]: full_matrix.cols[0]})
    solution['current_bound'] = full_matrix.additive_time + full_matrix.matrix[0][0]
    return solution


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
    matrix_symmetry = check_symmetric(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0 and should_add_zero(matrix_symmetry, len(matrix), i, j):
                zeros.append((i, j))
    return zeros


def check_symmetric(matrix):
    direction = "no"
    if matrix[0][0] == float("Inf"):
        direction = "from_left"
    elif matrix[0][len(matrix)-1] == float("Inf"):
        direction = "from_right"
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j - i] != matrix[j - i][i]:
                return "no"
    return direction


def should_add_zero(symmetry_type, matrix_len, i, j):
    if symmetry_type == "no":
        return True
    if symmetry_type == "from_left" and j > i:
        return True
    if symmetry_type == "from_right" and i + j < matrix_len:
        return True


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
