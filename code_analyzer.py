import itertools
import os
import sys
import re
import ast


def length_restriction_s001(string_01):
    """Check the length of the strings. The restriction is 79 chars"""
    lr = 79
    if len(string_01) > lr:
        return True
    else:
        return False


def indentantion_s002(string_02):
    ii = 0
    if string_02 and string_02.strip():
        while string_02[ii] == " ":
            ii += 1
        if ii % 4 != 0:
            return True
        else:
            return False
    else:
        return False


def semicolon_s003(string_03):
    if string_03 and string_03.strip():
        if '#' in string_03:
            if string_03.strip()[0] != "#":
                str_working = string_03[:string_03.index('#')].strip()
            else:
                return False
        else:
            str_working = string_03.strip()
        if str_working[len(str_working.strip()) - 1] == ';':
            return True
    else:
        return False


def inline_comments_s004(string_04):
    if string_04 and string_04.strip():
        if "#" in string_04:
            if string_04.strip()[0] != "#":
                ind = string_04.index("#")
                if string_04[ind - 1] + string_04[ind - 2] != "  ":
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


def todo_found_s005(string_05):
    ls = list(map(''.join, itertools.product(*zip('todo'.upper(), 'todo'.lower()))))
    count = 0
    if "#" in string_05:
        for jj in ls:
            if jj in string_05:
                count += 1
    else:
        return False
    if count > 0:
        return True


def blank_line_s006(string_06) -> 'Check if string is empty or contain spaces only':
    """Check if string is empty or contain spaces only"""
    if string_06 and string_06.strip():
        return False
    else:
        return True


def files_list_sorted(path) -> "return sorted list":
    dir_list = []
    if os.path.isfile(path):
        dir_list.append(os.path.relpath(path))
    else:
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.name[-2:] == "py":
                    dir_list.append(os.path.relpath(entry))
    dir_list.sort()
    return dir_list


def spaces_after_construction_s007(string_07) -> "check the number of spaces after a function or class":
    if re.match(r'^class {2,}', string_07.strip()):
        return 'class'
    elif re.match(r'^def {2,}', string_07.strip()):
        return 'def'
    else:
        return False


def camel_case_s008(string_08):
    if re.match(r'^class', string_08.strip()):
        checking_string = string_08.strip()[len('class'):].strip().strip(":")
        if re.match(r'[A-Z][a-z]*[A-Z]*[a-z]*\b', checking_string):
            return False
        else:
            return True, checking_string


def sc_function_s009(string_09):
    if re.match(r'^def', string_09.strip()):
        checking_string = string_09.strip()[len('def'):string_09.strip().index('(')].strip().strip(":")
        return snake_case_checking(checking_string)


def file_pep8_checking(python_file: "file object", file: "path to file", args_ast: "ast arg dictionary")\
        -> 'Checks all conditions':
    k = 0
    file_relative_path = os.path.relpath(file)
    blank_line_limit = 2
    count_blank_lines = 0
    messages_error = {
        1: "S001 Too long",
        2: "S002 Indentation is not a multiple of four",
        3: "S003 Unnecessary semicolon",
        4: "S004 At least two spaces required before inline comments",
        5: "S005 TODO found",
        6: "S006 More than two blank lines used before this line",
        7: "S007 Too many spaces after",
        8: "should use CamelCase",
        9: "should use snake_case",
        10: "should be written in snake_case",
        11: "should be written in snake_case",
        12: "S012 The default argument value is mutable"
    }
    for i in python_file.readlines():
        k += 1
        if length_restriction_s001(i):
            print(f'{file_relative_path}: Line {k}: {messages_error[1]}')
        if indentantion_s002(i):
            print(f'{file_relative_path}: Line {k}: {messages_error[2]}')
        if semicolon_s003(i):
            print(f'{file_relative_path}: Line {k}: {messages_error[3]}')
        if inline_comments_s004(i):
            print(f'{file_relative_path}: Line {k}: {messages_error[4]}')
        if todo_found_s005(i):
            print(f'{file_relative_path}: Line {k}: {messages_error[5]}')
        if blank_line_s006(i):
            count_blank_lines += 1  # counter turn on
        if blank_line_s006(i) is False:
            count_blank_lines = 0  # nulify counter
        if count_blank_lines > blank_line_limit:
            print(f'{os.path.relpath(file)}: Line {k+1}: {messages_error[6]}')
            count_blank_lines = 0  # dismiss counter after an error
        if spaces_after_construction_s007(i):
            (print(f'{file_relative_path}: Line {k}: {messages_error[7]} '
                   f'{spaces_after_construction_s007(i)}'))
        if camel_case_s008(i):
            (print(f'{file_relative_path}: Line {k}: S008 Class name '
                   f'"{camel_case_s008(i)[1]}" {messages_error[8]}'))
        if sc_function_s009(i):
            (print(f'{file_relative_path}: Line {k}: S009 Function name '
                   f'"{sc_function_s009(i)[1]}" {messages_error[9]}'))
        if k in args_ast[0]:  # check s010 condition
            (print(f'{file_relative_path}: Line {k}: S010 Argument name '
                   f'"{args_ast[0][k]}" {messages_error[10]}'))
        if k in args_ast[1]:  # check s011 condition
            (print(f'{file_relative_path}: Line {k}: S011 Variable '
                   f'"{args_ast[1][k]}" {messages_error[11]}'))
        if k in args_ast[2]:  # check s012 condition
            print(f'{file_relative_path}: Line {k}: {messages_error[12]}')


def snake_case_checking(string: str)\
        -> 'checks if the string conform to the snake case pattern':
    if re.match(r'^[a-z0-9_]+\b', string):
        return False
    else:
        return True, string


def arguments_ast_list_s010(file: "file object")\
        -> 'return a dictionary of lines where args[0] and variables[1] not in snake_case':
    tree1 = ast.parse((file.read()))
    args_not_passed = {}
    vars_not_passed = {}
    def_args_not_passed = {}
    for j in ast.walk(tree1):
        if isinstance(j, ast.arg):
            argument = j.arg
            num = j.lineno
            if snake_case_checking(argument):
                new_entry = {num: argument}
                args_not_passed.update(new_entry)
        elif isinstance(j, ast.Name):
            if isinstance(j.ctx, ast.Store):
                num_var = j.lineno
                num_id = j.id
                if snake_case_checking(num_id):
                    new_entry_var = {num_var: num_id}
                    vars_not_passed.update(new_entry_var)
        elif isinstance(j, ast.FunctionDef):
            num = j.lineno
            for item in j.args.defaults:
                if isinstance(item, ast.List):
                    new = {num: ast.dump(item)}
                    def_args_not_passed.update(new)

    return args_not_passed, vars_not_passed, def_args_not_passed


if __name__ == '__main__':

    args = sys.argv
    dir_path = args[1]
    check_list = files_list_sorted(dir_path)  # compiling a list of files to check
    for n in check_list:
        with open(n, 'r') as ast_check:
            ast_dict_args = arguments_ast_list_s010(ast_check)
        check_file = open(n, 'r')
        file_pep8_checking(check_file, n, ast_dict_args)
        check_file.close()
