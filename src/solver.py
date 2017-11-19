import src.working_with_files as files
import src.parse_data as parser
import src.data_validation as validation
import src.littles_algorithm as algo


def solve_problem(input_file, output_file):
    try:
        conditions = init_data(input_file)
    except FileNotFoundError:
        print("Error - there is no such file: " + input_file)
        return
    except validation.ParsingDataError as e:
        print(e.what)
        return
    solution = calculate_solution(conditions)
    create_answer(output_file, solution)


def init_data(input_file):
    data = files.reading_from_file(input_file)
    validation.check_data(data)
    return parser.decode_data(data)


def calculate_solution(conditions):
    return conditions


def create_answer(output_file, solution):
    files.writing_in_the_file(output_file, parser.encode_data(solution))
