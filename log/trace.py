#coding=gbk


levelTrace = 1
levelHintHint = 2
levelHintGood = 4
levelWarning = 8
levelError = 16
levelEmphasize = 32
levelAll = levelTrace | levelHintHint | levelHintGood | levelWarning | levelError | levelEmphasize


class Output:
    def __init__(self):
        self.mLevel = levelAll

    def setLevel(self, lvl):
        self.mLevel = lvl

    def getLevel(self):
        return self.mLevel

    def cancelLevel(self, lvl):
        self.mLevel = self.mLevel & ~lvl

    def flush(self):
        pass

    def onTrace(self, msg, level):
        pass


class Tracer:
    def __init__(self):
        self.mLevel = levelAll
        self.mOutput = []

    def setLevel(self, lvl):
        self.mLevel = lvl

    def getLevel(self):
        return self.mLevel

    def registerTrace(self, o):
        self.mOutput.append(o)

    def unregisterTrace(self, o):
        self.mOutput.remove(o)

    def flush(self):
        for o in self.mOutput:
            o.flush()

    def output(self, msg, level):
        if (level & self.mLevel) != 0:
            for o in self.mOutput:
                if (o.getLevel() & level) != 0:
                    o.onTrace(msg, level)


class OutputTest(Output):
    def __init__(self):
        Output.__init__(self)

    def onTrace(self, msg, level):
        print(level, msg)


if __name__ == "__main__":
    log = Tracer()
    log.registerTrace(OutputTest())
    log.registerTrace(OutputTest())
    log.output("test", levelError)
