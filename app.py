import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sys
print(f"Python version: {sys.version}")
print(f"Python path: {sys.executable}")
print("Debug: Starting app.py")
import sqlalchemy
import psycopg2

print(f"Python version: {sys.version}")
print(f"SQLAlchemy version: {sqlalchemy.__version__}")
print(f"psycopg2 version: {psycopg2.__version__}")
print(f"DATABASE_URL: {os.environ.get('DATABASE_URL')}")

# ... rest of your app.py code ...
app = Flask(__name__)
print("Debug: Flask app created")

# Configure the database
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///your_local_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
print("Debug: Database initialized")

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    roll = db.Column(db.Float)
    pitch = db.Column(db.Float)
    yaw = db.Column(db.Float)
    accel = db.Column(db.Text)  # Changed to Text for potentially long strings
    roll_time = db.Column(db.Text)  # Changed to Text for potentially long strings
    punch = db.Column(db.Integer)
    fastest_punch = db.Column(db.Float)
    avg_punch_per_min = db.Column(db.Float)

print("Debug: SensorData model defined")

@app.route('/sensor_data', methods=['POST'])
def receive_sensor_data():
    print("Debug: POST request received")
    try:
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
        print("Debug: Data saved successfully")
        return jsonify({"message": "Data received and stored successfully"}), 201
    except Exception as e:
        print(f"Debug: Error in POST request - {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route('/sensor_data', methods=['GET'])
def get_sensor_data():
    print("Debug: GET request received")
    try:
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
    except Exception as e:
        print(f"Debug: Error in GET request - {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    print("Debug: Home route accessed")
    return "Arduino Sensor Data API is running!"

@app.errorhandler(Exception)
def handle_error(e):
    print(f"Debug: An error occurred - {str(e)}")
    return jsonify({"error": str(e)}), 500

print("Debug: All routes defined")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Debug: Database tables created")
    
    port = int(os.environ.get('PORT', 5000))
    print(f"Debug: Starting Flask development server on port {port}")
    app.run(host='0.0.0.0', port=port)

print("Debug: End of app.py file")