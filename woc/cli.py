#!/usr/bin/python3
# *_*coding:utf-8 *_*
import os
import sys
import subprocess
from tqdm import tqdm
from rich.progress import track
from os.path import dirname, abspath, join
from woc.utils import render_markdown
import webbrowser

ROOT = dirname(abspath(__file__))
import click
from click_help_colors import HelpColorsGroup


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    package_conf = {}
    with open(join(ROOT, "__version__.py")) as f:
        exec(f.read(), package_conf)
    # click.secho(package_conf['__version__'], fg='green')
    click.secho(package_conf['__version__'], blink=True, bold=True)
    ctx.exit()


# http://patorjk.com/software/taag/#p=display&f=Graffiti&t=hello
@click.group(chain=True,
             cls=HelpColorsGroup,
             help_headers_color='yellow',
             help_options_color='magenta',
             help_options_custom_colors={
                 'up': 'cyan',
                 'push': 'cyan',
                 'undo': 'red',
                 'unstage': 'red',
                 'revert': 'red',
                 'diff': 'green',
                 'branch': 'green',
                 'add': 'blue',
                 'commit': 'blue',
                 'save': 'blue',
             })
@click.option('-v',
              '--version',
              is_flag=True,
              callback=print_version,
              expose_value=False,
              is_eager=True)
def cli():
    """\b
__    __ ____  ____
\ \/\/ // () \/ (__`
 \_/\_/ \____/\____)
"""


# http://patorjk.com/software/taag/#p=display&h=0&v=0&f=Graffiti&t=funlp


@cli.command(help='clean useless path and file')
def clean():
    FILE = join(ROOT, 'scripts', 'clean.sh')
    subprocess.run(f'bash {FILE}'.split())


@cli.command(short_help='pipenv virtual environment pipline')
@click.option('-c',
              '--create',
              is_flag=True,
              default=False,
              help="create pipenv environment base current directory")
@click.option('-d',
              '--delete',
              is_flag=True,
              default=False,
              help="delete pipenv environment base current directory")
def pipenv(create, delete):
    if create:
        FILE = join(ROOT, 'scripts', 'create.sh')
        subprocess.run(f'bash {FILE}'.split())
    elif delete:
        FILE = join(ROOT, 'scripts', 'delete.sh')
        subprocess.run(f'bash {FILE}'.split())
    else:
        click.secho('No pipline, please checkout your command...', fg='red')


@cli.command(help='render a beautiful tree with given path')
@click.argument('path', nargs=-1)
def tree(path):
    FILE = join(ROOT, 'tree.py')
    DIR = path[0] if path else os.getcwd()
    subprocess.run(f'python3 {FILE} {DIR}'.split())


@cli.command(short_help='install python package')
@click.argument('pkgs', nargs=-1, required=True)
@click.option('-y',
              '--yes',
              is_flag=True,
              default=False,
              show_default=True,
              help="whether to use pypi official source")
def pip(pkgs, yes):
    """Examples:

    \b
            install packages use pypi:
                - woc pip fire just scrapy -y
            install requirements.txt:
                - woc pip requirements.txt
    """

    if pkgs[0] in ['requirements.txt', 'requirements-dev.txt']:
        file = pkgs[0]
        with open(file, 'r') as f:
            pkgs = [pkg.strip() for pkg in f.readlines()]

    for pkg in track(pkgs):
        # for pkg in tqdm(pkgs):
        if yes:
            subprocess.run(f'pip3 install {pkg}'.split())
        else:
            subprocess.run(
                f'pip3 install {pkg} -i https://mirrors.aliyun.com/pypi/simple'
                .split())


@cli.command(short_help='simplified git pipline')
@click.argument('do', nargs=1, required=True)
def git(do):
    """Examples:

    \b
            push changes to remote git repo:
                - woc git p | push
            remove all cached files from staging area:
                - woc git c | cache

    """
    if do == 'push' or do == 'p':
        subprocess.run(f"bash {join(ROOT, 'scripts', 'gitpush.sh')}".split())
    elif do == 'cache' or do == 'c':
        subprocess.run('git rm -r --cache .'.split())


@cli.command(help='deploy hexo blog')
def hexod():
    FILE = join(ROOT, 'scripts', 'deploy.sh')
    subprocess.run(f'bash {FILE}'.split())


@cli.command(help='print alias')
def alias():
    render_markdown(join(ROOT, 'resources', 'Alias.md'))


@cli.command(short_help='show document')
@click.argument('which', nargs=1, required=True)
def docs(which):
    """👀Docs👀

    \b
    git
    keras
    sklearn
    pandas or pd
    tensorflow or tf
    pytorch or torch
    """
    if which == 'git':
        render_markdown(join(ROOT, 'resources', 'GitTutorials.md'))
    elif which == 'pandas' or which == 'pd':
        webbrowser.open('https://pandas.pydata.org/docs/user_guide/')
    elif which == 'tensorflow' or which == 'tf':
        webbrowser.open('https://www.tensorflow.org/addons/api_docs/python/')
    elif which == 'pytorch' or which == 'torch':
        webbrowser.open('https://pytorch.org/tutorials/')
    elif which == 'keras':
        webbrowser.open('https://keras.io/examples/')
    elif which == 'sklearn':
        webbrowser.open('https://scikit-learn.org/stable/')


@cli.command(short_help='install something useful')
@click.argument('pkg', nargs=1, required=True)
def install(pkg):
    """Examples:

    \b
            install nodejs:
                - woc install node
            install frequently-used linux packages through apt-get:
                - woc install apt
    """
    if pkg == 'node':
        if sys.platform.startswith('darwin'):
            subprocess.run(f'brew install node'.split())
        elif sys.platform.startswith('win'):
            pass
        else:
            # https://developer.aliyun.com/article/760687
            # 先安装node包管理器nvm
            subprocess.run(
                f'wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash'
                .split())
            subprocess.run(f'export NVM_DIR="$HOME/.nvm"'.split())
            subprocess.run(f'nvm --version'.split())
            # 安装最新版node
            subprocess.run(f'nvm install node'.split())
    elif pkg == 'apt':
        FILE = join(ROOT, 'scripts', 'aptinstall.sh')
        subprocess.run(f'bash {FILE}'.split())


@cli.command(help='config jupyter notebook extension and theme')
def configjupyter():
    FILE = join(ROOT, 'scripts', 'setnotebook.sh')
    subprocess.run(f'bash {FILE}'.split())


@cli.command(help='publish present package to pypi')
def publish():
    FILE = join(ROOT, 'scripts', 'publish.sh')
    subprocess.run(f'bash {FILE}'.split())


@cli.command(help='run python script')
def run():
    FILE = join(ROOT, 'scripts', 'run.sh')
    subprocess.run(f'bash {FILE}'.split())


def execute():
    try:
        cli(prog_name='woc')
    except Exception as e:
        pass


if __name__ == "__main__":
    execute()
