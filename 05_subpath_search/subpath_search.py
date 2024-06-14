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
    dir_content = list(root_dir.glob('*'))

    next_dir_index_list = [i for i, v in enumerate(dir_content) if v.name == subpath[0]]
    if len(next_dir_index_list) > 0:
        next_dir_index = next_dir_index_list[0]
        dir_content.pop(next_dir_index)
        dir_content = [root_dir / subpath[0]] + dir_content

    for path in dir_content:
        if len(subpath) == 1:
            if path.is_file():
                if path.name == subpath[0]:
                    return str(path)
        else:
            if path.is_dir():
                found_file = find_subpath(path, subpath[1:])
                if found_file:
                    return found_file
                found_file = find_subpath(path, subpath)
                if found_file:
                    return found_file
    return None


if __name__ == '__main__':
    subpath = ['b', 'a', 'r', 'b', 'a', 'r', 'a', 'file.txt']
    found_file = find_subpath(pathlib.Path.home(), subpath)
    if found_file:
        print(f'Found the file at: {found_file}')
    else:
        print(f'Subpath "{subpath}" is not found.')
