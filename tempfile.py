import sys
import csv
import re
import json
def get_plan():
    file_name = sys.argv[1]
    regex_clean_plan = re.compile(r'duration: .*plan:')
    qplans=[]
    features=[]
    with open(file_name,'r') as log_file:
        reader = csv.reader(log_file)
        for row in reader:
           # print(row)
           col = 0
           for column in row:
               if(col == 13 and 'duration' in row[col]):
                   #print(row[col], col)
                   meta = regex_clean_plan.findall(row[col])
                   for word in meta:
                       qplan = row[col].replace(word,'')
                        try:
                            print(qplan['Plan']['Plans'][0].keys())
                            for(key in qplan['Plan'].keys()):
                                if(key not in features):
                                    f.append(key)
                            #print('\n')
                            plans.append(json.loads(row[col]))
                        except ValueError:
                            print('not a valid json structure')
               col +=1
    return(plans)

for elmt in get_plan():
    #print(elmt)
    print('\n')
