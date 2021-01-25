<h1 align="center">Automated Text Classifier Builder Web Service</h1>
    
---
## Usage    

1.  Drag and drop a dataset.
2.  Choose a text classification method.
3.  Send parameters and wait for the training to finish.

After the training is over, user can now: 
-  Evaluate Trained AI Model and see metrics like F1 Score, Accuracy and Confusion Matrix
-  Make the Trained AI Classify given Input
-  Optionally change train-test split of dataset 

<br>
<br>
<br>
<p align="center">
    <img src="https://github.com/DevMilk/AutoNLPClassifier/blob/for_heroku/usage/usage.gif">
</p>            

<p align="center">
  <img width =704 height=396 src="https://github.com/DevMilk/AutoNLPClassifier/blob/for_heroku/usage/screenshot.png">
</p>        
<p align="center">
  <img width =704 height=396 src="https://github.com/DevMilk/AutoNLPClassifier/blob/for_heroku/usage/screenshot2.png">
</p>       

---

## Automated Properties

-  Text preprocessing (Lemmatization, stopwords removal etc. )
-  HTML form generation based on parameters of method
-  HTML menu generation based on model tree dictionary on Python code
-  Model initialization on model tree from parameter tree
-  Model training, evaluation, prediction and parameter change implementation
-  Server-side session per user
-  Caching
---

## Features for Developers/Contributors    

-  Easy model implementation/extension using Model Interface
-  Model Choice Tree is generated by converting model_tree dictionary on Python to model choice tree HTML elements by Javascript 
<br>
<br>
<br>
<p align="center">
    <img src="https://github.com/DevMilk/AutoNLPClassifier/blob/for_heroku/usage/screenshot3.png">
</p>     

---
## Setup Directions


    pip install -r requirements.txt
    flask run


