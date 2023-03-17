import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

def predict_emotions_rf(df, emotion):
    df_copy = df.copy()
    random_forest = joblib.load("./random_forest.joblib")
    prediction = random_forest.predict(df_copy)
    df_copy['mood'] = prediction
    return df_copy[df_copy['mood'] == emotion] 

def predict_emotions_nn(df, emotion):
    df_copy = df.copy()
    random_forest = joblib.load("./random_forest.joblib")
    prediction = random_forest.predict(df_copy)
    df_copy['mood'] = prediction
    return df_copy[df_copy['mood'] == emotion] 

