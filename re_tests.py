import re
import os
import json

FILE_NAME = r"resources\temp"
FILE_LOG = "api.parkingwatcher.com.access.log"
SEARCH_PATTERN = r'\b[a-z]\b'


def get_path(file_name):
    return os.getcwd() + os.sep + 'resources' + os.sep + file_name


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


def dict_check(match_obj, dict_obj):
    if match_obj:
        if dict_obj.get(match_obj.group()) is None:
            dict_obj[match_obj.group()] = 0
        dict_obj[match_obj.group()] = dict_obj.get(match_obj.group()) + 1
    return dict_obj


def log_statistics(file_path):
    # search_pattern = r'\b(200|301)\b'
    search_code_response = r'\b[2-4][0-5][0-9]\b'
    search_agent = r'(?<=\().*(?=\))'
    result_code = dict()
    result_agent = dict()
    with open(file_path, 'r') as file:
        for line in file:
            match_code = re.search(search_code_response, line)
            match_agent = re.search(search_agent, line)
            result_code = dict_check(match_code, result_code)
            result_agent = dict_check(match_agent, result_agent)

    result_code = dict(sorted(result_code.items()))
    result_agent = dict(sorted(result_agent.items()))
    print(json.dumps(result_code, indent=4))
    print(json.dumps(result_agent, indent=4))


full_path = get_path(FILE_LOG)
log_statistics(full_path)
