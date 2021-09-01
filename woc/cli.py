#!/usr/bin/python3
# *_*coding:utf-8 *_*
import os
import sys
import subprocess
from tqdm import tqdm
from rich.progress import track
from os.path import dirname, abspath, join

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
    """

                                /T /I.
                               / |/ | .-~/.
                           T\ Y  I  |/  /  _
          /T               | \I  |  I  Y.-~/
         I l   /I       T\ |  |  l  |  T  /
  __  | \l   \l  \I l __l  l   \   `  _. |
  \ ~-l  `\   `\  \  \\ ~\  \   `. .-~   |
   \   ~-. "-.  `  \  ^._ ^. "-.  /  \   |
 .--~-._  ~-  `  _  ~-_.-"-." ._ /._ ." ./
  >--.  ~-.   ._  ~>-"    "\\   7   7   ]
 ^.___~"--._    ~-{  .-~ .  `\ Y . /    |
  <__ ~"-.  ~       /_/   \   \I  Y   : |
    ^-.__           ~(_/   \   >._:   | l
        ^--.,___.-~"  /_/   !  `-.~"--l_
               (_/ .  ~(   /'     "~"--,Y   -=b-.
                (_/ .  \  :           / l      c"~o \
                 \ /    `.    .     .^   \_.-~"~--.  )
                  (_/ .   `  /     /       !         )/
                   / / _.   '.   .':      /
                 /_/ . ' .-~" `.  / \  \               ,v=-
                  ~( /   '  :   | K   "-.~-.______//=-
                      "-,.    l   I/ \_    __{--->._(==-
                        //(     \ <            ~"~"   \\=-
                       /' /\     \  \        ,v=
                     .^. / /\     "  }__ //=-
                    / / ' '  "-.,__ {---(==-
                  .^ '        :  T   ~" \\ =-
                  / ./. .| .|. \
                 / .  .  . : | :!
                (_/  /   | | j-" _)
                ~-<_(_.^-~"˜¤¹
"""


# http://patorjk.com/software/taag/#p=display&h=0&v=0&f=Graffiti&t=funlp


@cli.command(help='clean useless path and file')
def clean():
    FILE = join(ROOT, 'scripts', 'clean.sh')
    subprocess.run(f'bash {FILE}'.split())


@cli.command(help='create pipenv environment base current directory')
def create():
    FILE = join(ROOT, 'scripts', 'create.sh')
    subprocess.run(f'bash {FILE}'.split())


@cli.command(help='render a beautiful tree with given path')
@click.argument('path', nargs=-1)
def tree(path):
    FILE = join(ROOT, 'tree.py')
    DIR = path[0] if path else os.getcwd()
    subprocess.run(f'python3 {FILE} {DIR}'.split())


@cli.command(help='''
woc pip --help\n
Examples:\n
    woc pip fire just scrapy -y\n
    woc pip requirements.txt
''')
@click.argument('pkgs', nargs=-1, required=True)
@click.option('-y',
              '--yes',
              is_flag=True,
              default=False,
              show_default=True,
              help="Whether to use pypi official source")
def pip(pkgs, yes):

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


@cli.command(help='push changes to remote git')
def gitp():
    FILE = join(ROOT, 'scripts', 'gitpush.sh')
    subprocess.run(f'bash {FILE}'.split())


@cli.command(help='remove all cached files from staging area')
def gitrmc():
    subprocess.run('git rm -r --cache .'.split())


@cli.command(help='deploy hexo blog')
def hexod():
    FILE = join(ROOT, 'scripts', 'deploy.sh')
    subprocess.run(f'bash {FILE}'.split())


@cli.command(help='print alias')
def alias():
    ALIASES = '''
alias ll='ls -lh'
alias l='ls -lha'
alias ..='cd ..'
alias axel='axel -n 100'
alias free="free -h"
alias df="df -h"
alias vi="vim"
alias ~="cd ~"
alias sh="bash"

# pathes
alias cddow="cd ~/Downloads/;pwd"
alias cdh="cd ~;pwd"
alias cddoc="cd ~/Documents/;pwd"
alias cdmusic="cd ~/Music;pwd"
alias cdgitee="cd ~/Music/GiteProjects/"
alias cdgithub="cd ~/Music/GithubProjects/"

#alias jp="jupyter notebook --no-browser --allow-root >&1 &"
alias jp="jupyter notebook --no-browser"

#alias jl="jupyter lab --allow-root >&1 &"
alias jl="jupyter lab"

# start mongodb server
alias imongo="sudo /usr/local/mongodb/bin/mongod --dbpath=/usr/local/mongodb/data/db/"
   
'''
    click.secho(ALIASES, blink=True)


