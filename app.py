from flask import Flask, jsonify, request
from flask import render_template



from .models.model_getter import *

shorten = {
    "Random Forest": "RF",
    "Multinomial Naive Bayes" : "MNB",
    "Nearest Centroid": "NC",
    "XGBoost": "XGB"
}

def simplifyDict(dictionary):
    if(not isinstance(dictionary, dict)):
        return 0

    allKeys = []
    tmp = dictionary
    for key in list(tmp.keys()):
        val = simplifyDict(tmp[key])

    return tmp



Model_dict = {
    "BOW":{

        "BASIC": {
            "RF" : getBasicBow("RF"),
            "MNB": getBasicBow("MNB"),
            "SVC": getBasicBow("SVC"),
            "NC" : getBasicBow("NC"),
            "XGB": getBasicBow("XGB")
        },
        "TF-IDF": {
            "RF" : getTfidfBow("RF"),
            "MNB": getTfidfBow("MNB"),
            "SVC": getTfidfBow("SVC"),
            "NC" : getTfidfBow("NC"),
            "XGB": getTfidfBow("XGB")
        }
    }

}

#TODO: Model_dict'in son değer olmadan olan structure'sini çıkar, Javascript'e aktar, javascript de o structure'yi html olarak üretsin 

app = Flask(__name__, template_folder='templates')




def shortenModelName(modelName):
    try:
        return shorten[modelName]
    except:
        return modelName

def getModelFromDict(args):
    for i,arg in enumerate(args):
        args[i] = shortenModelName(arg)

    model = Model_dict[args[-1]]
    for arg in args[-2::-1]:
        model = model[arg]
    return model 


def most_frequent(List): 
    counter = 0
    num = List[0] 
      
    for i in List: 
        curr_frequency = List.count(i) 
        if(curr_frequency> counter): 
            counter = curr_frequency 
            num = i 
  
    return num 


def runMethodOfModel(methodName, args,material):
    results = []
    if(args[-1]=="ALL IN ONE"):
        for key in list(Model_dict.keys()):
            for ml_model in list(Model_dict[key].keys()):
                results.append(getattr(Model_dict[key][ml_model], methodName)(*material))
        results = [most_frequent(results)]
    else:
        model =  getModelFromDict(args)
        results.append(getattr(model,methodName)(*material))

    return results

@app.route('/')
def hello():
    return render_template("index.html",jsonify(Model_dict));


#Make the model predict

@app.route('/predict', methods= ["POST"])
def predict():
    parameters = request.get_json()
    text = parameters.get("text")
    args = parameters.get("args")

    return jsonify(runMethodOfModel("predict",args,[text]))

#Verisetini boler
@app.route("/split",methods = ["POST"])
def change_split():
    global X_train,y_train,X_test,y_test
    try:
        parameters = request.get_json()
        test_ratio = parameters.get("test_ratio")
        X_train, X_test, y_train, y_test = get_train_test_dataset(cleaned_data,test_ratio)
        return jsonify(["Data Splitted with {} test data ratio".format(test_ratio)])
    except Exception as e:
        print(e)
        return jsonify(["Error on splitting dataset"])

#Train the current model and return train accuracy

@app.route('/train', methods= ["POST"])
def train(): 
    try:
        parameters = request.get_json()
        args = parameters.get("args")
        params = parameters.get("params") #must be a dict
        runMethodOfModel("set_params_of_model",args,[(params)])
        runMethodOfModel("fit",args,(X_train,y_train))
        return jsonify(["Training Success"])
    except Exception as e:
        print(e)
        return jsonify(["ERROR ON TRAINING"])

#Test the current model and return test accuracy

@app.route('/test', methods= ["POST"])
def test(): 
    parameters = request.get_json()
    args = parameters.get("args")
    return jsonify(runMethodOfModel("evaluate", args, (X_test,y_test)))


@app.route('/param', methods= ["POST"])
def get_param(): 
    parameters = request.get_json()
    args = parameters.get("args")
    return jsonify(runMethodOfModel("get_params", args,(0,0)))


if __name__ == '__main__':
  app.run()