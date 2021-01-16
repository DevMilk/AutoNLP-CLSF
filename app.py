from flask import Flask, jsonify, request, render_template,session
from flask_dropzone import Dropzone
from io import StringIO


from .models.model_tree_functions import *
import os
app = Flask(__name__, template_folder='templates')

X_train,X_test,y_train,y_test,cleaned_data = defineData(data_path)

# Dropzone settings
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_MAX_FILE_SIZE'] = 1024
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = '.csv, .xlsx, .xls'
app.secret_key = "super secret key"

dropzone = Dropzone(app)

model_tree = buildTreeByParamTree(param_tree)
#------------------------------Page Endpoints----------------------------


#Index page
@app.route('/', methods= ["GET"])
def hello():
    return render_template("index.html", properties=app_properties);


#Get model tree
@app.route('/model-tree')
def getStructure():
    return jsonify(simplifyTree(model_tree))

#------------------------------METHOD ENDPOINTS----------------------------


#Get parameters of model
@app.route('/param', methods= ["POST"])
def get_param(): 
    parameters = request.get_json()
    args = parameters.get("args")
    return jsonify(runMethodOfModel("get_params", args,(0,0),model_tree))


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
    try:
        parameters = request.get_json()
        text = parameters.get("text")
        args = parameters.get("args")
        return jsonify(runMethodOfModel("predict",args,[text],model_tree))
    except:
        return jsonify(["Model Not Trained"])


#Test the current model and return test accuracy
@app.route('/test', methods= ["POST"])
def test(): 
    parameters = request.get_json()
    args = parameters.get("args")
    try:
        return jsonify(runMethodOfModel("evaluate", args, (X_test,y_test),model_tree))
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
            runMethodOfModel("set_params_of_model",args,[(params)],model_tree)
        runMethodOfModel("fit",args,(X_train,y_train),model_tree)
        return jsonify(["Training Success"])
    except Exception as e:
        print(e)
        return jsonify(["ERROR ON TRAINING"])


@app.route('/setDataset', methods= ["POST"])
def setDataset():
    global X_train,X_test,y_train,y_test,cleaned_data
    try:
        print("uploading...")
        if request.method == 'POST':
            data_file = request.files.get("file[0]")
            X_train,X_test,y_train,y_test,cleaned_data = defineData(StringIO(data_file.read().decode("utf-8")))
            
            """session["cleaned_data"] = cleaned_data;
            session["X_train"] = X_train
            session["X_test"] = X_test
            session["y_train"] = y_train
            session["y_test"] = y_test"""

        #cleaned_data = cleanAndSplit(csv_file)
        return jsonify(["UPLOAD SUCCESSFULL"])
    except Exception as e:
        print("Error "+str(e))
        return jsonify(["UPLOAD FAILED"])


#--------------------------------------------------------------------------

if __name__ == '__main__':
  app.run()