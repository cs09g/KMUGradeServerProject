import os
import glob
import time
import ptrace
import resource
from subprocess import call

RUN_COMMAND_LIST = []

class ExecutionTools(object):
    def __init__(self, usingLang, limitTime, limitMemory, answerPath, version,
                 runFileName, problemName, caseCount):
        self.usingLang = usingLang
        self.limitTime = limitTime
        self.limitMemory = limitMemory
        self.answerPath = answerPath
        self.version = version
        self.runFileName = runFileName
        self.problemName = problemName
        self.caseCount = caseCount
        
    def Execution(self):
        # copy input data
        try:
            if self.caseCount > 0:
                call('cp ' + self.answerPath + self.problemName + '_cases_total_inputs.in input.txt', shell = True)
        except Exception as e:
            print e
            return 'ServerError', 0, 0
        
        # make execution command
        self.MakeCommand()
                
        pid = os.fork()
         
        if pid == 0:
            self.RunProgram()
        
        else:
            result, time, usingMem = self.WatchRunProgram(pid)
        
        print time, usingMem
        
        userTime = int(time * 1000)
        
        if result == 'TimeOver' or result == 'RunTimeError':
            return result, userTime, usingMem
        
        if userTime > self.limitTime:
            return 'TimeOver', userTime, usingMem
        
        coreSize = 0
        coreList = glob.glob('core.[0-9]*')
        
        if len(coreList) > 0:
            coreSize = os.path.getsize(coreList[0])
        
        if coreSize == 0:  # if not exist core file -> evaluate output
            return 'Grading', userTime, usingMem
        
        else:
            return 'RunTimeError', 0, 0
        
        
    def MakeCommand(self):
        # make execution command
        if self.usingLang == 'PYTHON':
            if self.version == '2.7':
                RUN_COMMAND_LIST.append('/usr/bin/python')
                RUN_COMMAND_LIST.append('/usr/bin/python')
                RUN_COMMAND_LIST.append(self.runFileName + '.py')
                
            elif self.version == '3.4':
                RUN_COMMAND_LIST.append('/usr/local/bin/python3')
                RUN_COMMAND_LIST.append('/usr/local/bin/python3')
                RUN_COMMAND_LIST.append(self.runFileName + '.py')
                
        elif self.usingLang == 'C' or self.usingLang == 'C++':
            RUN_COMMAND_LIST.append('./main')
            RUN_COMMAND_LIST.append('./main')
            
        elif self.usingLang == 'JAVA':
            RUN_COMMAND_LIST.append('/usr/bin/java')
            RUN_COMMAND_LIST.append('/usr/bin/java')
            RUN_COMMAND_LIST.append(self.runFileName)
    
    def RunProgram(self):
        os.nice(19)
        
        reditectionSTDOUT = os.open('output.txt', os.O_RDWR|os.O_CREAT)
        os.dup2(reditectionSTDOUT,1)
        
        rlimTime = int(self.limitTime / 1000) + 1
        
        resource.setrlimit(resource.RLIMIT_CORE, (1024,1024))
        resource.setrlimit(resource.RLIMIT_CPU, (rlimTime,rlimTime))
        
        ptrace.traceme()
        
        if self.usingLang == 'PYTHON' or self.usingLang == 'JAVA':
            reditectionSTDERROR = os.open('core.1', os.O_RDWR|os.O_CREAT)
            os.dup2(reditectionSTDERROR,2)
            
            os.execl(RUN_COMMAND_LIST[0], RUN_COMMAND_LIST[1], RUN_COMMAND_LIST[2])
            
        elif self.usingLang == 'C' or self.usingLang =='C++':
            os.execl(RUN_COMMAND_LIST[0], RUN_COMMAND_LIST[1])
            
    def WatchRunProgram(self, pid):
        usingMem = 0
        temp = 0
        
        while True:
            wpid, status, res = os.wait4(pid,0)
    
            if os.WIFEXITED(status):
                return 'ok', res[0], usingMem
            
            exitCode = os.WEXITSTATUS(status)
            if exitCode != 5 and exitCode != 0 and exitCode != 17:
                return 'RunTimeError', 0, 0 
                
            elif os.WIFSIGNALED(status):
                return 'TimeOver', res[0], usingMem
            
            else:
                self.GetUsingMemory(pid)
                
                if temp > usingMem:
                    usingMem = temp
                
                ptrace.syscall(pid, 0)
                
    def GetUsingMemory(self, pid):
        procFile = open('/proc/' + str(pid) + '/status', 'r')
        fileLines = procFile.readlines()

        for i in range(15,20):
            index = fileLines[i].find('VmRSS')
            if index != -1:
                words = fileLines[i].split()
                temp = int(words[index+1])
                break;
            
        return temp