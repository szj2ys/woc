#!/usr/bin/python3
# *_*coding:utf-8 *_*
import os
import sys
import subprocess
import traceback
from datetime import datetime
from pathlib import Path
from tqdm import tqdm
from rich.progress import track
from rich.console import Console
from os.path import dirname, abspath, join, basename, splitext

from woc.downloader import downloading
try:
    from woc.math2latex import py2tex
    from woc.helpers import render_markdown, redirect, get_pure_filename
except:
    from .math2latex import py2tex
    from .helpers import render_markdown
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
██╗    ██╗ ██████╗  ██████╗
██║    ██║██╔═══██╗██╔════╝
██║ █╗ ██║██║   ██║██║
██║███╗██║██║   ██║██║
╚███╔███╔╝╚██████╔╝╚██████╗
 ╚══╝╚══╝  ╚═════╝  ╚═════╝
    """


# https://manytools.org/hacker-tools/ascii-banner/


@cli.command(context_settings=dict(ignore_unknown_options=True, ),
             cls=HelpColorsCommand,
             help_options_color='cyan',
             short_help='pipenv virtual environment pipeline')
@click.option('-c',
              '--create',
              is_flag=True,
              help="create pipenv environment base current directory")
@click.option('-d',
              '--delete',
              is_flag=True,
              help="delete pipenv environment base current directory")
def pipenv(create, delete):
    """Examples:

        \b
                create pipenv environment base current directory:
                    - woc pipenv -c | --create
                delete pipenv environment base current directory:
                    - woc pipenv -d | --delete
        """
    CHECK_PIPENV = os.system('pipenv --venv')
    if CHECK_PIPENV == 0:
        # exist pipenv environment
        pass
    if create:
        FILE = join(ROOT, 'scripts', 'create.sh')
        subprocess.run(f'bash {FILE}'.split())
    if delete:
        FILE = join(ROOT, 'scripts', 'delete.sh')
        subprocess.run(f'bash {FILE}'.split())
    if not (create or delete):
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
@click.option('-a',
              '--ali',
              is_flag=True,
              show_default=True,
              help="use aliyun pypi source")
@click.option('-d',
              '--douban',
              is_flag=True,
              show_default=True,
              help="use douban pypi source")
@click.option('-H',
              '--hide',
              is_flag=True,
              show_default=True,
              help="hide message on terminal")
@click.option('-v',
              '--virtualenv',
              is_flag=True,
              show_default=True,
              help="install package in pipenv virtualenv")
@click.option('-u',
              '--upgrade',
              is_flag=True,
              show_default=True,
              help="upgrade package")
def pip(pkgs, ali, douban, upgrade, hide, virtualenv):
    if upgrade:
        UPGRADE = '--upgrade'
    else:
        UPGRADE = ''

    if pkgs[0] in ['requirements.txt', 'requirements-dev.txt']:
        file = pkgs[0]
        with open(file, 'r') as f:
            pkgs = [pkg.strip() for pkg in f.readlines() if len(pkg) > 0]
    pkgs = [pkg for pkg in pkgs if not str(pkg).__contains__('-')]

    REDIRECT_SEG = redirect(hide)

    if virtualenv:
        # pipenv path
        PIPENV = subprocess.getoutput('pipenv --venv')
        PIP = PIPENV + '/bin/pip'
    else:
        PIP = 'pip3'

    # trying to upgrade pip first
    os.system(
        f'{PIP} install pip --upgrade -i https://mirrors.aliyun.com/pypi/simple'
        f' {REDIRECT_SEG}')

    # for pkg in tqdm(pkgs):
    for pkg in track(pkgs, description=''):
        if ali:
            os.system(f'{PIP} install {pkg} {UPGRADE} -i '
                      f'https://mirrors.aliyun.com/pypi/simple {REDIRECT_SEG}')
        elif douban:
            os.system(
                f'{PIP} install {pkg} {UPGRADE} -i https://pypi.douban.com/simple'
                f' {REDIRECT_SEG}')
        else:
            os.system(
                f'{PIP} install {pkg} {UPGRADE} -i https://pypi.org/simple {REDIRECT_SEG}'
            )


@cli.command(cls=HelpColorsCommand,
             help_options_color='cyan',
             short_help='simplified git pipeline')
@click.option('-p', '--push', is_flag=True, help='push change to remote')
@click.option('-m', '--msg', help='message')
@click.option('-doc', '--doc', is_flag=True, help='show git tutorials')
@click.option('-c', '--cache', is_flag=True, help='remove cached files')
@click.option('-l', '--lock', is_flag=True, help='remove index.lock')
@click.option('-t', '--tag', help='git tag')
def git(push, msg, cache, lock, tag, doc):

    if push:
        if not msg:
            # If no massage is given, to use the current time instead
            msg = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        os.system(f'yapf -irp .;git add . --all;git commit -m "'
                  f'{msg}";git push')

    if lock:
        # fix bug: fatal: Unable to create 'xxx/.git/index.lock': File exists.
        subprocess.run('rm -f ./.git/index.lock'.split())
    if cache:
        subprocess.run('git rm -r --cache .'.split())

    if tag:
        COMMAND = f'''git tag --annotate "{tag}" --message "{msg if msg else tag}"'''
        os.system(COMMAND)

    if doc:
        render_markdown(join(ROOT, 'resources', 'GitTutorials.md'))


@cli.command(cls=HelpColorsCommand,
             help_options_color='cyan',
             short_help='hexo pipeline')
@click.option('-d', '--deploy', is_flag=True, help='deploy hexo blog')
def hexo(deploy):
    if deploy:
        FILE = join(ROOT, 'scripts', 'deploy.sh')
        with Console().status("[bold green]"):
            subprocess.run(f'bash {FILE}'.split())
    else:
        click.secho(
            "I don't know what you're trying to do. Do you know what you're doing...",
            fg='red')


def render_alias():
    render_markdown(join(ROOT, 'resources', 'Alias.md'))


@cli.command(cls=HelpColorsCommand,
             help_options_color='cyan',
             short_help='show document')
@click.option('-kr', '--keras', is_flag=True, help="show keras doc")
@click.option('-sl', '--sklearn', is_flag=True, help="show sklearn doc")
@click.option('-pd', '--pandas', is_flag=True, help="show pandas doc")
@click.option('-tf', '--tensorflow', is_flag=True, help="show tensorflow doc")
@click.option('-tc', '--torch', is_flag=True, help="show pytorch doc")
@click.option('-md', '--markdown', is_flag=True, help="show markdown doc")
@click.option('-py', '--python', is_flag=True, help="show python doc")
@click.option('-pl', '--plotly', is_flag=True, help="show plotly doc")
@click.option('-ple',
              '--plotly_express',
              is_flag=True,
              help="show plotly "
              "express doc")
def docs(markdown, torch, tensorflow, pandas, sklearn, keras, python, plotly,
         plotly_express):
    """👀Documents👀"""
    if markdown:
        webbrowser.open('https://www.songzhijun.com/posts/89757140/')
    if pandas:
        webbrowser.open('https://pandas.pydata.org/docs/user_guide/')
    if tensorflow:
        webbrowser.open('https://www.tensorflow.org/addons/api_docs/python/')
    if torch:
        webbrowser.open('https://pytorch.org/tutorials/')
    if keras:
        webbrowser.open('https://keras.io/examples/')
    if sklearn:
        webbrowser.open('https://scikit-learn.org/stable/')
    if python:
        webbrowser.open('https://docs.python.org/3/')
    if plotly:
        webbrowser.open('https://plotly.com/python/plotly-fundamentals/')
    if plotly_express:
        webbrowser.open('https://plotly.com/python/plotly-express/#')

    # webbrowser.open('https://www.songzhijun.com')


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
@click.option('-ip', '--ip', is_flag=True, help='checkout ip address')
@click.option('-serv',
              '--server',
              is_flag=True,
              help='server directory to browser')
def kit(ip, server):
    if ip:
        os.system('ifconfig | grep "inet " | grep -v 127.0.0.1')
    if server:
        os.system('python3 -m http.server --directory ./')


@cli.command(cls=HelpColorsCommand,
             help_options_color='cyan',
             short_help='config some environment')
@click.option('-jp',
              '--jupyter',
              is_flag=True,
              help='config jupyter notebook extensions and theme')
@click.option('-al', '--alias', is_flag=True, help='print frequent used alias')
def config(jupyter, alias):

    if jupyter:
        FILE = join(ROOT, 'scripts', 'setnotebook.sh')
        with Console().status("[bold green]configing jupyter..."):
            subprocess.run(f'bash {FILE}'.split())
    if alias:
        render_alias()


@cli.command(cls=HelpColorsCommand,
             help_options_color='cyan',
             short_help='manage pypi package')
@click.option('-p', '--publish', is_flag=True, help='publish package to pypi')
@click.option('-c', '--clean', is_flag=True, help='clean compile files')
def pypi(publish, clean):
    """Examples:

    \b
            publish package to pypi:
                - woc pypi -p | --publish
            clean pypi build output:
                - woc pypi -c | --clean
            combine activity chain:
                - woc pypi -pc
    """

    if publish:
        FILE = join(ROOT, 'scripts', 'publish.sh')
        subprocess.run(f'bash {FILE}'.split())

    if clean:
        FILE = join(ROOT, 'scripts', 'clean.sh')
        subprocess.run(f'bash {FILE}'.split())

    if not (publish or clean):
        click.secho(
            "I don't know what you're trying to do. Do you know what you're doing...",
            fg='red')


@cli.command(cls=HelpColorsCommand,
             help_options_color='cyan',
             help='run python script')
@click.argument('script', nargs=1, required=True)
@click.option('-D',
              '--logdir',
              default=None,
              show_default=True,
              help='log directory')
@click.option('-b',
              '--background',
              is_flag=True,
              show_default=True,
              help="run program in background")
def run(script, logdir, background):
    # pipenv path
    PIPENV = subprocess.getoutput('which pipenv')
    CHECK_PIPENV = os.system('pipenv --venv')
    if logdir:
        LOG_PATH = f'''{logdir}/{get_pure_filename(script)}'''
        LOG_FILE = f'''{LOG_PATH}/{datetime.now().strftime(
            "%Y-%m-%d:%H:%M:%S")}.log'''
        Path(LOG_PATH).mkdir(parents=True, exist_ok=True)

    REDIRECT_SEG = redirect(background)

    if CHECK_PIPENV == 0:
        # if exist pipenv environment
        if not logdir:
            os.system(f'''{PIPENV} run python3 {script}''')
        else:
            os.system(
                f'''{PIPENV} run python3 {script} >>{LOG_FILE} {REDIRECT_SEG}'''
            )
    else:
        if not logdir:
            os.system(f'''python3 {script}''')
        else:
            os.system(f'''python3 {script} >>{LOG_FILE} {REDIRECT_SEG}''')


@cli.command(cls=HelpColorsCommand,
             help_options_color='cyan',
             help='download url')
@click.argument('args', nargs=-1, required=True)
@click.option('-d',
              '--dir',
              type=click.Path(),
              default="./",
              show_default=True,
              help="download directory")
def download(args, dir):
    downloading(args, dir)


@cli.command(cls=HelpColorsCommand,
             help_options_color='cyan',
             short_help='render math expression into latex')
@click.argument('math_expression', nargs=1, required=True)
def latex(math_expression):
    '''Example:

    \b
    woc latex 'x = 2*sqrt(2*pi*k*T_e/m_e)*(DeltaE/(k*T_e))**2*a_0**2'
    '''
    latex = py2tex(math_expression)
    # latex = py2tex('x = 2*sqrt(2*pi*k*T_e/m_e)*(DeltaE/(k*T_e))**2*a_0**2')
    Console().print(latex, style='green')


def execute():
    try:
        cli()
    except Exception as error:
        traceback.print_exc()


if __name__ == "__main__":
    execute()
