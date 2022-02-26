
from flask import Flask,request

app = Flask(__name__)

@app.route("/hackverse",methods = ['POST'])
def start():
    if request.method == 'POST':
        data = {
            'key':'MBSAIADITYA',
            'value':{
                '1':'This is what I was talkig about.'
            }
        }
        return data


