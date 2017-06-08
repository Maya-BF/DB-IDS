#!/usr/bin/python3
import sys
import csv
import re
import json

list_features = []
features = ['Node Type','Join Type','Command','Startup Cost',
            'Total Cost','Plan Rows','Plan Width','Output','Index Cond',
            'Order By','Recheck Cond','Filter','Workers Planned','Function Call',
            'TID Cond','Join Filter','Merge Cond','Hash Cond','One-Time Filter',
            'Strategy','Partial Mode','Operation','Parent Relationship',
            'Custom Plan Provider','Parallel Aware','Schema','Alias']

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
                        i   print('not a valid json structure')
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

def valtoreal(key,value):
    '''Assigns the right function from transtype module to the correspondent data type to transform it to real.'''
    trans_funcs = (trans_nodetype,trans_jointype,trans_command,trans_startupcost,trans_totalcost,
                   trans_planrow,trans_planwidth,trans_output,trans_indexcond,trans_orderby,
                   trans_recheckcond,trans_filter,trans_workersplanned,trans_funccall,
                   trans_tidcond,trans_joinfilter,trans_mergecond,trans_hashcond,trans_onetimefilter,
                   trans_strategy,trans_partialmode,trans_operation,trans_parentrelationship,
                   trans_customplanpro,trans_parallelaware,trans_schema,trans_alias)
    #mimics a switch statement
    trans_cases = dict(zip(features,trans_funcs))

    trans_cases.get(key,)(value)

def init_csv():
    '''Set the header of a csv file with all the features'''
    '''TO DO: Add memory related info (buckets..)'''

    with open('data.csv','wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(features)
    #test csv header
    '''with open('data.csv','rb') as outcsv:
        reader = csv.reader(outcsv)
        for row in reader:
            print(row)
    '''
#Init data csv file with header
init_csv()
feature_vect = []
feature_vect.append(u'Query Text')
for elmt in get_plan():
    print(elmt)
    print(get_features(elmt['Plan']))
    print('\n')

