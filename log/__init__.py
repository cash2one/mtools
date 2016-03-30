#coding=gbk

from trace import *
from console import *

_g_tracer = Tracer()

def setTraceLevel(level):
    _g_tracer.setLevel(level)

def output2Console():
    _g_tracer.registerTrace(ConsoleOutput())

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
