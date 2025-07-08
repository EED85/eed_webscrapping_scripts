import functools
import pathlib


@functools.singledispatch
def file_exists(file_path) -> bool:
    """
    Check if a file exists at the given path.

    Parameters
    ----------
    file_path : str | pathlib.PosixPath | pathlib.WindowsPath
        The path to the file.

    Returns
    -------
    bool
        True if the file exists, False otherwise.
    """
    raise NotImplementedError(f"Unsupported type: {type(file_path)}")


@file_exists.register(str)
def _(file_path: str) -> bool:
    return pathlib.Path(file_path).is_file()


@file_exists.register(pathlib.PosixPath)
@file_exists.register(pathlib.WindowsPath)
def _(file_path: pathlib.WindowsPath | pathlib.PosixPath) -> bool:
    return file_path.is_file()
