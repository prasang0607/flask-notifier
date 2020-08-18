from flask import Flask, request, jsonify
from config import config
from boto3 import client

app = Flask(__name__)
app.secret_key = '&@)g(^$*s&^*@&$(c^&^!sd$^*&^%*@$%'


@app.route('/NotifyPS', methods=['POST'])
def hello_world():
    json_request = request.get_json()

    if json_request['x-api-key'] != config['API_KEY']:
        return jsonify(message='invalid api key'), 400

    try:
        sns = client(
            'sns',
            region_name=config['AWS_REGION'],
            aws_access_key_id=config['ACCESS_KEY'],
            aws_secret_access_key=config['SECRET_KEY']
        )

        if 9 < json_request.get('hour', config['DEFAULT_HOUR']) < 21:
            sns.publish(
                TopicArn=config['TOPIC_ARN_FOR_SMS'],
                Message=config['MESSAGE']
            )
        else:
            sns.publish(
                TopicArn=config['TOPIC_ARN_FOR_EMAIL'],
                Subject='Battery Alert!',
                Message=config['MESSAGE']
            )

        return jsonify(message='message sent'), 200
    except Exception as e:
        return jsonify(message='something went wrong'), 400
