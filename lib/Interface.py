from functools import wraps

def GunnerMod(mod):
    @wraps(mod)
    def wrapper(*args,**kwargs):
        mod(*args,**kwargs)
        if 'taskinfo' in kwargs:
            kwargs['taskinfo'].finish()
    return wrapper
