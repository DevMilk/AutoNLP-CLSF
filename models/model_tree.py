from .models.basic_bow_models import *

data_path = "dataset/example_dataset.csv";


app_properties = {
    "title":"Title",
    "initial_input":"Initial Input",
    "initial_prediction": "Initial Prediction",
    "initial_description": "Initial Description"
}


param_tree = {
    "BOW":{

        "DESC": "Bag Of Words transforms texts to represent them as term count vector.",
        
        "BASIC": {
            "Random Forest" : 
                (Direct_BOW_Model,("RF")),
            "Multinomial Naive Bayes": 
                (Direct_BOW_Model,("MNB")),
            "SVC": 
                (Direct_BOW_Model,("SVC")),
            "Nearest Centroid" : 
                (Direct_BOW_Model,("NC")),
            "XGBoost": 
                (Direct_BOW_Model,("XGB")),
        },
        "TF-IDF": {
            "DESC": "TF-IDF combined by Bag Of Words takes term popularity into account.",

            "Random Forest" :  
                (TfIdf_BOW_Model,("RF")),
            "Multinomial Naive Bayes": 
                (TfIdf_BOW_Model,("MNB")),
            "SVC": 
                (TfIdf_BOW_Model,("SVC")),
            "Nearest Centroid" : 
                (TfIdf_BOW_Model,("NC")),
            "XGBoost": 
                (TfIdf_BOW_Model,("XGB")),
        }
    }

}