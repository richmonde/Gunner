import asyncio
import threading
import lib.Gruntime as Gruntime
from functools import partial
from sys import path
from os import listdir
from os.path import abspath
from inspect import getmembers, isfunction
from shlex import split as shlexSplit
from lib.Errors import ModNotFoundError, NothingError
from lib.base.TaskList import TaskItem

def StartTaskLoop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def StartTaskThread():
    loop = asyncio.new_event_loop()
    Gruntime.set_value("TaskLoop",loop)
    Gruntime.get_value("TaskLoop").set_exception_handler(exception_handler)
    thread = threading.Thread(target=lambda: StartTaskLoop(loop))
    #Gruntime.set_value("TaskThread",thread)
    thread.start()

def Fire(s):

    s = ParseSingle(s)
    modname, args = s
    ifconcurrent, mod = GetmodfromSingle(s)
    pargs = [p for p in args if type(p) == str]
    kargs = {x:y for x,y in [list(k.items())[0] for k in args if type(k) == dict]}
    ti = TaskItem(modname, ','.join(["{}={}".format(*list(arg.items())[0]) if type(arg)== dict else arg for arg in args]))
    if ifconcurrent:
        kargs["taskinfo"] = ti
        pmod = partial(mod,**kargs)
        Gruntime.get_value("TaskLoop").set_exception_handler(exception_handler)
        future = Gruntime.get_value("TaskLoop").run_in_executor(None,pmod,*pargs)
        key = Gruntime.get_value("TaskList").addTask(ti)
        future.key = key
        return
    mod(*pargs, **kargs)
    
def ParseSingle(sgl: str):
    """
    @GUNNER 语法分析
    (module_name) **kwargs
    ParseSingle("somemod 123 arg2='456' arg3=\"789\"")
    //output
    ('somemod', ['123',{'arg2':'456'},{'arg3':'789'}])
    """
    sgl = list(shlexSplit(sgl))
    if len(sgl) == 0:
        raise NothingError
    args = ParseArgs(sgl[1:])
    return sgl[0], args


def ParseArgs(args):
    return list(map(KeyHandler, args))


def KeyHandler(kv: str):
    kv = kv.split('=')
    if len(kv) == 1:
        return kv[0]
    if kv[1].isdigit():
        return {kv[0]: int(kv[1])}
    return {kv[0]:kv[1].strip('"').strip("'")}

def exception_handler(loop,context):
    if 'future' in context.keys() and (future := context['future']):
        TL = Gruntime.get_value("TaskList")
        item = TL.getTask(future.key)
        item.status = Gruntime.ERROR
        item.result = str(future.exception())
    Gruntime.get_value("Console").print("❌",context['exception'])


def GetmodfromSingle(sngl: tuple):
    """
    取内置模块/自定义模块
    ret: bool,Function 是否为异步任务|函数对象
    """
    modname, args = sngl
    ifconcurrent, mod = Getstart(modname)
    return ifconcurrent, mod


def Getstart(mname):
    import lib.Gbuiltins as gbt
    if btin := dict(getmembers(gbt, isfunction)).get(mname):
        return False, btin
    spdir = abspath(__file__ + '/../../script/')
    path.insert(0, spdir)
    mods = [modname[0:-3]
            for modname in listdir(spdir) if modname.endswith('.py')]
    try:
        if (mname in mods):
            idx = mods.index(mname)
            mod = __import__(mods[idx], fromlist=['start'])
            start = getattr(mod, 'start', None)
            return hasattr(mod,"CONCURRENT_FLAG_OF_GUNNER"), start
    except ValueError as e:
        pass
    raise ModNotFoundError(mname)



