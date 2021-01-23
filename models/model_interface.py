class Model_Interface:
  def get_params(self):
    pass
  def updateModel(self,model):
    pass
  def set_params_of_model(self,params):
    pass
  def fit(self, X_train, y_train):
    pass
  def predict(self, text):
    pass
  def evaluate(self, X_test, y_test):
    pass