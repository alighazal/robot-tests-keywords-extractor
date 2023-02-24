import os

class Keyword:
    def __init__(self, name=None):
        self.name = name
        self.sub_keywords = []
        self.definition_location = []
        self.definitions = {}


def traverse_folder(root_path):
    files = []
    files_stack = []
    files_stack.append(root_path)
    while files_stack:
        path = files_stack[-1]
        dir_list = os.scandir(path)
        files_stack.pop()
        for file in dir_list:
            if file.is_dir():
                files_stack.append(f"{path}/{file.name}")
            elif file.is_file():
                if file.name.split(".")[-1] == "robot":
                    files.append(f"{path}/{file.name}")

    return files


# ---------------------------


def extract_keywords_from_robot_file(file_path):
    try:
        robot_file_keywords = {}
        file = open(file_path, "r")
        file_content = file.read()
        keywords_section = file_content.split("*** Keywords ***")[1].split("*** Test Cases ***")[0]
        lines_in_keywords_section = keywords_section.split("\n")
        # print(lines_in_keywords_section)

        keyword_temp = Keyword()
        keyword_temp.definition_location.append(file_path)
        for line in lines_in_keywords_section:
            if line:
                if line[0] != " " and line[0] != "#" and line.strip()[0] != "$":  # keyword
                    if keyword_temp.name:
                        robot_file_keywords[keyword_temp.name] = keyword_temp
                        keyword_temp = Keyword()
                        keyword_temp.definition_location.append(file_path)
                    keyword_temp.name = line
                else:
                    # format line
                    formated_line = line.strip()
                    if formated_line[0] == "[":
                        continue
                    if file_path in keyword_temp.definitions:
                        keyword_temp.definitions[file_path].append(formated_line)
                    else:
                        keyword_temp.definitions[file_path] = [formated_line]

                    keyword_temp.sub_keywords.append(Keyword(name=formated_line))

        if keyword_temp.name:
            robot_file_keywords[keyword_temp.name] = keyword_temp
    except Exception:
        print(f"Can't parse {file_path}")

    return robot_file_keywords


# --------------------


def print_keywords(keywords, allow_print_definition_details=False):
    for keyword_iter in keywords:
        if keywords[keyword_iter].name:
            print(f"== {keywords[keyword_iter].name}")
            for definition in keywords[keyword_iter].definitions:
                print(f"    {definition}")
                if allow_print_definition_details:
                    for line in keywords[keyword_iter].definitions[definition]:
                        print(f"        {line}")


# --------------------


sct_root_path = "."

files_in_sct_dir = traverse_folder(sct_root_path)
keywords = {}

for sct_file in files_in_sct_dir:
    extracted_keywords = extract_keywords_from_robot_file(sct_file)
    for extracted_keyword in extracted_keywords:
        if extracted_keyword in keywords:
            keywords[extracted_keyword].definition_location.extend(
                extracted_keywords[extracted_keyword].definition_location
            )
            keywords[extracted_keyword].definitions.update(
                extracted_keywords[extracted_keyword].definitions
            )

        else:
            keywords[extracted_keyword] = extracted_keywords[extracted_keyword]

print_keywords(keywords)
