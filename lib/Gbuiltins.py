import lib.Gruntime as Gruntime
from lib.Core import Getstart

def workdir(newDir):
    """
    设置工作目录
    """
    print("The workdir is set to",newDir)

def task(name=""):
    """
    查看任务列表
    PS: task name= #输出所有任务
    """
    if not name:
        Gruntime.get_value("TaskList").gettable()
        return
    tl = Gruntime.get_value("TaskList")
    t = {k:v for k,v in tl.tasks.items() if v.modname == name}
    tl.gettable(t)

def help(modname):
    if not modname:
        pass
        return
    
    _, mod = Getstart(modname)
    Gruntime.get_value("RichInspect")(mod,methods=True)
    
    
        
