from flask import Flask,render_template,request
from joblib import load
import numpy as np

app = Flask(__name__,template_folder='templates',static_folder='static')

model = load('ml_model/random_forest_model.joblib')
scaler = load('ml_model/scaler.joblib')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=["POST"])
def submit():
    if request.method == "POST":
        age = int(request.form.get('age'))
        cycle_length = int(request.form.get('cycle_length'))
        period_duration = int(request.form.get('period_duration'))
        flow_intensity = int(request.form.get('flow_intensity'))
        pms_score = int(request.form.get('pms_score'))
        spotting = int(request.form.get('spotting'))
        stress_level = int(request.form.get('stress_level'))

        input_data = np.array([[age, cycle_length, period_duration, flow_intensity, pms_score, spotting, stress_level]])
        input_data_scaled = scaler.transform(input_data)


        prediction = model.predict(input_data_scaled)[0]
        

        print(prediction)
        flow_label = {0: "Light", 1: "Medium"}.get(flow_intensity, "Heavy")
        prediction = "abnormal" if prediction==1 else "normal"
        spotting_label = "No "if spotting==0 else "Yes"

        return render_template('result.html',
                               prediction=prediction,
                               age=int(age),
                               cycle_length=int(cycle_length),
                               period_duration=int(period_duration),
                               flow_intensity=flow_label,
                               pms_score=int(pms_score),
                               spotting=spotting_label,
                               stress_level=int(stress_level))
if __name__ == '__main__':
    app.run(debug=True)