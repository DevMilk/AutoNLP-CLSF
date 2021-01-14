from .model_getter import *

data_path = "dataset/7allV03.csv";


app_properties = {
    "title":"Title",
    "initial_input":"Initial Input",
    "initial_prediction": "Initial Prediction",
    "initial_description": "Initial Description"
}


model_tree = {
    "BOW":{

        "DESC": "Bag Of Words transforms texts to represent them as term count vector.",
        
        "BASIC": {
            "Random Forest" : getBasicBow("RF"),
            "Multinomial Naive Bayes": getBasicBow("MNB"),
            "SVC": getBasicBow("SVC"),
            "Nearest Centroid" : getBasicBow("NC"),
            "XGBoost": getBasicBow("XGB")
        },
        "TF-IDF": {
            "DESC": "TF-IDF combined by Bag Of Words takes term popularity into account.",

            "Random Forest" : getTfidfBow("RF"),
            "Multinomial Naive Bayes": getTfidfBow("MNB"),
            "SVC": getTfidfBow("SVC"),
            "Nearest Centroid" : getTfidfBow("NC"),
            "XGBoost": getTfidfBow("XGB")
        }
    }

}