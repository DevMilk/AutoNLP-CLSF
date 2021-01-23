from .dataset.dataset import *

# Get Model
def getModel(model,init_arg):
    model_object = model(init_arg)
    print('{} was installed successfully!'.format(model))
    return model_object

def buildTreeByParamTree(param_tree):
    if(not isinstance(param_tree, dict) and not isinstance(param_tree, str)):
        if(isinstance(param_tree[1],str)): 
            return getModel(param_tree[0],*(param_tree[1],))
        return getModel(param_tree[0],*param_tree[1])

    tmp = param_tree.copy()
    for key in list(tmp.keys()):
        if(key=="DESC"):
            continue

        tmp[key] = buildTreeByParamTree(tmp[key])

    return tmp


