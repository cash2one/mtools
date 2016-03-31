#coding=gbk

from trace import *
from console import *
from logfile import *

_g_tracer = Tracer()
_g_tracer.registerTrace(FileOutput("log.log"))

def setTraceLevel(level):
    _g_tracer.setLevel(level)

def getTraceLevel():
    return _g_tracer.getLevel()

def flushTrace():
    _g_tracer.flush()

def output2Console():
    o = ConsoleOutput()
    o.cancelLevel(levelTrace)
    _g_tracer.registerTrace(o)
    return o

def trace(msg):
    _g_tracer.output(msg, levelTrace)

def hint(msg):
    _g_tracer.output(msg, levelHintHint)

def good(msg):
    _g_tracer.output(msg, levelHintGood)

def warning(msg):
    _g_tracer.output(msg, levelWarning)

def error(msg):
    _g_tracer.output(msg, levelError)

def emphasize(msg):
    _g_tracer.output(msg, levelEmphasize)
