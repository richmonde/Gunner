import lib.Gruntime as Gruntime
from time import strftime
from dataclasses import dataclass, field
from uuid import uuid1
from rich.table import Table

DONE,RUNNING,ERROR = ['DONE','RUNNING','ERROR']

@dataclass
class TaskItem():
    modname: str
    args: str
    create_time: str = strftime("%y%m%d_%H%M%S")
    status: str = RUNNING
    result: str = None
    logs: list = field(default_factory=lambda:[])
    
    def getself(self):
        return [v for k,v in self.__dict__.items() if k != 'logs'] + [str(len(self.logs))]
    
    def update(self,res):
        self.result = res

    def log(self,info):
        self.update(info)
        self.logs.append((strftime("%y%m%d-%H:%M:%S"),info))

    def finish(self):
        self.status = DONE
    
    def error(self):
        self.status = ERROR



@dataclass
class TaskList():
    total: int = 0
    done: bool = False
    tasks: dict[TaskItem] = field(default_factory = lambda: {})
    
    def getTask(self,key):
        return self.tasks.get(key)
    
    def addTask(self,task:TaskItem):
        key = "{}_{}".format(task.modname , str(uuid1())[:8])
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
        table = Table(*["TaskName","ModuleName","ArgsName","Create_Time","Status","Result","Log_Count"],caption_justify="left")
        all_rows_atonce = [[taskname,*(taskitem.getself())] for taskname,taskitem in data.items()]
        table.caption = "Total: {}".format(len(all_rows_atonce))
        for row in all_rows_atonce: 
            table.add_row(*row)
        Gruntime.get_value("Console").print(table)
        return
