from flask import Flask, request, jsonify
import boto3
import os

app = Flask(__name__)

sns = boto3.client('sns', region_name=os.getenv("AWS_REGION"))

@app.route('/notificaciones', methods=['POST'])
def enviar_notificacion():
    data = request.json
    if not data.get('correo') or not data.get('mensaje'):
        return jsonify({'error': 'Correo y Mensaje son requeridos'}), 400

    try:
        sns.publish(
            TopicArn=os.getenv("SNS_TOPIC_ARN"),
            Message=data['mensaje'],
            Subject="Notificación",
            MessageStructure='string'
        )
        return jsonify({'mensaje': 'Notificación enviada exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
