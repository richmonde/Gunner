from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich import inspect
from lib.Config import loadConfig
from lib.base.TaskList import TaskList
DONE = 'DONE'
RUNNING = 'RUNNING'
ERROR = 'ERROR'
def _init():  # 初始化
    global _global_dict
    _global_dict = {
        'TaskList': TaskList(),
        'Config': loadConfig(),
        'Console': Console(),
        'RichInspect': inspect,
        #'ThreadPool': ThreadPoolExecutor(max_workers=3),
        'TaskLoop': None,
        'TaskThread': None,
    }


def set_value(key, value):
    """ 定义一个全局变量 """
    _global_dict[key] = value


def get_value(key, defValue=None):
    """ 获得一个全局变量,不存在则返回默认值 """
    try:
        return _global_dict[key]
    except KeyError:
        return defValue
