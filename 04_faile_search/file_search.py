import pathlib
from typing import Optional


def find_file(root_dir: pathlib.Path, file_name: str) -> Optional[str]:
    """
    Finds the file with the given name in the root directory and its subdirectories.

    Params:
    -------
    root_dir: pathlib.Path
        Root directory to start the search from.
    file_name: str
        Name of the file to search for.

    Returns:
    --------
    str
        Full path of the first occurrence of the file. If the file is not found, returns None.
    """
    for path in root_dir.glob('*'):
        if path.is_dir():
            found_file = find_file(path, file_name)
            if found_file:
                return found_file
        elif path.is_file() and path.name == file_name:
            return str(path)
    return None


if __name__ == '__main__':
    file_name = 'file_search.py'
    found_file = find_file(pathlib.Path.home(), file_name)
    if found_file:
        print(f'Found the file at: {found_file}')
    else:
        print(f'File "{file_name}" is not found.')
