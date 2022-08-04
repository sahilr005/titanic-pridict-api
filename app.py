from ast import If
from flask import Flask,request
import pandas as pd
import flasgger
from flasgger import Swagger
import pickle 
import sys


app = Flask(__name__)
Swagger(app)

pickle_in =open("titanic_pred1.pkl","rb")
model = pickle.load(pickle_in)

@app.route("/")
def welcome():
    return "Hello sahil"
# Pclass Sex	Age	SibSp	Parch	Fare	Embarke
def predict_res(prediction):
    rs = ""
    if prediction == 1:
        rs = "been"
    else:
        rs = "not"
    return "The Passenger has "+ rs +" Survived"

@app.route("/predict")
def titanic_pred():

    '''
    Titanic Data Predict.
    ---
    parameters:
        - name: pclass
          in: query
          type: number
          r equired: true
        - name: sex
          in: query
          type: number 
          required: true
        - name: age
          in: query
          type: number 
          required: true
        - name: sibSp
          in: query
          type: number 
          required: true
        - name: parch
          in: query
          type: number 
          required: true
        - name: fare
          in: query
          type: number 
          required: true 
        - name: embarked
          in: query
          type: number 
          required: true 
    responses:
        200:
            description: OutPut Val
    '''

    pclass = request.args.get("pclass", type = int)
    sex = request.args.get("sex", type = int)
    age = request.args.get("age", type = int)
    sibSp = request.args.get("sibSp", type = int)
    parch = request.args.get("parch", type = int)
    fare = request.args.get("fare" ,type = int)
    embarked = request.args.get("embarked" ,type = int)
    prediction = model.predict([[pclass,sex,age,sibSp,parch,fare,embarked]]) 
    # prediction = model.predict([[1,2,38,1,0,71,20.3]])
    # return "The Passenger has "+ predict_res(prediction) +" Survived"
    return "The Passenger has "+" Survived"

@app.route("/prdict/file",methods=["POST"])
def titanic_pred_file():
    
    '''
    Titanic Data Predict.
    ---
    parameters:
        - name: file
          in: formData
          type: file
          required: true
    responses:
        200:
            description: OutPut Val
    '''

    df = pd.read_csv(request.files.get("file"))
    prediction = model.predict(df)
    return "The Passenger has "+  predict_res(prediction) +" Survived"

if __name__ =="__main__":
    app.run()