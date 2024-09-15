import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///sensor_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    roll = db.Column(db.Float)
    pitch = db.Column(db.Float)
    yaw = db.Column(db.Float)
    accel = db.Column(db.String)  # Store as comma-separated string
    roll_time = db.Column(db.String)  # Store as comma-separated string
    punch = db.Column(db.Integer)
    fastest_punch = db.Column(db.Float)
    avg_punch_per_min = db.Column(db.Float)

@app.route('/sensor_data', methods=['POST'])
def receive_sensor_data():
    data = request.json
    new_data = SensorData(
        roll=data['Roll'],
        pitch=data['Pitch'],
        yaw=data['Yaw'],
        accel=','.join(map(str, data['Accel/Time'])),
        roll_time=','.join(map(str, data['Roll/Time'])),
        punch=data['Punch'],
        fastest_punch=data['Fastest Punch'],
        avg_punch_per_min=data['Average punch / min']
    )
    db.session.add(new_data)
    db.session.commit()
    
    return jsonify({"message": "Data received and stored successfully"}), 201

@app.route('/sensor_data', methods=['GET'])
def get_sensor_data():
    latest_data = SensorData.query.order_by(SensorData.timestamp.desc()).first()
    if latest_data:
        return jsonify({
            "Roll": latest_data.roll,
            "Pitch": latest_data.pitch,
            "Yaw": latest_data.yaw,
            "Accel/Time": [float(x) for x in latest_data.accel.split(',')],
            "Roll/Time": [float(x) for x in latest_data.roll_time.split(',')],
            "Punch": latest_data.punch,
            "Fastest Punch": latest_data.fastest_punch,
            "Average punch / min": latest_data.avg_punch_per_min
        })
    else:
        return jsonify({"message": "No data available"}), 404

@app.route('/', methods=['GET'])
def home():
    return "Arduino Sensor Data API is running!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))