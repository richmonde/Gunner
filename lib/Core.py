import asyncio
from importlib import reload
import threading
import lib.Gruntime as Gruntime
import lib.Gconstants as Gconstants
import json
from functools import partial
from sys import path
from os import listdir
from inspect import getmembers, isfunction
from shlex import split as shlexSplit
from lib.Errors import ModNotFoundError, NothingError
from lib.base.TaskList import TaskItem
from rich.console import Console
from rich import inspect
from lib.base.TaskList import TaskList
from os.path import abspath

def StartTaskLoop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def StartTaskThread():
    loop = asyncio.new_event_loop()
    Gruntime.set_value("TaskLoop",loop)
    Gruntime.get_value("TaskLoop").set_exception_handler(exception_handler)
    thread = threading.Thread(target=lambda: StartTaskLoop(loop),daemon=True)
    Gruntime.set_value("TaskThread",thread)
    thread.start()


def Fire(s):

    s = ParseSingle(s)
    modname, args = s
    Flag, mod = GetmodfromSingle(s)
    pargs = [p for p in args if type(p) == str]
    kargs = {x:y for x,y in [list(k.items())[0] for k in args if type(k) == dict]}
    argstr = ','.join(["{}={}".format(*list(arg.items())[0]) if type(arg)== dict else arg for arg in args])
    ti = TaskItem(modname,argstr,Gruntime.get_value("Config").get("workdir"))
    if Flag == Gconstants.CONCURRENT:
        kargs["taskinfo"] = ti
        pmod = partial(mod,**kargs)
        key = Gruntime.get_value("TaskList").addTask(ti)
        future = Gruntime.get_value("TaskLoop").run_in_executor(None,pmod,*pargs)
        future.key = key
        return
    if Flag != Gconstants.GBUILTIN:
        kargs["taskinfo"] = ti
        key = Gruntime.get_value("TaskList").addTask(ti)
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
        item.status = Gconstants.ERROR
        item.result = str(future.exception())
    Gruntime.get_value("Console").print("❌",context['exception'])


def GetmodfromSingle(sngl: tuple):
    """
    取内置模块/自定义模块
    ret: Flag,Function 任务类型标记|函数对象
    """
    modname, args = sngl
    Flag, mod = Getstart(modname)
    return Flag, mod


def Getstart(mname):
    import lib.Gbuiltins as gbt
    if btin := dict(getmembers(gbt, isfunction)).get(mname):
        return Gconstants.GBUILTIN, btin
    spdir = Gruntime.get_value('Config').get('workdir')
    path.insert(0, spdir)
    mods = [modname[0:-3]
            for modname in listdir(spdir) if modname.endswith('.py')]
    try:
        if mname in (rtmods := Gruntime.get_value("RuntimeMods")):
            mod = reload(rtmods['mname'])
            start = getattr(mod, 'start', None)
            return Gconstants.CONCURRENT if hasattr(mod,"CONCURRENT_FLAG_OF_GUNNER") else Gconstants.NORMALMOD, start
        if (mname in mods):
            mod = __import__(mname, fromlist=['start'])
            start = getattr(mod, 'start', None)
            return Gconstants.CONCURRENT if hasattr(mod,"CONCURRENT_FLAG_OF_GUNNER") else Gconstants.NORMALMOD, start
    except ValueError as e:
        pass
    raise ModNotFoundError(mname)

def InitRuntime():
    
    Gruntime.set_value("MainPath",abspath("."))
    Gruntime.set_value("TaskList",TaskList())
    Gruntime.set_value("Config",loadConfig())
    Gruntime.set_value("Console",Console())
    Gruntime.set_value("RichInspect",inspect)
    re2ab()

def StopRuntime():
    loop = Gruntime.get_value("TaskLoop")
    loop.call_soon_threadsafe(loop.stop)

def re2ab(key='workdir'):
    conf = Gruntime.get_value("Config")
    relative = conf.get(key)
    conf[key] = abspath(relative)
    Gruntime.set_value("Config",conf)

def loadConfig():
    confile = Gruntime.getConfile()
    with open(confile,'r') as f:
        wjson = json.loads(f.read())
    return wjson

def setConfig(key,value):
    confile = Gruntime.getConfile()
    wjson = loadConfig()
    with open(confile,'w') as f:
        wjson[key] = value
        json.dump(wjson,f)
    Gruntime.set_value("Config",loadConfig())
    re2ab()
        

