from .preprocessing import clean_text
from sklearn.model_selection import train_test_split
import pandas as pd

def clean_data(data):
    cleaned_data = data.copy()
    cleaned_data["text"] = data["text"].apply(lambda x: clean_text(x, remove_whitespaces=False))
    return cleaned_data

def get_train_test_dataset(cleaned_data,test_ratio=0.2):
    return train_test_split(cleaned_data["text"],cleaned_data["class"],test_size=test_ratio)


def readAndNameCsv(data_path):
    return pd.read_csv(data_path,names=["class","text"],skiprows=[0])
    
def cleanAndSplit(data,split=0.2):

    #Determine which column is feature or target 
    cleaned_data = clean_data(data)
    if(len(cleaned_data["class"].unique()) > len(cleaned_data["text"].unique())):
        cleaned_data.rename(columns={'class': 'text', 'text':'class'},inplace=True) 

    return train_test_split(cleaned_data["text"],cleaned_data["class"],test_size=split),cleaned_data


def defineData(data_path,split=0.2):
    data = readAndNameCsv(data_path)
    return cleanAndSplit(data)