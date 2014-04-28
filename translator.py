import importlib
from types import ModuleType
import inspect

def createModuleDict(getNamesFromModule):
    '''Given a modulename create a dict with all imported names.'''
    newDict = {}
    #print getNamesFromModule
    my_module = importlib.import_module(getNamesFromModule)
    
    for modulename in [t for t in my_module.__dict__.itervalues() if isinstance(t, ModuleType)]:
        try:
            newDict[modulename.__name__.split(".")[-1]] = modulename.__name__.split(".")[-1]
            newDict.update(createModuleDict(getNamesFromModule + '.' + modulename.__name__.split(".")[-1]))
        except:
            pass
    for typename in [t for t in my_module.__dict__.itervalues() if inspect.isclass(t) ]:
        try:    
            newDict[typename.__name__] = typename.__name__
        except:
            pass
    for functionname in [t for t in my_module.__dict__.itervalues() if hasattr(t, '__call__') ]:
        try:
            newDict[functionname.__name__] = functionname.__name__
        except:
            pass
    return newDict


def getKeywords():
    return {'and' : 'and',           'del' : 'del',         'from' : 'from',     'not' : 'not',    'while' : 'while',
            'as' : 'as',             'elif' : 'elif',       'global' : 'global', 'or' : 'or',      'with' : 'with',
            'assert' : 'assert',     'else' : 'else',       'if' : 'if',         'pass' : 'pass',  'yield' : 'yield', 
            'break' : 'break',       'except' : 'except',   'import' : 'import', 'print' : 'print', 
            'class' : 'class',       'exec' : 'exec',       'in' : 'in',         'raise' : 'raise', 
            'continue' : 'continue', 'finally' : 'finally', 'is' : 'is',         'return' : 'return',
            'def' : 'def',           'for' : 'for',         'lambda' : 'lambda', 'try' : 'try'}
    
def getBuiltInNames():
    

    buildinNames = createModuleDict('__builtin__')
    buildinNames.update(getKeywords())
    return buildinNames

