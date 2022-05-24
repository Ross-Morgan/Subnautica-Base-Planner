import os
from typing import Callable, TypeVar

import attr
import yaml
from PyQt6 import QtCore, QtGui

T = TypeVar("T")


def _qsize(s: list):
    return QtCore.QSize(*s)


@attr.define(frozen=True)
class Config:
    size: QtCore.QSize = attr.field(converter=_qsize)
    title: str
    icon: QtGui.QIcon = attr.field(converter=QtGui.QIcon)


class Assets:
    roboto = "../assets/roboto-regular.ttf"

    class Images:
        backgrounds = [
            "../assets/images/biomes/sky.svg",
            "../assets/images/biomes/shallow.svg",
            "../assets/images/biomes/deep.svg",
            "../assets/images/biomes/river.svg",
            "../assets/images/biomes/lava.svg",
            "../assets/images/biomes/void.svg",
        ]

    class Scripts:
        main_window = "window.qss"
        slider = "slider.qss"
        depth = "depth.qss"
        spinbox = "spinbox.qss"


def check_wd(func: Callable):
    """
    Ensures cwd of file is in `src` folder
    """

    _change_wd = False

    os.chdir(".")

    print("changing cwd")

    def inner(*args, **kwargs):
        func(*args, **kwargs, change_wd=_change_wd)

    return inner


def load_config(file_path: str):
    """
    Loads configuration as a `dict` from a `.yaml` file

    Apply decorator to a function whose first positional argument
    is a config of type `dict`

    ## Example:
    ```
    @load_config("../config/config.yaml")
    def main(config: dict, ...):
        pass
    ```

    ---

    - @param file_path: str [ Path to .yaml configuration file]
    """

    config_data: dict = yaml.safe_load(open(file_path, "r"))

    def outer(func: Callable[[dict], None]):

        def inner():
            return func(config_data)
        return inner
    return outer


def modify_vars(cls: T, func: Callable, *types: type, f_args: tuple = None, f_kwargs: dict = None):  # noqa
    """
    Calls passed function on all user-defined members of a class

    - @param cls: T [ Class to modify ]
    - @param func: Callable [ Function to call of members ]
    - @param f_args: Any [ Positional arguments to pass to function ]
    - @param f_kwargs: Any [ Keyword arguments to pass to function ]
    """
    f_args = f_args or ()
    f_kwargs = f_kwargs or {}

    # Get all variables
    filtered_members = filter(lambda f: not f.startswith("__"), vars(cls))

    # Extract member names and values
    for member in filtered_members:
        attr = getattr(cls, member)
        if isinstance(attr, types):
            setattr(cls, member, func(attr, *f_args, **f_kwargs))


######


def load_script(path: str):
    return open(f"../assets/scripts/{path}", "r", encoding="utf-8").read()


def load_scripts(iterable: dict[str, str] | list[str]) -> list[T] | dict[T]:
    if isinstance(iterable, dict):
        modified_members = {}

        for member in iterable:
            modified_members[member] = load_script(modified_members[member])

    else:
        modified_members = []

        for member in iterable:
            modified_members.append(load_script(member))

    return modified_members


def load_assets():
    # Replace filepaths with script contents
    modify_vars(Assets.Scripts, load_script, str)
    modify_vars(Assets.Scripts, load_scripts, list, dict)
