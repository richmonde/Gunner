from sys import modules as Gruntime_mods
def _init():  # 初始化
    global _global_dict
    _global_dict = {
        'MainPath': None,
        'TaskList': None,
        'Config': None,
        'Console': None,
        'RichInspect': None,
        #'ThreadPool': ThreadPoolExecutor(max_workers=3),
        'TaskLoop': None,
        'TaskThread': None,
        'RuntimeMods': Gruntime_mods
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

def getConfile():
    return f"{get_value('MainPath')}/config.json"