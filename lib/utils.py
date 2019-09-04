import ast
import inspect
import os

import requests

from lib.qlogging import QuantumLogger

logger = QuantumLogger("utils")

def get_decorators(cls):
    target = cls
    decorators = {}

    def visit_FunctionDef(node):
        decorators[node.name] = []
        for n in node.decorator_list:
            name = ''
            if isinstance(n, ast.Call):
                name = n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id
            else:
                name = n.attr if isinstance(n, ast.Attribute) else n.id

            decorators[node.name].append(name)

    node_iter = ast.NodeVisitor()
    node_iter.visit_FunctionDef = visit_FunctionDef
    node_iter.visit(ast.parse(inspect.getsource(target)))
    return decorators


def string_in_file(file: str, search_term: str):
    with open(f"./../data/app_data/{file}") as data_file:
        data_file.seek(0, 0)
        for cnt, line in enumerate(data_file):
            logger.debug(f"{cnt}: Checking for {search_term} inside {file}:{line}")
            if search_term == line:
                data_file.close()
                logger.debug(f"{cnt}: Found {search_term} inside {file}:{line}")
                return True
        logger.debug(f"Not found")
        data_file.close()
        return False


def append_string_in_file(file: str, appended_string: str):
    with open(f"./../data/app_data/{file}", "a") as data_file:
        data_file.seek(0, 2)
        data_file.writelines(appended_string)
        data_file.flush()
        logger.debug(f"{appended_string} added to {file} in /data/app_data")
        data_file.close()

def get_commit_sha1():
    req = requests.get("https://api.github.com/repos/JohnRipper/quantum/commits")
    if req.status_code == 200:
        # like github
        sha = req.json()[0]["sha"][:7]
        return(sha)

