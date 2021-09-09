#!/usr/bin/python3
# *_*coding:utf-8 *_*
import os
import sys
import subprocess
from datetime import datetime
from time import sleep
from tqdm import tqdm
from rich.progress import track
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from os.path import dirname, abspath, join

from woc.downloader import downloading
from woc.utils import render_markdown
import webbrowser

ROOT = dirname(abspath(__file__))
import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand

# CONSTANTS
CLICK_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
CLICK_CONTEXT_SETTINGS_NO_HELP = dict(help_option_names=[])


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
             context_settings=CLICK_CONTEXT_SETTINGS,
             help_headers_color='yellow',
             help_options_color='magenta',
             help_options_custom_colors={
                 'install': 'red',
                 'pip': 'cyan',
                 'pipenv': 'red',
                 'git': 'red',
                 'pypi': 'green',
                 'run': 'magenta',
                 'hexo': 'green',
                 'tree': 'cyan',
                 'docs': 'cyan',
                 'kit': 'magenta',
             })
@click.option('-v',
              '--version',
              is_flag=True,
              callback=print_version,
              expose_value=False,
              is_eager=True,
              help='Show version')
def cli():
    """\b
__    __ ____  ____
\ \/\/ // () \/ (__`
 \_/\_/ \____/\____)
"""


# http://patorjk.com/software/taag/#p=display&h=0&v=0&f=Graffiti&t=funlp


def time():
    layout = Layout()

    class Clock:
        """Renders the time in the center of the screen."""
        def __rich__(self) -> Text:
            return Text(datetime.now().ctime(),
                        style="bold magenta",
                        justify="center")

    layout.update(Clock())

    with Live(layout, screen=True, redirect_stderr=False) as live:
        try:
            while True:
                sleep(1)
        except KeyboardInterrupt:
            pass


@cli.command(context_settings=dict(ignore_unknown_options=True, ),
             cls=HelpColorsCommand,
             help_options_color='cyan',
             short_help='pipenv virtual environment pipeline')
@click.argument('do', nargs=1, required=True)
def pipenv(do):
    """Examples:

        \b
                create pipenv environment base current directory:
                    - woc pipenv c | create
                delete pipenv environment base current directory:
                    - woc pipenv d | delete
        """
    if do in ['c', 'create']:
        FILE = join(ROOT, 'scripts', 'create.sh')
        subprocess.run(f'bash {FILE}'.split())
    elif do in ['d', 'delete']:
        FILE = join(ROOT, 'scripts', 'delete.sh')
        subprocess.run(f'bash {FILE}'.split())
    else:
        click.secho(
            "I don't know what you're trying to do. Do you know what you're doing...",
            fg='red')


@cli.command(cls=HelpColorsCommand,
             help_options_color='cyan',
             help='render a beautiful tree with given path')
@click.argument('path', nargs=-1)
def tree(path):
    '''render a beautiful tree with given path'''
    FILE = join(ROOT, 'tree.py')
    DIR = path[0] if path else os.getcwd()
    subprocess.run(f'python3 {FILE} {DIR}'.split())


@cli.command(context_settings=dict(ignore_unknown_options=True, ),
             cls=HelpColorsCommand,
             help_options_color='cyan',
             short_help='install python package')
@click.argument('pkgs', nargs=-1, required=True)
@click.option('-y',
              '--yes',
              is_flag=True,
              show_default=True,
              help="whether to use pypi official source")
@click.option('-u',
              '--upgrade',
              is_flag=True,
              show_default=True,
              help="upgrade pip")
def pip(pkgs, yes, upgrade):
    """Examples:

    \b
            install packages use pypi:
                - woc pip fire just scrapy -y
            install requirements.txt:
                - woc pip requirements.txt
            install package and upgrade pip:
                - woc pip fire -u | -yu
    """
    args = sys.argv

    if set(args).intersection(['-yu', '-uy']):
        yes = upgrade = True

    if upgrade:
        subprocess.run('pip install --upgrade pip'.split())

    if pkgs[0] in ['requirements.txt', 'requirements-dev.txt']:
        file = pkgs[0]
        with open(file, 'r') as f:
            pkgs = [pkg.strip() for pkg in f.readlines()]
    pkgs = [
        pkg for pkg in pkgs
        if pkg not in ['-y', '--yes', '-u', '--upgrade', '-yu', '-uy']
    ]
    # for pkg in tqdm(pkgs):
    for pkg in track(pkgs, description=''):
        if yes:
            subprocess.run(
                f'pip3 install {pkg} -i https://pypi.org/simple'.split())
        else:
            subprocess.run(
                f'pip3 install {pkg} -i https://mirrors.aliyun.com/pypi/simple'
                .split())


