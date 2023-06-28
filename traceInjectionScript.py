# Python script to create copy of specified file, then inject that file with with trace code
# Requires one argument for the filename 
# The new injected script is found at fileToTrace.py, and has to be manually run (because we don't know if it needs arguments)
# Admittedly this injection is quite weird and feels like a workaround, however haven't found alternative yet

newFileName = "fileToTrace.py"
analysisCodeToInsert = """##Start of injected analysis code
from sys import settrace
import sys
import atexit
import json
import os
import pathlib

currentFilePath = pathlib.Path(__file__).resolve()
linesInAnalysisString = {0}
_traced_lines = []
def _my_tracer(frame, event, arg = None):
    # extracts frame code
    _code = frame.f_code
    _file_name = _code.co_filename
    # print(_file_name)
  
    # extracts calling function name
    _func_name = _code.co_name
  
    # extracts the line number
    _line_no = frame.f_lineno
    #print("current file path", currentFilePath)
    #print( "current file name", _file_name)
    if ( (os.path.basename(_file_name) == os.path.basename(str(currentFilePath))) and _line_no>linesInAnalysisString and (event == 'line' or event == 'call')):
        _actual_line_no = _line_no-linesInAnalysisString
        #print(f"A {{event}} encountered in     {{_func_name}}() at line number {{_actual_line_no}} in file {{_file_name}}")
        _traced_lines.append(str(_actual_line_no))
    return _my_tracer

def exit_handler():
    with open('dynamicResults.json', 'w') as f:
        f.write(json.dumps(_traced_lines))
settrace(_my_tracer)
sys._getframe().f_trace = _my_tracer
atexit.register(exit_handler)

##End of injected analysis code

"""
linesInAnalysisString = len(analysisCodeToInsert.split('\n') )-1
# print(linesInAnalysisString)
analysisCodeToInsert = analysisCodeToInsert.format(str(linesInAnalysisString))

def prePendAndCreateNewFile(originalfile,string):
    with open(originalfile,'r') as f:
        with open(newFileName,'w') as f2: 
            f2.write(string)
            f2.write(f.read())
      



def run(fileToBeCopied):


    prePendAndCreateNewFile(fileToBeCopied, analysisCodeToInsert)
    return newFileName


