
from flask import Flask,request
from flask_cors import CORS
from joblib import load
import random
app = Flask(__name__)

CORS(app)
def calc_cal_per_day(age,weight,height,gender):
    if gender == 1:
      cal_per_day = 66.4730+(13.7516 *weight)+(5.0033 *height)-(6.7550 *age)
    elif gender == 0:
      cal_per_day = 655.0955 +(9.5634  *weight)+(1.8496   *height)-(4.6756 *age)
    return cal_per_day

model = load("Predictor_Velvets.joblib")
@app.route("/hackverse",methods = ['POST'])
def start():
    if request.method == 'POST':
        age = float(request.json["age"])
        gender = float(request.json["gender"])
        weight_kg = float(request.json["weight_kg"])
        height_cm = float(request.json["height_cm"])
        BMI_actual = weight_kg/((height_cm/100)**2)
        Lower_Weight = round((18*((height_cm/100)**2)))
        Ideal_Weight = round((21.5*((height_cm/100)**2))) #Generated by Backend,User may change it
        Higher_Weight = round((25*((height_cm/100)**2)))
        if int(weight_kg-Ideal_Weight)>2:  
            amount_overweight = weight_kg-Ideal_Weight
            cal_to_be_burnt_per_day = calc_cal_per_day(age,weight_kg,height_cm,gender)-calc_cal_per_day(age,Ideal_Weight,height_cm,gender)
            comment = f"You are OverWight by  {round(weight_kg-Ideal_Weight)}Kg\nCal to be burnt per day is {cal_to_be_burnt_per_day}"
        elif int(weight_kg-Ideal_Weight)<=2 and int(weight_kg-Ideal_Weight)>=0:
            amount_overweight = 0
            cal_to_be_burnt_per_day = 0
            comment = "You are overweight by less than 2kg ..so its not taken into account!!"
        else :
            amount_overweight = -1
            cal_to_be_burnt_per_day = 0
            comment = "You need to raise your Weight!!!"
        Actual_BF_precent = list(model.predict([[age,gender,height_cm,weight_kg]]))[0]
        Ideal_BF_precent = list(model.predict([[age,gender,height_cm,Ideal_Weight]]))[0]
        for i in range(5):
            id = random.randint(0,10)
            data['shoulders'][str(i)] = data_json['1']['shoulders'][str(id)]
            data['arms'][str(i)] = data_json['2']['arms'][str(id)]
            data['legs'][str(i)] = data_json['3']['legs'][str(id)]
            data['abs'][str(i)] = data_json['4']['abs'][str(id)]
            data['chest'][str(i)] = data_json['5']['chest'][str(id)]
        data = {
            'bmi_actual':BMI_actual,
            'lower_weight':Lower_Weight,
            'ideal_weight':Ideal_Weight,
            'higher_weight':Higher_Weight,
            'amount_overweight':amount_overweight,
            'cal_to_be_burnt_per_day':cal_to_be_burnt_per_day,
            'comment':comment,
            'actual_bf':Actual_BF_precent,
            'ideal_bf':Ideal_BF_precent,
             'shoulders':{

            },
            'arms':{

            },
            'legs':{

            },
            'abs':{

            },
            'chest':{

            },
        }
        return data

