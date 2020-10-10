from flask import Flask, request
import os


app = Flask(__name__)

@app.route("/")
def get():
    return request.args.get('apiKey')

def validate_key(provided_key):
    if provided_key == null:
        print('Key Not Found')
        return False
    if provided_key == os.environ.get('API_KEY'):
        return True
    else:
        print('Key Incorrect')
        return False
