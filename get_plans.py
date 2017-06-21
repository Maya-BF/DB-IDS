#!/usr/bin/python3
import sys
import csv
import re
import json
import datautil as du

list_features = []
'''-------------Feature List----------------'''

features = ['Node Type','Join Type','Command','Startup Cost',
            'Total Cost','Plan Rows','Plan Width','Output','Index Cond',
            'Order By','Recheck Cond','Filter','Workers Planned','Function Call',
            'TID Cond','Join Filter','Merge Cond','Hash Cond','One-Time Filter',
            'Strategy','Partial Mode','Operation','Parent Relationship',
            'Custom Plan Provider','Parallel Aware','Schema','Alias']

'''---------------Enum type lists-----------------'''

#List of all node types
nodetype = ['result','projectset','insert','update','delete',
             'append','mergeappend','recursiveunion','bitmapand','bitmapor',
             'nestedloop','merge','seqscan','samplescan','gather',
             'gathermerge','indexscan','indexonlyscan','bitmapindexscan','tidscan',
             'subqueryscan','functionscan','bitmapheapscan','tablefunctionscan','valuesscan',
             'ctescan','namedtuplestorescan','worktablescan','foreignscan','foreigninsert',
             'foreignupdate','foreigndelete','materialize','sort','group',
             'aggregate','groupaggregate','mixedaggregate','windowagg','unique',
             'setop','hashsetop','lockrows','limit','hash']
jointype = ['Left','Full','Right','Semi','Anti']
command = ['Intersect','Intersect All','Except','Except All']
strategy = ['Plain','Sorted','Hashed','Mixed','Sorted','Hashed']
partialmode = ['Partial','Finalize','Simple']
operation = ['Insert','Update','Delete']
parentrelationship = ['Inner','Outer','Null']
enum_dict = {'nodetype':nodetype,'jointype':jointype,'command':command,'strategy':strategy,
             'partialmode':partialmode,'operation':operation,'parentrelationship':parentrelationship}

'''-----------------Int type feature list ------- '''
int_features = ['startupcost','totalcost','planrows','planwidth','workersplanned','parallelaware']
bool_features= ['parallelaware']

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

def valtoreal(feature,value):
    '''Assigns the right function from transtype module to the correspondent data type to transform it to real.'''
    '''trans_funcs = (nodetypetoreal,jointypetoreal,commandtoreal,startupcosttoreal,totalcosttoreal,
                   planrowtoreal,planwidthtoreal,outputtoreal,indexcondtoreal,orderbytoreal,
                   recheckcondtoreal,filtertoreal,workersplannedtoreal,funccalltoreal,
                   tidcondtoreal,joinfiltertoreal,mergecondtoreal,hashcondtoreal,onetimefiltertoreal,
                   strategytoreal,partialmodetoreal,operationtoreal,parentrelationshiptoreal,
                   customplanprotoreal,parallelawaretoreal,schematoreal,aliastoreal)
    '''
    feature,value = du.clean_name(feature,value)
    if(feature in enum_dict.keys()): return(du.enumtoreal(enum_dict[feature],value))
    elif(feature in int_features): return(float(value))
    elif(feature in bool_features): return(float(int(value)))
    else:
        print("%s is not of a known type." .format(feature))
        return(0)

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
'''init_csv()
feature_vect = []
feature_vect.append(u'Query Text')
for elmt in get_plan():
    print(elmt)
    print(get_features(elmt['Plan']))
    print('\n')
    '''
print(valtoreal('parallelaware','true'))
