import os
root_path = "."

files_stack = []
files_stack.append(root_path)
files = []

while files_stack:
    path = files_stack[-1]
    dir_list = os.scandir(path)
    files_stack.pop()
    for file in dir_list:
        if file.is_dir():
            files_stack.append(f"{path}/{file.name}")
        elif file.is_file():
            if (file.name.split('.')[-1] == 'robot'):
                files.append(f"{path}/{file.name}")

# ---------------------------

class Keyword:
    def __init__(self, name=None):
        self.name = name
        self.sub_keywords = []
        self.definition_location = []


def extract_keywords_from_robot_file(file_path):
    robot_file_keywords = {}
    file = open(file_path, "r")
    file_content = file.read()
    keywords_section = (file_content.split("*** Keywords ***")
                        [1].split("*** Test Cases ***")[0])
    lines_in_keywords_section = keywords_section.split('\n')

    keyword_temp = Keyword()
    keyword_temp.definition_location.append(file_path)
    for line in lines_in_keywords_section:
        if (line):
            if (line[0] != " " and  line[0] != "#" ):  # keyword
                if (keyword_temp.name):
                    robot_file_keywords[keyword_temp.name] = keyword_temp
                    keyword_temp = Keyword()
                    keyword_temp.definition_location.append(file_path)
                keyword_temp.name = line
            else:
                # format line
                formated_line = line.strip().split("  ")[0]
                if (formated_line[0] == '['):
                    continue

                robot_file_keywords[formated_line] = Keyword(
                    name=formated_line)
                keyword_temp.sub_keywords.append(formated_line)

    if (keyword_temp.name):
        robot_file_keywords[keyword_temp.name] = keyword_temp

    return robot_file_keywords


keywords = {}

# ------------------------
for file_path in files:
    # print (file)
    extracted_keywords = extract_keywords_from_robot_file(file_path)
    for extracted_keyword in extracted_keywords:
        if (extracted_keyword in keywords):
            keywords[extracted_keyword].definition_location.extend( extracted_keywords[extracted_keyword].definition_location  )
        else:
            keywords[extracted_keyword] = extracted_keywords[extracted_keyword]


# view
print_sub_keywords = False
for keyword_iter in keywords:
    if (keywords[keyword_iter].name and keywords[keyword_iter].definition_location):
        print(f"- {keywords[keyword_iter].name}")
        for location in keywords[keyword_iter].definition_location :
            print ( f"      --- defined in {location}" )

    if (print_sub_keywords and keywords[keyword_iter].sub_keywords):
        for sub_keyword in keywords[keyword_iter].sub_keywords:
            print(
                f"---   {sub_keyword.name}")
