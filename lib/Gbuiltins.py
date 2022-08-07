from lib.Errors import TaskNotFoundError
import lib.Gruntime as Gruntime
import lib.Gconstants as Gconstants
from lib.Core import Getstart,setConfig

def workdir(newDir=""):
    """
    设置工作目录
    Set Workdir
    """
    if not newDir:
        print(Gruntime.get_value("Config").get('workdir'))
        return
    setConfig('workdir',newDir)
    print("The workdir is set to",newDir)

def task(name=""):
    """
    查看任务列表,可查看指定名称的任务
    Show task list, or show certain tasks by a name
    """
    if not name:
        Gruntime.get_value("TaskList").gettable()
        return
    tl = Gruntime.get_value("TaskList")
    t = {k:v for k,v in tl.tasks.items() if v.modname == name}
    tl.gettable(t)

def logs(id):
    """
    查看日志
    Show logs
    """
    tl = Gruntime.get_value("TaskList")
    if not tl.total:
        print("Empty task list")
        return
    ti = tl.getTask(id)
    if ti:
        lgs = Gconstants.LINESEP.join(ti.logs)
        Console = Gruntime.get_value('Console')
        Console.print(lgs)
        return
    raise TaskNotFoundError(id)

def help(modname):
    if not modname:
        pass
        return
    
    _, mod = Getstart(modname)
    Gruntime.get_value("RichInspect")(mod,methods=True)
    
    


