from turtle import shape
import pandas as pd
import numpy as np
import sklearn
import pickle
# Xay dung cay
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix
#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics
from memory_profiler import profile
@profile

def matrix(model, _features, y_test):
    y_pred = model.predict(_features)
    # Model Accuracy: how often is the classifier correct?
    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
    # Model Precision: what percentage of positive tuples are labeled as such?
    print("Precision:",metrics.precision_score(y_test, y_pred))
    # Model Recall: what percentage of positive tuples are labelled as such?
    print("Recall:",metrics.recall_score(y_test, y_pred))
    print(f"F1 score: {metrics.f1_score(y_test, y_pred)}")

    import matplotlib.pyplot as plt
    plot_confusion_matrix(model, _features, y_test)
    plt.show()

def load_decision_tree(_features, y_test):
    model = pickle.load(open("models/finalized_model.sav", 'rb'))
    matrix(model, _features, y_test)

def load_svm(_features, y_test):
    model = pickle.load(open("models/svm_model.sav", 'rb'))
    matrix(model, _features, y_test)

def load_xgb(_features, y_test):
    model = pickle.load(open("models/xgb_model.sav", 'rb'))
    matrix(model, _features, y_test)

def load_logreg(_features, y_test):
    model = pickle.load(open("models/logreg_model.sav", 'rb'))
    matrix(model, _features, y_test)

def load_knn(_features, y_test):
    model = pickle.load(open("models/knn_model.sav", 'rb'))
    matrix(model, _features, y_test)

def load_rdf(_features, y_test):
    model = pickle.load(open("models/rdf_model.sav", 'rb'))
    matrix(model, _features, y_test)

def load_Naive(_features, y_test):
    model = pickle.load(open("models/Naive_Bayes_model.sav", 'rb'))
    matrix(model, _features, y_test)

if __name__ == '__main__':
    df_pose = pd.read_csv("/home/zek/Thesis/stat_status_report.csv")
    df_label = pd.read_csv("/home/zek/Thesis/real_status_report.csv")

    _features = df_pose.iloc[:,0:]
    y_test = df_label.values.reshape(-1,1)

    load_decision_tree(_features, y_test)
    load_svm(_features, y_test)
    load_xgb(_features, y_test)
    load_logreg(_features, y_test)
    load_knn(_features, y_test)
    load_rdf(_features, y_test)
    load_Naive(_features, y_test)

    
