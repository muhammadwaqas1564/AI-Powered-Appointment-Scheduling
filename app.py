from flask import Flask, request, jsonify
from datetime import datetime
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Sample data for model training
data = [
    [100, 9, 15], [101, 10, 30], [102, 11, 15], [103, 12, 60], [104, 13, 45],
    [500, 9, 15], [501, 10, 30], [502, 11, 15], [503, 12, 60], [504, 13, 45]
]
labels = [1, 1, 0, 0, 1, 1, 1, 0, 0, 1]  # 1: Appointment successful, 0: Conflict

# Split data
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

# Train the model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# To store scheduled appointments
scheduled_appointments = {}

# Available doctors and their patient ID ranges
doctors = {
    "Dr. Ahmad (Neurologist)": range(100, 500),
    "Dr. Fatima (Dermatologist)": range(500, 1000)
}

@app.route('/schedule', methods=['POST'])
def schedule_appointment():
    data = request.get_json()

    # Extract fields
    name = data['name']
    gender = data['gender']
    doctor = data['doctor']
    patient_id = int(data['patient_id'])
    requested_hour = int(data['requested_hour'])
    duration = int(data['duration'])
    appointment_date = data['appointment_date']

    # Validate doctor and patient ID
    if doctor not in doctors:
        return jsonify({"success": False, "message": "Invalid doctor selected."})
    
    if patient_id not in doctors[doctor]:
        return jsonify({"success": False, "message": f"Patient ID must be between {min(doctors[doctor])} and {max(doctors[doctor])} for {doctor}."})
    
    # Check if patient has already booked
    if doctor in scheduled_appointments:
        if any(appt['patient_id'] == patient_id for appt in scheduled_appointments[doctor]):
            return jsonify({"success": False, "message": f"Patient ID {patient_id} has already booked an appointment."})

        # Check for conflicting time slots
        for appointment in scheduled_appointments[doctor]:
            if appointment['date'] == appointment_date and appointment['hour'] == requested_hour:
                return jsonify({"success": False, "message": f"Appointment slot on {appointment_date} at {requested_hour}:00 is already taken."})
    
    # Schedule the appointment
    if doctor not in scheduled_appointments:
        scheduled_appointments[doctor] = []

    scheduled_appointments[doctor].append({
        'patient_id': patient_id,
        'name': name,
        'gender': gender,
        'hour': requested_hour,
        'duration': duration,
        'date': appointment_date
    })

    return jsonify({"success": True, "message": f"Appointment scheduled successfully for {name} with {doctor} on {appointment_date} at {requested_hour}:00 for {duration} minutes."})

if __name__ == "__main__":
    app.run(debug=True)
