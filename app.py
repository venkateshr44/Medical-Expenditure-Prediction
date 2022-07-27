from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('RandomForestRegressor.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

standard_to = StandardScaler()

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        age = int(request.form['age'])
        bmi = float(request.form['BMI'])
        children=int(request.form['children'])
        sex_male = request.form['sex_male']
        if(sex_male=='Male'):
            sex_male = 1
        else:
            sex_male = 0
        smoker_yes = request.form['smoker_yes']
        if(smoker_yes=='Yes'):
            smoker_yes = 1
        else:
            smoker_yes = 0
        region_northwest = 0
        region_southeast = 0
        region_southwest = request.form['region_southwest']
        if(region_southwest=='SouthWest'):
            region_southwest = 1
            region_southeast = 0
            region_northwest = 0
        elif(region_southwest=='SouthEast'):
            region_southwest = 0
            region_southeast = 1
            region_northwest = 0
        elif(region_southwest=='NorthWest'):
            region_southwest = 0
            region_southeast = 0
            region_northwest = 1
        else:
            region_southwest = 0
            region_southeast = 0
            region_northwest = 0
        prediction=model.predict([[sex_male,smoker_yes,region_northwest,region_southeast,region_southwest,age,bmi,children]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_text="Patient has no expenditure")
        else:
            return render_template('index.html',prediction_text="Expenditure of a patient is {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
	app.run(debug=True)