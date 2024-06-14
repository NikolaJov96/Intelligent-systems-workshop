import pathlib
from typing import List, Optional


def find_subpath(root_dir: pathlib.Path, subpath: List[str]) -> Optional[str]:
    """
    Finds the whole subpath in the root directory and its subdirectories.

    Params:
    -------
    root_dir: str
        Root directory to start the search from.
    subpath: List[str]
        List of directory names ending with the file name to search for.

    Returns:
    --------
    str
        Full path of the first occurrence of the file. If the file is not found, returns None.
    """
    pass


if __name__ == '__main__':
    subpath = ['b', 'a', 'r', 'b', 'a', 'r', 'a', 'file.txt']
    found_file = find_subpath(pathlib.Path.home(), subpath)
    if found_file:
        print(f'Found the file at: {found_file}')
    else:
        print(f'Subpath "{subpath}" is not found.')
