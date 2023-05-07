from flask import Flask, render_template, escape, request
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)
model = pickle.load(open('logreg_model.pkl','rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction',methods=['POST'])
def predict():
	'''
	data = request.get_json(force=True)
	features = [np.array(data['data'])]
	prediction = model.predict(features)
	return str(prediction[0])
	'''
	if request.method == 'POST':
		# Get the data from form
		name = request.form['name']
		home_team = request.form['home-team']
		away_team = request.form['away-team']
		HCD = float(request.form['HCD'])
		HSD = float(request.form['HSD'])
		HSTD = float(request.form['HSTD'])
		HFD = float(request.form['HFD'])

		features = [np.array([HCD, HSD, HSTD, HFD])]
		pred = model.predict(features)
		prediction_result = pred[0]

		# Determine the output
		if int(prediction_result) == 0:
			prediction = 'Dear Mr/Mrs/Ms {name}, {home_team} will win!'.format(name = name, home_team=home_team)
		elif int(prediction_result) == 1:
			prediction = 'Dear Mr/Mrs/Ms {name}, {home_team} VS {away_team} will be draw!'.format(name = name, home_team=home_team, away_team=away_team)
		else:
			prediction = 'Sorry Mr/Mrs/Ms {name}, {away_team} will win!'.format(name = name, away_team=away_team)

		return render_template('prediction.html', prediction = prediction)
		
	else:
		return render_template('error.html')
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')