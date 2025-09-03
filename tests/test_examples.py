import pytest
import importlib.util
from pathlib import Path


def get_python_files(directory):
    return [str(p) for p in list(Path(directory).rglob("*.py"))]


@pytest.mark.parametrize("py_file", get_python_files("/examples"))
def test_python_file_imports(py_file):
    spec = importlib.util.spec_from_file_location(Path(py_file).stem, py_file)
    module = importlib.util.module_from_spec(spec)

    # This will raise an exception if there are syntax/import errors
    spec.loader.exec_module(module)