@cli.command(help='print git tutorials')
def gittuto():
    GIT_TUTORIALS = '''
    ## Push代码的建议执行顺序

    git status #查看修改状态

    # git checkout filename #放弃某文件的修改。

    git stash # 储存修改

    git rebase # 与本地分支合并

    git stash pop # 弹出储存文件，此时新文件可能会与你的文件产生冲突，解决冲突。

    # git add filename 添加某个修改文件

    git add . # 提交所有加点

    # git reset HEAD filename # 回滚指定文件，回滚所有加点："git reset HEAD . "

    # echo "请输入描述信息" | boxes -d columns -a c
    echo "请输入描述信息" | pv -qL 20
    read -p ": " input
    git commit -m "$input"


    git push # 本地remote远程分支名，本地分支名

    git status #查看修改状态


    # 把这个目录变成git可以管理的仓库
    # git init

    # git add -A  提交所有变化
    # git add -u  提交被修改(modified)和被删除(deleted)文件，不包括新文件(new)
    # git add .  提交新文件(new)和被修改(modified)文件，不包括被删除(deleted)文件
    # git status
    # 添加到暂存区里面去
    # git add -A


    # echo "请输入描述信息" | boxes -d columns -a c
    # echo "请输入描述信息" | pv -qL 20
    # read -p ": " input
    # git commit -m "$input"
    # git pull --rebase origin master
    # git push origin master



    # 关联到远程库
    # git remote add origin git@+服务器地址

    # git clone 指定分支
    # git clone -b dev_jk http://10.1.1.11/service/tmall-service.git

    # 将最新的修改推送到远程仓库
    # git push -u origin master     # 这句直接提交不用写什么commit，很方便

    # 获取远程库与本地同步合并
    # git pull --rebase origin master
    git pull = git fetch + git merge

    # 查看改动情况
    # git status

    # 查看在哪个位置
    # git branch

    # 切换到分支
    # git checkpoint develop    # develop是分支名称

    # 上传到服务器
    # git push origin develop   # origin是服务器的名称 develop是分支名称

# git reset:主要用来版本回退
git reset --hard head~1 # 将head指向上1次的commit。也可以用git reset --hard id 回退到指定版本

# push大文件失败，在将大文件删除之后，其余小文件仍然受到之前大文件push失败的影响，无法正常push。
# 解决方案：需要将之前含有大文件的commit记录删除（全部删除），使用git reset --hard head~1回退就可以

# 查看日志
git log --oneline --graph

# git log 命令可以显示所有提交过的版本信息，而git reflog 可以查看所有分支的所有操作记录（包括已经被删除的 commit 记录和 reset 的操作）
git reflog # 找到删除的id后退出，再执行git reset --hard id回退到删除以前的状态

# 删除cache file
git rm -r --cached .
    '''
    click.echo_via_pager(GIT_TUTORIALS)


@cli.command(help='install linux packages through apt-get')
def aptinstall():
    FILE = join(ROOT, 'scripts', 'aptinstall.sh')
    subprocess.run(f'bash {FILE}'.split())


@cli.command(help='delete pipenv environment')
def delete():
    FILE = join(ROOT, 'scripts', 'delete.sh')
    subprocess.run(f'bash {FILE}'.split())


@cli.command(help='install node')
def installnode():
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


@cli.command(help='config jupyter notebook extension and theme')
def configjupyter():
    FILE = join(ROOT, 'scripts', 'setnotebook.sh')
    subprocess.run(f'bash {FILE}'.split())


@cli.command(help='run install')
def install():
    FILE = join(ROOT, 'scripts', 'install.sh')
    subprocess.run(f'bash {FILE}'.split())


@cli.command(help='run publish')
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
