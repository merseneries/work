import re
import os

FILE_NAME = r"resources\temp"
SEARCH_PATTERN = r'\b[a-z]\b'


def get_path(file_name):
    return os.getcwd() + os.sep + FILE_NAME


def fun_search(file_path, pattern):
    result = "fun_search result:\n"
    with open(file_path, "r") as file:
        for line in file:
            match_result = re.search(pattern, line, flags=re.IGNORECASE)
            if match_result:
                result += "  Letter: " + match_result.group() + " Indexes: " + str(match_result.span()) + "\n"
    return result


def fun_search_all(file_path, pattern):
    result = "fun_search_all result:\n"
    with open(file_path, "r") as file:
        for index, line in enumerate(file, 1):
            match_result = re.compile(pattern, flags=re.IGNORECASE)
            for element in match_result.finditer(line):
                result += " Row #" + str(index) + " Letter: " + element.group() + " Index: " + str(
                    element.start()) + "\n"
    return result


print(fun_search(get_path(FILE_NAME), SEARCH_PATTERN))
print(fun_search_all(get_path(FILE_NAME), SEARCH_PATTERN))
