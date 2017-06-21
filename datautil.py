#Python data utility module
'''
def nodetypetoreal(value):
    #List of all node types
    nodetypes = ['result','projectset','insert','update','delete',
                 'append','mergeappend','recursiveunion','bitmapand','bitmapor',
                 'nestedloop','merge','seqscan','samplescan','gather',
                 'gathermerge','indexscan','indexonlyscan','bitmapindexscan','tidscan',
                 'subqueryscan','functionscan','bitmapheapscan','tablefunctionscan','valuesscan',
                 'ctescan','namedtuplestorescan','worktablescan','foreignscan','foreigninsert',
                 'foreignupdate','foreigndelete','materialize','sort','group',
                 'aggregate','groupaggregate','mixedaggregate','windowagg','unique',
                 'setop','hashsetop','lockrows','limit','hash']
    return(enumtoreal(nodetypes,value))
'''
def clean_name(*more):
    #n = name.replace(" ","").lower()
    if(more):
        names = [m.replace(" ",'').lower() for m in more]
        return(names)

def enumtoreal(enum_list,val):
    #leave 0 value to empty vals
    enum_ind = {k:float(i)+1 for i,k in enumerate(enum_list)}
    return(enum_ind.get(val,'null'))

#print(nodetypetoreal("hash"))
