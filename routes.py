import sys
import src.solver as solver


def main():
    if len(sys.argv) < 3:
        print('Error. Use "python routes.py <input_data_filename> <output_data_filename>"')
        return
    solver.solve_problem(*sys.argv[1:3])


if __name__ == "__main__":
    main()
