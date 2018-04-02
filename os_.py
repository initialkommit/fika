import os
import getpass
import socket
import platform


def get_username():
    """shell 로그인 계정"""
    return getpass.getuser()


def is_my_pc():
    """ 맥북이면 내 PC로 판단함."""
    return platform.system().lower() == 'darwin'


def is_server():
    """ 맥북이 아니면 서버로 판단함."""
    return not is_my_pc()


def is_live_server():
    """예를 들어 hostname이 '-live'로 끝나면 live server로 인식"""
    return socket.gethostname().endswith('-live')


class ImproperlyConfigured(Exception):
    """NOT proper os environment variables"""
    pass


def get_env_var(var_name):
    """OS 환경 변수를 가져옴"""
    try:
        return os.environ[var_name]
    except KeyError:
        msg = "Please set the %s environment variable" % var_name
        raise ImproperlyConfigured(msg)
