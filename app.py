from flask import Flask, jsonify, request, render_template
from flask_dropzone import Dropzone
from io import StringIO
import os
from flask_session import Session
from flask_caching import Cache
from .models.model_tree_functions import defineData, buildTreeByParamTree,runMethodOfModel, simplifyTree,\
                                            get_train_test_dataset
from .models.model_tree import *
app = Flask(__name__, template_folder='templates')


app.secret_key = "super secret key"
config = {
    # Dropzone settings
    "DROPZONE_UPLOAD_MULTIPLE": True,
    "DROPZONE_MAX_FILE_SIZE": 1024,
    "DROPZONE_ALLOWED_FILE_CUSTOM": True,
    "DROPZONE_ALLOWED_FILE_TYPE": '.csv, .xlsx, .xls',
    "CACHE_TYPE": "simple", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 0
}
app.config.from_mapping(config)
session =  Session(app)
cache = Cache(app)
dropzone = Dropzone(app)


#------------------------------Page Endpoints----------------------------


#Index page
@cache.cached(timeout=120)
@app.route('/', methods= ["GET"])
def hello():
    return render_template("index.html", properties=app_properties);


#Get model tree
@app.route('/model-tree')
@cache.cached(timeout=120)
def getStructure():
    try:
        session.model_tree
    except:
        session.X_train,session.X_test,session.y_train,session.y_test,session.cleaned_data = defineData(data_path)
        session.model_tree = buildTreeByParamTree(param_tree)
    return jsonify(simplifyTree(session.model_tree))

#------------------------------METHOD ENDPOINTS----------------------------


#Get parameters of model
@app.route('/param', methods= ["POST"])
def get_param(): 
    parameters = request.get_json()
    args = parameters.get("args")
    return jsonify(runMethodOfModel("get_params", args,(),session.model_tree))


#Split Dataset
@app.route("/split",methods = ["POST"])
def change_split():
    try:
        parameters = request.get_json()
        test_ratio = parameters.get("test_ratio")
        session.X_train, session.X_test, session.y_train, session.y_test = get_train_test_dataset(session.cleaned_data,test_ratio)
        return jsonify(["Data Splitted with {} test data ratio".format(test_ratio)])
    except Exception as e:
        print(e)
        return jsonify(["Error on splitting dataset"])


#Make the model predict
@app.route('/predict', methods= ["POST"])
def predict():
    try:
        parameters = request.get_json()
        text = parameters.get("text")
        args = parameters.get("args")
        return jsonify(runMethodOfModel("predict",args,[text],session.model_tree))
    except Exception as e:
        print("Error "+str(e))
        return jsonify(["Model Not Trained"])


#Test the current model and return test accuracy
@app.route('/test', methods= ["POST"])
def test(): 
    parameters = request.get_json()
    args = parameters.get("args")
    try:
        return jsonify(runMethodOfModel("evaluate", args, (session.X_test,session.y_test),session.model_tree))
    except:
        return jsonify(["Model Not Trained"])


#Train the current model and return train accuracy
@app.route('/train', methods= ["POST"])
def train(): 
    try:
        parameters = request.get_json()
        args = parameters.get("args")
        params = parameters.get("params") #must be a dict
        if(params!=None):
            runMethodOfModel("set_params_of_model",args,[(params)],session.model_tree)
        runMethodOfModel("fit",args,(session.X_train,session.y_train),session.model_tree)
        return jsonify(["Training Success"])
    except Exception as e:
        print(e)
        return jsonify(["ERROR ON TRAINING"])


@app.route('/setDataset', methods= ["POST"])
def setDataset():
    try:
        print("uploading...")
        if request.method == 'POST':
            data_file = request.files.get("file[0]")
            session.X_train,session.X_test,session.y_train,session.y_test,session.cleaned_data = \
                defineData(StringIO(data_file.read().decode("utf-8")))
        return jsonify(["UPLOAD SUCCESSFULL"])
    except Exception as e:
        print("Error "+str(e))
        return jsonify(["UPLOAD FAILED"])


#--------------------------------------------------------------------------

if __name__ == '__main__':
  app.run()