@cli.command(cls=HelpColorsCommand,
             help_options_color='cyan',
             short_help='simplified git pipeline')
@click.argument('args', nargs=-1, required=True)
def git(args):
    """Examples:

    \b
            push changes to remote git repo:
                - woc git p | push
            remove all cached files from staging area:
                - woc git c | cache
            fix bug: fatal: Unable to create 'xxx/.git/index.lock':
                - woc git l | lock

    """
    args = sys.argv

    if set(args).intersection(['p', 'push', '-p', '--push']):
        FILE = join(ROOT, 'scripts', 'gitpush.sh')
        subprocess.run(f'bash {FILE}'.split())
    elif set(args).intersection(['l', 'lock', '-l', '--lock']):
        # fix bug: fatal: Unable to create 'xxx/.git/index.lock': File exists.
        subprocess.run('rm -f ./.git/index.lock'.split())
    elif set(args).intersection(['c', 'cache', '-c', '--cache']):
        subprocess.run('git rm -r --cache .'.split())
    else:
        click.secho(
            "I don't know what you're trying to do. Do you know what you're doing...",
            fg='red')


@cli.command(cls=HelpColorsCommand,
             help_options_color='cyan',
             short_help='hexo pipeline')
@click.argument('do', nargs=1, required=True)
# @click.option('-d',
#               '--deploy',
#               is_flag=True,
#               default=False,
#               help="deploy hexo blog")
def hexo(do):
    """Examples:

    \b
            deploy hexo blog:
                - woc hexo d | deploy
    """
    if do in ['d', 'deploy']:
        FILE = join(ROOT, 'scripts', 'deploy.sh')
        with Console().status("[bold green]"):
            subprocess.run(f'bash {FILE}'.split())
    else:
        click.secho(
            "I don't know what you're trying to do. Do you know what you're doing...",
            fg='red')


def alias():
    render_markdown(join(ROOT, 'resources', 'Alias.md'))


@cli.command(cls=HelpColorsCommand,
             help_options_color='cyan',
             short_help='show document')
@click.argument('which', nargs=1, required=False)
def docs(which):
    """👀Docs👀

    \b
        - git
        - keras
        - sklearn
        - pandas or pd
        - tensorflow or tf
        - pytorch or torch
        - markdown or md
    """
    if which == 'git':
        render_markdown(join(ROOT, 'resources', 'GitTutorials.md'))
    elif which in ['md', 'markdown']:
        webbrowser.open('https://www.songzhijun.com/posts/89757140/')
    elif which in ['pd', 'pandas']:
        webbrowser.open('https://pandas.pydata.org/docs/user_guide/')
    elif which in ['tf', 'tensorflow']:
        webbrowser.open('https://www.tensorflow.org/addons/api_docs/python/')
    elif which in ['torch', 'pytorch']:
        webbrowser.open('https://pytorch.org/tutorials/')
    elif which == 'keras':
        webbrowser.open('https://keras.io/examples/')
    elif which == 'sklearn':
        webbrowser.open('https://scikit-learn.org/stable/')
    else:
        webbrowser.open('https://www.songzhijun.com')


@cli.command(cls=HelpColorsCommand,
             help_options_color='cyan',
             short_help='install something useful')
