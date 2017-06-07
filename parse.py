import sys
import re
import json
'''
This function splits posgtresql's log file into the query info, query string
and query plan (in json format) and saves it query info and query plan files.
'''

def parse_log():
    logfile = sys.argv[1]
    txtfilename = sys.argv[2]
    jsonfilename = sys.argv[3]
    try:
        #automatically closes the file
        with open(logfile, 'r') as in_file:
            log = in_file.read()

        #TODO: define re options

        log_str = log.replace('\n','')
        #print(log_str)
        regex_query_info = re.compile('\d{4}-\d{2}-\d{2}\s?\d{2}:\d{2}:\d{2}.\d{0,3}\s\w{3}\s\[\d+\]\s\w+@\w+\s+LOG:\s+duration:\s+\d+.?\d*\s+ms',re.MULTILINE|re.DOTALL)
        regex_query_str = re.compile('\"Query Text\":.*;\"',re.MULTILINE|re.DOTALL)
        regex_query_plan = re.compile('\"Plan\":\s*\{.*\}',re.MULTILINE|re.DOTALL)

        #Get the query info Date Time ..
        query_info = regex_query_info.findall(log_str)
        #Delete the matches from the read file in memory

        for i in query_info:
            #log_no_query_info = log_str.replace(i,'')
            log_str = log_str.replace(i,'')

        #Get the query statement
        query_str = regex_query_str.findall(log_str)

        for s in query_str:
            log_str = log_str.replace(s,'')

        #Get the query Plan
        query_plan = regex_query_plan.findall(log_str)
        #print(query_plan)

        with open(jsonfilename,'a') as jsonfile:
            json.dump(query_plan,jsonfile)

        '''
        with open(txtfilename,'a') as txtfile:
            if(query_info):
                for info,i in zip(query_info,range(len(query_info))):
                    info = info.replace('[','')
                    info = info.replace(']','')
                    info = info.split(' ')
                    print(info)
                    #record = info + ',' + query_str[14:-2] + ',' + query_plan[i] + '\n'
                    txtfile.write(record)
        '''
        '''if(query_info):
            for i, info in enumerate(query_info):
                #reformat query info date,time,time zone, transaction id, user,
                #database, estimated time

                info = info.replace('[','')
                info = info.replace(']','')
                info = info.replace('LOG:','')
                info = info.replace(' duration: ','')
                info = info.replace(' ms','')
                info = info.split(' ')
                user_db = info[4].split("@")
                info[4] = user_db[0]
                info[5] = user_db[1]
                #TODO: Format date and time to a datamining friendly format
                #print(info)

                query = query_str[i]
                query = query[15:-1]
                query = query.replace('\\\"','')
                query = query.replace('\\n','')
                query = ' '.join(query.split())
                print(query)
                #record = info + ',' + query_str[14:-2] + ',' + query_plan[i] + '\n'

                #Format the query plan to
        '''
    except IOError:
        print('There was a pb with the files')


parse_log()

