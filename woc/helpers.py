import os
import re
import shutil
import stat
import sys
import tempfile
import warnings
from os.path import dirname, abspath, join, basename, splitext
from rich.console import Console
from rich.markdown import Markdown
try:
    from woc.decorator import decorator
    from woc.config import Config
except:
    from .config import Config
    from .decorator import decorator
from contextlib import contextmanager
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional

import requests

try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping

_canonicalize_regex = re.compile("[-_]+")

SHELL = os.getenv("SHELL", "")
MACOS = sys.platform == "darwin"
WINDOWS = sys.platform.startswith("win") or (sys.platform == "cli"
                                             and os.name == "nt")


def redirect(hide: bool = False):
    """
    use `2>&1` to redirect the output of the error message to standard output

    :param hide:
    :return:
    """
    if WINDOWS:
        return ''
    elif hide:
        # the final & is to make the program continue when terminal exit
        return ' 2>&1 &'
    else:
        return ''


def get_pure_filename(fpath: str):
    """Get pure filename

    :param fpath: woc/woc/woc.txt
    :return: woc
    """
    return splitext(basename(fpath))[0]


def canonicalize_name(name: str) -> str:
    return _canonicalize_regex.sub("-", name).lower()


def module_name(name: str) -> str:
    return canonicalize_name(name).replace(".", "_").replace("-", "_")


def _del_ro(action: Callable, name: str, exc: Exception) -> None:
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)


@contextmanager
def temporary_directory(*args: Any, **kwargs: Any) -> Iterator[str]:
    name = tempfile.mkdtemp(*args, **kwargs)

    yield name

    shutil.rmtree(name, onerror=_del_ro)


def get_cert(config: Config, repository_name: str) -> Optional[Path]:
    cert = config.get(f"certificates.{repository_name}.cert")
    if cert:
        return Path(cert)
    else:
        return None


def get_client_cert(config: Config, repository_name: str) -> Optional[Path]:
    client_cert = config.get(f"certificates.{repository_name}.client-cert")
    if client_cert:
        return Path(client_cert)
    else:
        return None


def _on_rm_error(func: Callable, path: str, exc_info: Exception) -> None:
    if not os.path.exists(path):
        return

    os.chmod(path, stat.S_IWRITE)
    func(path)


def safe_rmtree(path: str) -> None:
    if Path(path).is_symlink():
        return os.unlink(str(path))

    shutil.rmtree(path, onerror=_on_rm_error)


def merge_dicts(d1: Dict, d2: Dict) -> None:
    for k, v in d2.items():
        if k in d1 and isinstance(d1[k], dict) and isinstance(d2[k], Mapping):
            merge_dicts(d1[k], d2[k])
        else:
            d1[k] = d2[k]


def download_file(
    url: str,
    dest: str,
    session: Optional[requests.Session] = None,
    chunk_size: int = 1024,
) -> None:
    get = requests.get if not session else session.get

    with get(url, stream=True) as response:
        response.raise_for_status()

        with open(dest, "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)


def paths_csv(paths: List[Path]) -> str:
    return ", ".join('"{}"'.format(str(c)) for c in paths)


def is_dir_writable(path: Path, create: bool = False) -> bool:
    try:
        if not path.exists():
            if not create:
                return False
            path.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryFile(dir=str(path)):
            pass
    except OSError:
        return False
    else:
        return True


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
