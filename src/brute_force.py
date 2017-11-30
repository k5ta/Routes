import itertools
import src.parse_data as parser
from src.route_time_helper import calc_time


def get_exact_solution(conditions):
    min_route = full_search(conditions.graph, conditions.vertices, conditions.initial)
    solution = parser.decode_data('{ "bypass": [] }')
    solution.bypass.append({conditions.initial: conditions.time})
    for i in range(1, len(min_route)):
        last_time = list(solution.bypass[-1].values())[0]
        solution.bypass.append({conditions.vertices[min_route[i]]:
                                calc_time(last_time, conditions.graph[min_route[i - 1]][min_route[i]])})
    solution.bypass.append({conditions.initial:
                            calc_time(list(solution.bypass[-1].values())[0],
                                      conditions.graph[min_route[-1]][min_route[0]])})
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
    min_length = float("Inf")
    min_route = None
    for each in permutations:
        current_route = [initial_index, *each]
        current_length = get_route_length(matrix, current_route)
        if min_length > current_length:
            min_length = current_length
            min_route = current_route
    return min_route


def get_route_length(matrix, vertices_to_visit):
    route_length = 0
    for i in range(len(vertices_to_visit) - 1):
        route_length = route_length + matrix[vertices_to_visit[i]][vertices_to_visit[i + 1]]
    return route_length + matrix[vertices_to_visit[-1]][vertices_to_visit[0]]
