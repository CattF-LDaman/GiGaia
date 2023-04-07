import functools
import threading

def threaded_nondaemon(func):
    @functools.wraps(func)
    def wr(*args, **kwargs):

        t = threading.Thread(target=func,args=args,kwargs=kwargs,name=str(func)+str((args,kwargs)),daemon=False)
        t.start()

    return wr

def threaded_daemon(func):
    @functools.wraps(func)
    def wr(*args, **kwargs):

        t = threading.Thread(target=func,args=args,kwargs=kwargs,name=str(func)+str((args,kwargs)),daemon=True)
        t.start()

    return wr
