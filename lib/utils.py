import ast
import inspect
import os
from pathlib import Path

import requests

from lib.qlogging import QuantumLogger

logger = QuantumLogger("utils")
path = os.path.dirname(os.path.abspath(__file__))


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
    fp = os.path.join(path, f"./../data/app_data/{file}")
    with open(fp) as data_file:
        data_file.seek(0, 0)
        for cnt, line in enumerate(data_file):
            logger.debug(f"{cnt}: Checking for {search_term} inside {file}:{line}")
            if search_term == line:
                data_file.close()
                logger.debug(f"{cnt}: Found {search_term} inside {file}:{line}")
                return True
        data_file.close()
        logger.debug(f"Could not find {search_term} in {file}")
        return False


def append_string_in_file(file: str, appended_string: str):
    fp = os.path.join(path, f"./../data/app_data/{file}")
    with open(fp, "a") as data_file:
        data_file.seek(0, 2)
        data_file.writelines(appended_string)
        data_file.flush()
        data_file.close()
        logger.debug(f"{appended_string} added to {file} in /data/app_data")


def split_string(str, limit, sep=" "):
    # do not use this shit.
    words = str.split(" ")
    result, part = [], ""
    for word in words:
        if len(sep) + len(word) > limit:
            for i in range(0, len(word), limit):
                if len(sep) + len(word[i:i + limit]) > limit - len(part):
                    if part:
                        result.append(part)
                        part = ""
                    result.append(word[i:i + limit])
                else:
                    part += sep + word[i:i + limit]
        elif len(sep) + len(word) > limit - len(part):
            result.append(part)
            part = sep + word
        else:
            part += sep + word
    if part != "":
        result.append(part)
    return result


def get_latest_sha1():
    """Retrieves the latest commit sha1"""
    req = requests.get("https://api.github.com/repos/JohnRipper/quantum/commits")
    if req.status_code == 200:
        # like github
        sha1 = req.json()[0]["sha"][:7]
        return(sha1)


def get_current_sha1():
    """Reads .git/refs/heads/master for the current commit"""
    cwd = Path.cwd()
    # pathlib uses __divmod__ for path joining, HOHOHHO
    headfile = Path(cwd / ".git/refs/heads/master")
    sha1 = headfile.read_text()[:7]
    return(sha1)
