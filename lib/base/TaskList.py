import lib.Gruntime as Gruntime
import lib.Gconstants as Gconstants
from os.path import exists as direxists
from os import makedirs
from time import strftime
from dataclasses import dataclass, field
from uuid import uuid1
from rich.table import Table

@dataclass
class TaskItem():
    modname: str
    args: str
    workdir: str
    key: str = None
    create_time: str = strftime("%y%m%d_%H%M%S")
    status: str = Gconstants.RUNNING
    result: str = None
    logs: list = field(default_factory=lambda:[])
    
    
    def getself(self):
        return [v for k,v in self.__dict__.items() if k not in ['logs','workdir','key']] + [str(bool(len(self.logs)))]
    
    def update(self,res):
        self.result = res

    def log(self,info):
        timestamp = f"[{strftime('%y%m%d-%H:%M:%S')}]"
        if len(info) > 1024:
            opentype = "a" if type(info) == str else "ab"
            logdir = f"{self.workdir}/{self.key}/"
            if not direxists(logdir):
                makedirs(logdir)
            with open(f"{logdir}/{self.key}.log",opentype) as logfile:
                logfile.write(timestamp.encode()+Gconstants.LINESEP.encode()+info)
        else:
            self.update(info)
            self.logs.append("[{}] {}".format(timestamp,info))
        if len(self.logs) == 5:
            logdir = f"{self.workdir}/{self.key}/"
            if not direxists(logdir):
                makedirs(logdir)
            with open(f"{logdir}/{self.key}.log","a") as logfile:
                logfile.write(Gconstants.LINESEP.join(self.logs))
            self.logs.clear()

    def finish(self):
        self.status = Gconstants.DONE
    
    def error(self):
        self.status = Gconstants.ERROR



@dataclass
class TaskList():
    total: int = 0
    done: bool = False
    tasks: dict[TaskItem] = field(default_factory = lambda: {})
    
    def getTask(self,key):
        return self.tasks.get(key)
    
    def addTask(self,task:TaskItem):
        key = "{}_{}".format(task.modname , str(uuid1())[:8])
        task.key = key
        self.tasks[key] = task
        self.total += 1
        self.done = False
        return key

    def removeTask(self, key):
        if key in self.tasks:
            del self.tasks[key]

    def gettable(self,data:dict = {}):
        if not data:
            data = self.tasks
        table = Table(*["TaskName","ModuleName","ArgsName","Create_Time","Status","Result","HaveLogs"],caption_justify="left")
        all_rows_atonce = [[taskname,*(taskitem.getself())] for taskname,taskitem in data.items()]
        table.caption = "Total: {}".format(len(all_rows_atonce))
        for row in all_rows_atonce: 
            table.add_row(*row)
        Gruntime.get_value("Console").print(table)
        return
