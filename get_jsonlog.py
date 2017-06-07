import sys
import re
import json

def get_jsonlog():
    logfile = sys.argv[1]
    jsonfile = sys.argv[2]

    try:
        with open(logfile, 'r') as in_file:
           log = in_file.read()
    #regex to get the json part fromm log

        log = log.replace('\n','')
        #regex_json = re.compile('plan:.*(?!noneLOG:|noneSTATEMENT:|noneERROR:|noneHINT:)\}', re.MULTILINE|re.DOTALL)
        regex_json = re.compile('plan:.*[^noneLOG:]\}',re.MULTILINE|re.DOTALL)
        #regex = re.compile('plan:.*')
        json_log = regex_json.findall(log)
        print(json_log)

    except IOError:
        print('File not found')

get_jsonlog()
