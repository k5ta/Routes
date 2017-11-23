import itertools
import src.parse_data as parser


def get_exact_solution(conditions):
    min_route = full_search(conditions.graph, conditions.vertices, conditions.initial)
    solution = parser.decode_data('{ "bypass": [] }')
    solution.bypass.append({conditions.initial: conditions.time})
    solution.bypass.extend(min_route)
    print(solution)
    return solution


def full_search(matrix, vertices, initial):
    indexes = []
    initial_index = -1
    for i in range(len(vertices)):
        if vertices[i] != initial:
            indexes.append(i)
        else:
            initial_index = i
    permutations = itertools.permutations(indexes)
    variants = []
    for each in permutations:
        variants.append((initial_index, each[0], each[1]))
    min_length = float("Inf")
    min_route = None
    for each in variants:
        current_length = get_route_length(matrix, each)
        if min_length > current_length:
            min_length = current_length
            min_route = each
    return min_route


def get_route_length(matrix, vertices):
    route_length = 0
    for i in range(len(vertices) - 1):
        route_length = route_length + matrix[vertices[i]][vertices[i + 1]]
    return route_length + matrix[vertices[-1]][vertices[0]]
