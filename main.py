import lib.Gruntime as Gruntime
from lib.Errors import NothingError
from lib.Core import Fire,StartTaskThread,InitRuntime,StopRuntime
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

def kbintrpt(psess):
    yn = psess.prompt("Exit?[y/N]: ")
    if yn.lower() == 'y':
        StopRuntime()
        Gruntime.get_value("TaskThread").join()
        print("Good Bye!")
        exit()

def start():
    psess = PromptSession()
    while True:
        try:
            with patch_stdout(raw=True):
                s = psess.prompt("{}>".format(Gruntime.get_value("Config").get("username")))
                Fire(s)
        except NothingError:
            continue
        except KeyboardInterrupt:
            kbintrpt(psess)
            continue
        except Exception as e:
            #Gruntime.get_value('Console').print_exception()
            Gruntime.get_value("Console").print("❌",e)
            continue



Gruntime._init()
InitRuntime()
StartTaskThread()
start()

