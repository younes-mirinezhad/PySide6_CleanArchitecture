# This Python file uses the following encoding: utf-8
import inspect
def func_info():
    frame = inspect.currentframe().f_back
    info = "-----> "
    info += frame.f_locals.get('self', None).__class__.__name__ if 'self' in frame.f_locals else None
    info += "."
    info += frame.f_code.co_name
    info += "()"
    return info
