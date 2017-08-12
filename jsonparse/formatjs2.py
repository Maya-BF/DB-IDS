import json
import pdb

def convert(jsondoc):
    json_data = open(jsondoc,'r+')
    jread = json.loads(json_data.read())
    print('pythondict: {}' .format(jread))
    walkjson(jread)

def walkjson(v,tree="",vcp="",openlist=False,opendict=False):
    #pdb.set_trace()
    #if(vcp is None):
    vcp = v.copy()
    if isinstance(v,list):
        for i,v2 in enumerate(v):
            openlist = True
            tree += '['
            if(isinstance(v2,str) or isinstance(v2,int)):
                tree += '[{}]' .format(v2)
                vcp.pop(i)
            else:
                walkjson(v2,tree,vcp,openlist,opendict)
            tree+= ']'
        if(opendict):
            tree += ')'
    elif isinstance(v,dict):
        tree += '('
        for k,v2 in v.items():
            opendict = True
            tree += '{}' .format(k)
            if(isinstance(v2,str) or isinstance(v2,int)):
                tree += '({})' .format(v2)
                vcp.pop(k)
            else:
                walkjson(v2,tree,vcp,openlist,opendict)
        tree += ')'
        if(openlist):
            tree += ']'

    if (not vcp):
        print(tree)
        print('END')

if __name__ == '__main__':
    #tab = {'A':{'B':'C'}}
    #walkjson(tab)
    convert('querytree.json')


