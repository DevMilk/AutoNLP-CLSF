from flask import Flask, jsonify, request
from flask import render_template
from .models.model_tree_functions import *


app = Flask(__name__, template_folder='templates')

X_train,X_test,y_train,y_test,cleaned_data = defineData(data_path)

#------------------------------Page Endpoints----------------------------


#Index page
@app.route('/', methods= ["GET"])
def hello():
    return render_template("index.html",properties =app_properties);



#Get model tree
@app.route('/model-tree')
def getStructure():
    return jsonify(simplifyTree())


#------------------------------METHOD ENDPOINTS----------------------------


#Get parameters of model
@app.route('/param', methods= ["POST"])
def get_param(): 
    parameters = request.get_json()
    args = parameters.get("args")
    return jsonify(runMethodOfModel("get_params", args,(0,0)))


#Split Dataset
@app.route("/split",methods = ["POST"])
def change_split():
    try:
        parameters = request.get_json()
        test_ratio = parameters.get("test_ratio")
        X_train, X_test, y_train, y_test = get_train_test_dataset(cleaned_data,test_ratio)
        return jsonify(["Data Splitted with {} test data ratio".format(test_ratio)])
    except Exception as e:
        print(e)
        return jsonify(["Error on splitting dataset"])


#Make the model predict
@app.route('/predict', methods= ["POST"])
def predict():
    parameters = request.get_json()
    text = parameters.get("text")
    args = parameters.get("args")
    try:
        return jsonify(runMethodOfModel("predict",args,[text]))
    except:
        return jsonify(["Model Not Trained"])

#Test the current model and return test accuracy
@app.route('/test', methods= ["POST"])
def test(): 
    parameters = request.get_json()
    args = parameters.get("args")
    try:
        return jsonify(runMethodOfModel("evaluate", args, (X_test,y_test)))
    except:
        return jsonify(["Model Not Trained"])

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

#--------------------------------------------------------------------------

if __name__ == '__main__':
  app.run()