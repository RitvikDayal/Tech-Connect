import pickle
import pandas as pd
import numpy as np
import sklearn

def ml_model(model_file, X_test):
    model = pickle.load(open(model_file, 'rb'))
    preds = model.predict(X_test)
    return pd.DataFrame(preds, columns=['results'])
