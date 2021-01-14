from .model_tree import *
#Get Model from dictionary by args
def getModelFromTree(args,model_tree=model_tree):
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


#Run method of model
def runMethodOfModel(methodName, args,material,model_tree=model_tree):
    results = []
    if(args[-1]=="ALL IN ONE"):
        for key in list(model_tree.keys()):
            for ml_model in list(model_tree[key].keys()):
                results.append(getattr(model_tree[key][ml_model], methodName)(*material))
        results = [most_frequent(results)]
    else:
        model =  getModelFromTree(args)
        results.append(getattr(model,methodName)(*material))

    return results

#Get simplified tree
def simplifyTree(model_tree=model_tree):
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