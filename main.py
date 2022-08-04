import lib.Gruntime as Gruntime
from lib.Errors import NothingError
from lib.Core import Fire,StartTaskThread
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout 

def start():
    psess = PromptSession()
    while True:
        try:
            with patch_stdout(raw=True):
                s = psess.prompt("<{}>".format(Gruntime.get_value("Config").get("username")))
                Fire(s)
        except NothingError:
            continue
        except Exception as e:
            Gruntime.get_value("Console").print("❌",e)
            continue

Gruntime._init()
StartTaskThread()
start()
