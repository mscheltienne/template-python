import ast
from importlib import import_module
from pathlib import Path

from mypy import stubgen

import template

# generate stub files, including private members and docstrings
directory = Path(template.__file__).parent
files = [
    str(file.as_posix())
    for file in directory.rglob("*.py")
    if file.parent.name not in ("commands", "tests")
    and file.name not in ("conftest.py", "_version.py")
]
stubgen.main(
    [
        "--no-analysis",
        "--no-import",
        "--include-private",
        "--include-docstrings",
        "--output",
        str(directory.parent),
        *files,
    ]
)
stubs = list(directory.rglob("*.pyi"))

# expand docstrings and inject into stub files
for stub in stubs:
    module_path = str(stub.relative_to(directory).with_suffix("").as_posix())
    module = import_module(f"{directory.name}.{module_path.replace('/', '.')}")
    module_ast = ast.parse(stub.read_text(encoding="utf-8"))
    objects = [
        node
        for node in module_ast.body
        if isinstance(node, (ast.ClassDef, ast.FunctionDef))
    ]
    for node in objects:
        docstring = getattr(module, node.name).__doc__
        if not docstring and isinstance(node, ast.FunctionDef):
            continue
        elif docstring:
            node.body[0].value.value = docstring
        for method in node.body:
            if not isinstance(method, ast.FunctionDef):
                continue
            docstring = getattr(getattr(module, node.name), method.name).__doc__
            if docstring:
                method.body[0].value.value = docstring
    unparsed = ast.unparse(module_ast)
    stub.write_text(unparsed, encoding="utf-8")
