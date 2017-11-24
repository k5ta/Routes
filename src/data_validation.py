from re import match


class ParsingDataError(Exception):
    def __init__(self, what):
        self.what = what


def check_data(data):
    error_string = check_initials(data)
    if not error_string:
        error_string = check_matrix(data)
    if error_string:
        raise ParsingDataError("Error in conditions: " + error_string)


def check_initials(data):
    if not data.initial:
        return "wrong initial vertex"
    elif not match(r"\d{2}:\d{2}$", data.time):
        return "wrong initial time"
    elif not isinstance(data.clients, list):
        return "wrong clients array"
    elif not isinstance(data.vertices, list):
        return "wrong vertices array"
    elif len(data.clients) == 0:
        return "the clients array shouldn't be empty"
    elif len(data.clients) != len(data.vertices) - 1:
        return "the length of the clients array should be 1 less than the length of the vertices array"


def check_matrix(data):
    some_list = data.clients[:]
    some_list.append(data.initial)
    if set(some_list) != set(data.vertices):
        return "the vertices array should be like clients array with initial vertex"
    if len(data.graph) != len(data.vertices):
        return "the number of rows of the matrix must be equal to the length of the vertices array"
    for row in data.graph:
        if len(row) != len(data.vertices):
            return "the length of each row of the matrix must be equal to the length of the vertices array"
    error_string = check_matrix_values(data.graph)
    if error_string:
        return error_string


def check_matrix_values(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i == j:
                matrix[i][j] = float("Inf")
            elif matrix[i][j] < 0:
                return "the distance between the vertices must be non-negative"
            elif not match(r"^\d{1,2}(:\d{2})?$", str(matrix[i][j])):
                return "wrong time format in the matrix"
    return ""
