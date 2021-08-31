# *_*coding:utf-8 *_*
import fire
import os


def install_package(*args):

    if 'o' in args:
        for pkg in [pkg for pkg in args if pkg not in ['o']]:
            os.system(
                f'pip3 install {pkg} -i https://mirrors.aliyun.com/pypi/simple'
            )
    else:
        for pkg in [pkg for pkg in args if pkg not in ['o']]:
            os.system(f'pip3 install {pkg}')


def main():
    fire.Fire(install_package)


if __name__ == '__main__':
    main()
