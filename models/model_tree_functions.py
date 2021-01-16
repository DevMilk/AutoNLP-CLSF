from .model_tree import *
#Get Model from dictionary by args
def getModelFromTree(args,model_tree):
    model = model_tree[args[-1]]
    for arg in args[-2::-1]:
        model = model[arg]
    return model 

#Get Most frequent result
def most_frequent(List): 
    counter = 0
    num = List[0] 
      
    for i in List: 
        curr_frequency = List.count(i) 
        if(curr_frequency> counter): 
            counter = curr_frequency 
            num = i 
  
    return num 

#Get simplified tree
def runMethodForAll(methodName,material,model_tree):
    if(not isinstance(model_tree, dict) and not isinstance(model_tree, str)):
            return getattr(model_tree,methodName)(*material)

    allResults = []
    tmp = model_tree.copy()
    for key in list(tmp.keys()):

        if(key=="DESC"):
            continue

        newResult = runMethodForAll(methodName,material,model_tree=tmp[key])

        try:
            allResults += newResult
        except:
            allResults.append(newResult)

    return allResults


#Run method of model
def runMethodOfModel(methodName, args,material,model_tree):
    results = []
    if(args[-1]=="ALL IN ONE"):
        results = runMethodForAll(methodName,material)
        if(not isinstance(results,str)):
            results = [most_frequent(results)]
    else:
        model =  getModelFromTree(args,model_tree)
        results.append(getattr(model,methodName)(*material))

    return results

#Get simplified tree
def simplifyTree(model_tree):
    if(not isinstance(model_tree, dict)):
        if(not isinstance(model_tree, str)):
            return 0
        else:
            return model_tree

    allKeys = []
    tmp = model_tree.copy()
    for key in list(tmp.keys()):
        tmp[key] = simplifyTree(tmp[key])

    return tmp