@click.argument('pkg', nargs=1, required=True)
def install(pkg):
    """Supports:

    \b
            node | apt | brew
    """
    if pkg == 'node':
        if sys.platform.startswith('darwin'):
            with Console().status("[bold green]"):
                subprocess.run(f'brew install node'.split())
        elif sys.platform.startswith('win'):
            pass
        else:
            # https://developer.aliyun.com/article/760687
            # 先安装node包管理器nvm
            with Console().status("[bold green]install nvm..."):
                subprocess.run(
                    f'wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash'
                    .split())
                subprocess.run(f'export NVM_DIR="$HOME/.nvm"'.split())
            subprocess.run(f'nvm --version'.split())
            # 安装最新版node
            with Console().status("[bold green]install node..."):
                subprocess.run(f'nvm install node'.split())
    elif pkg == 'brew':
        os.system(
            '/bin/bash -c "$(curl -fsSL '
            'https://raw.githubusercontent.com/Homebrew/install/HEAD/install'
            '.sh)"')
    elif pkg == 'apt':
        FILE = join(ROOT, 'scripts', 'aptinstall.sh')
        with Console().status("[bold green]installing..."):
            subprocess.run(f'bash {FILE}'.split())
    else:
        click.secho(
            "I don't know what you're trying to do. Do you know what you're doing...",
            fg='red')


@cli.command(cls=HelpColorsCommand,
             help_options_color='cyan',
             short_help='toolkits...')
@click.argument('opt', nargs=1, required=True)
def kit(opt):
    """Examples:

    \b
            checkout ip address:
                - woc kit ip
            print time:
                - woc kit time
            server directory:
                - woc kit server
    """
    if opt == 'ip':
        os.system('ifconfig | grep "inet " | grep -v 127.0.0.1')
    elif opt == 'time':
        time()
    elif opt == 'server':
        os.system('python3 -m http.server --directory ./')
    else:
        click.secho(
            "I don't know what you're trying to do. Do you know what you're doing...",
            fg='red')


@cli.command(cls=HelpColorsCommand,
             help_options_color='cyan',
             short_help='config some environment')
@click.argument('opt', nargs=1, required=True)
def config(opt):
    """Examples:

    \b
            config jupyter notebook extensions and theme:
                - woc config jupyter | jp
            print frequent used alias:
                - woc config alias
    """
    if opt in ['jp', 'jupyter']:
        FILE = join(ROOT, 'scripts', 'setnotebook.sh')
        with Console().status("[bold green]configing jupyter..."):
            subprocess.run(f'bash {FILE}'.split())
    elif opt == 'alias':
        alias()
    else:
        click.secho(
            "I don't know what you're trying to do. Do you know what you're doing...",
            fg='red')


@cli.command(cls=HelpColorsCommand,
             help_options_color='cyan',
             short_help='manage pypi package')
@click.argument('args', nargs=-1, required=True)
def pypi(args):
    """Examples:

    \b
            publish package to pypi:
                - woc pypi p | publish
            clean pypi build output:
                - woc pypi c | clean
            combine activity chain:
                - woc pypi -pc
    """
    args = sys.argv
    CHAIN = False
    if set(args).intersection(['-pc', '-cp', 'pc', 'cp']):
        CHAIN = True

    if CHAIN:
        FILE = join(ROOT, 'scripts', 'publish.sh')
        subprocess.run(f'bash {FILE}'.split())
        FILE = join(ROOT, 'scripts', 'clean.sh')
        subprocess.run(f'bash {FILE}'.split())
    elif set(args).intersection(['p', 'publish', '-p', '--publish']):
        FILE = join(ROOT, 'scripts', 'publish.sh')
        subprocess.run(f'bash {FILE}'.split())
    elif set(args).intersection(['c', 'clean', '-c', '--clean']):
        FILE = join(ROOT, 'scripts', 'clean.sh')
        subprocess.run(f'bash {FILE}'.split())
    else:
        click.secho(
            "I don't know what you're trying to do. Do you know what you're doing...",
            fg='red')


@cli.command(cls=HelpColorsCommand,
             help_options_color='cyan',
             help='run python script')
def run():
    FILE = join(ROOT, 'scripts', 'run.sh')
    subprocess.run(f'bash {FILE}'.split())


@cli.command(cls=HelpColorsCommand,
             help_options_color='cyan',
             help='download url')
@click.argument('args', nargs=-1, required=True)
@click.option('-d',
              '--dir',
              default="./",
              show_default=True,
              help="upgrade pip")
def download(args, dir):
    downloading(args, dir)


def execute():
    try:
        cli(prog_name='woc')
    except Exception as e:
        pass


if __name__ == "__main__":
    execute()
