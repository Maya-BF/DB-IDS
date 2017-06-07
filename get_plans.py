#!/usr/bin/python3
import sys
import csv
import re
import json
def get_plan():
    file_name = sys.argv[1]
    #regex to remove the first part of the query plan to leave only the
    #json query plan
    regex_clean_plan = re.compile(r'duration: .*plan:')
    plans=[]
    with open(file_name,'r') as log_file:
        reader = csv.reader(log_file)
        for row in reader:
           # print(row)
           col = 0
           #parse a csv line (row)
           for csv_num , csv_field in enumerate(row):
               #col 13 is the one of the query plan
               if(csv_num == 13 and 'duration' in row[csv_num]):
                   # regex to remove the first part of the query plan
                   # piece in the csv to leave only the json part
                   #TO DO: change findall to a single search?
                   before_plans = regex_clean_plan.findall(row[csv_num])
                   #for every
                   for text in before_plans:
                       plan = row[csv_num].replace(text,'')
                       try:
                           # transform json plan to dict
                           plan = json.loads(plan)
                           plans.append(plan)
                       except ValueError:
                           print('not a valid json structure')
    return(plans)

def get_features(plan):
    '''
    Parse plans and create a list of all nodes features
    input: plan is the plan['Plan'] from the json log
    '''
    features = plan.keys()
    [feature_vect.append(f) for f in features if f not in feature_vect]
    if 'Plans' in features:
       for p in plan['Plans']:
            get_features(p)
    return feature_vect

feature_vect = []
feature_vect.append(u'Query Text')
for elmt in get_plan():
    print(elmt)
    print(get_features(elmt['Plan']))
    print('\n')

