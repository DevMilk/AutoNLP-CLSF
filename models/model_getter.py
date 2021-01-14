from .basic_bow_models import *
from .dataset import get_train_test_dataset, read_original_data
import pandas as pd


def defineData(data_path):
    cleaned_data = read_original_data(pd.read_csv(data_path,names=["class","text"],skiprows=[0]))
    return *get_train_test_dataset(cleaned_data),cleaned_data

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



