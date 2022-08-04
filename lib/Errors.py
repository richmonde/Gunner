class GunnerError(Exception):
    def __str__(self):
        return self.msg

class InputError(GunnerError):
    def __init__(self, msg:str="", ipt:str|list=""):
        if type(ipt) == list:
            self.msg = msg.format(*ipt)
        else:
            self.msg = msg.format(ipt)
        
        super().__init__()

class NothingError(InputError):
    pass

class ModNotFoundError(InputError):
    def __init__(self, modname):
        super().__init__("The module '{}' was not found, please check your input or workdir config.", modname)

class MissingArgsError(InputError):
    def __init__(self, modname, argname):
        super().__init__("The arguments '{}' of '{}' input missing in function signature",[','.join(argname),modname])

class RedundantArgsError(InputError):
    def __init__(self, args):
        super().__init__("Reduntdant args {}",','.join(args))
