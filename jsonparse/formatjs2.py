import json
import pdb

def convert(jsondoc):
    '''
    CONVERT: Utility function that converts a json block into SVMLight format
    Input: Name of a json file
    '''
    json_data = open(jsondoc,'r+')
    jread = json.loads(json_data.read())
    print('pythondict: {}' .format(jread))
    walkjson(jread)

def walkjson(pyquery):
    global tree
    if isinstance(pyquery,list):
        tree += '('
        for value in pyquery:
            walkjson(value)
        tree+= ')'
    elif isinstance(pyquery,dict):
        tree += '('
        for key,value in pyquery.items():
            tree += '{}' .format(key)
            walkjson(value)
        tree += ')'
    else:
        tree += '({})' .format(pyquery)


if __name__ == '__main__':
    tree = ''
    convert('querytree.json')
    print(tree)
