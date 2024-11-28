from flask import Flask, request, jsonify
import boto3
import os

app = Flask(__name__)

sns = boto3.client('sns', 
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN")  # Solo si usas tokens temporales
)

@app.route('/notificaciones', methods=['POST'])
def enviar_notificacion():
    data = request.json
    if not data.get('correo') or not data.get('mensaje'):
        return jsonify({'error': 'Correo y Mensaje son requeridos'}), 400

    try:
        mensaje = data['mensaje']
        if data.get('url_pdf'):  # Si se incluye el enlace del PDF
            mensaje += f"\n\nPuedes descargar tu nota de venta aquí: {data['url_pdf']}"

        sns.publish(
            TopicArn=os.getenv("SNS_TOPIC_ARN"),
            Message=mensaje,
            Subject="Notificación de Nota de Venta",
            MessageStructure='string'
        )
        return jsonify({'mensaje': 'Notificación enviada exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
