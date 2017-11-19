def reading_from_file(filename):
    with open(filename, "r") as file:
        return file.read()


def writing_in_the_file(filename, data):
    with open(filename, "w") as file:
        file.write(data)
