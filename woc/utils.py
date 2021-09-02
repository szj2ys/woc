# *_*coding:utf-8 *_*
from __future__ import absolute_import, division, print_function
from os.path import dirname, abspath, join

# ROOT = dirname(dirname(abspath(__file__)))
from datetime import timedelta, datetime
import pandas as pd
import numpy as np
from tqdm import tqdm
import warnings
from doger import guru
from rich.console import Console
from rich.markdown import Markdown

loger = guru(level='DEBUG', name=__file__)
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


if __name__ == "__main__":
    starttime = (datetime.now() +
                 timedelta(days=-1)).strftime("%Y-%m-%d %H:%M:%S")
    str2date = datetime.strptime("2019-03-17 11:00:00", "%Y-%m-%d %H:%M:%S")
