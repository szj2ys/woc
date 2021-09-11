# *_*coding:utf-8 *_*
from __future__ import absolute_import, division, print_function
from datetime import timedelta, datetime
import pandas as pd
import warnings
from rich.console import Console
from rich.markdown import Markdown
from woc.utils.decorator import decorator

warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
pd.set_option("display.max_columns", None)
# pd.set_option("display.max_rows", None)
pd.set_option("display.float_format", lambda x: "{:.2f}".format(x))


def render_markdown(file):
    console = Console()
    with open(file, 'r') as readme:
        markdown = Markdown(readme.read())
    console.print(markdown)


@decorator
def deprecated(func, *args, **kwargs):
    """ Marks a function as deprecated. """
    warnings.warn(
        f"{func} is deprecated and should no longer be used.",
        DeprecationWarning,
        stacklevel=3,
    )
    return func(*args, **kwargs)


def deprecated_option(option_name, message=""):
    """ Marks an option as deprecated. """
    def caller(func, *args, **kwargs):
        if option_name in kwargs:
            warnings.warn(
                f"{option_name} is deprecated. {message}",
                DeprecationWarning,
                stacklevel=3,
            )

        return func(*args, **kwargs)

    return decorator(caller)
