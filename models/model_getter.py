from .basic_bow_models import *
from .dataset import get_train_test_dataset, clean_data
import pandas as pd

def readAndNameCsv(data_path):
    return pd.read_csv(data_path,names=["class","text"],skiprows=[0])
    
def cleanAndSplit(data,split=0.2):

    #Determine which column is feature or target 
    cleaned_data = clean_data(data)
    if(len(cleaned_data["class"].unique()) > len(cleaned_data["text"].unique())):
        cleaned_data.rename(columns={'class': 'text', 'text':'class'},inplace=True) 

    return *get_train_test_dataset(cleaned_data,split),cleaned_data


def defineData(data_path,split=0.2):
    data = readAndNameCsv(data_path)
    return cleanAndSplit(data)
    

# NGRAM MODELS
def getModel(model,init_arg):
    model_object = model(init_arg)
    print('{} was installed successfully!'.format(model))
    return model_object

def getBasicBow(ml):
    return getModel(Direct_BOW_Model,ml)

# TF-IDF BOW MODELS
def getTfidfBow(ml):
    return getModel(TfIdf_BOW_Model,ml)



