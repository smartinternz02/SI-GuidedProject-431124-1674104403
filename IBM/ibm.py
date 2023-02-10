import numpy as np
from flask import Flask, request, jsonify, render_template

#importing the inputScript file used to analyze the URL
import inputScript 

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "wQPxYr142xRdm7h5Kh43LXIAvRblAm06HNJ5ZwA5ANwY"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
#load model
app = Flask(__name__)



#Redirects to the page to give the user iput URL.
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict')
def predict():
    return render_template('final.html')

#Fetches the URL given by the URL and passes to inputScript
@app.route('/y_predict',methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    url = request.form['URL']
    checkprediction = inputScript.main(url)
    payload_scoring = {
           "input_data": [
                   {
                           "fields": [
                                   "index",
                                   "having_IPhaving_IP_Address",
                                   "URLURL_Length",
                                   "Shortining_Service",
                                   "having_At_Symbol",
                                   "double_slash_redirecting",
                                   "Prefix_Suffix",
                                   "having_Sub_Domain",
                                   "SSLfinal_State",
                                   "Domain_registeration_length",
                                   "Favicon",
                                   "port",
                                   "HTTPS_token",
                                   "Request_URL",
                                   "URL_of_Anchor",
                                   "Links_in_tags",
                                   "SFH",
                                   "Submitting_to_email",
                                   "Abnormal_URL",
                                   "Redirect",
                                   "on_mouseover",
                                   "RightClick",
                                   "popUpWidnow",
                                   "Iframe",
                                   "age_of_domain",
                                   "DNSRecord",
                                   "web_traffic",
                                   "Page_Rank",
                                   "Google_Index",
                                   "Links_pointing_to_page",
                                   "Statistical_report"
                           ],
                           "values": checkprediction}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/d35291ad-94b0-4257-afd0-86dc7f82c6eb/predictions?version=2023-01-30', json=payload_scoring,
     headers={'Authorization': 'Bearer ' + mltoken})
    print(response_scoring.json())
    pred=response_scoring.json()
    output=pred['predictions'][0]['values'][0][0]
   
    if(output==1):
        pred="Your are safe!!  This is a Legitimate Website."
        
    else:
        pred="You are on the wrong site. Be cautious!"
    return render_template('final.html', prediction_text='{}'.format(pred),url=url)



if __name__ == "__main__":
    app.run(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
