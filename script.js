document.getElementById('appointmentForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    
    const name = document.getElementById('name').value;
    const gender = document.getElementById('gender').value;
    const doctor = document.getElementById('doctor').value;
    const patientId = document.getElementById('patientId').value;
    const hour = document.getElementById('hour').value;
    const duration = document.getElementById('duration').value;
    const date = document.getElementById('date').value;

    const appointmentData = {
        name,
        gender,
        doctor,
        patient_id: patientId,
        requested_hour: hour,
        duration,
        appointment_date: date
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(appointmentData)
        });
        console.log('res', response)

        const result = await response.json();
        document.getElementById('message').textContent = result.message;

        if (result.success) {
            document.getElementById('appointmentForm').reset();
        }
    } catch (error) {
        console.log('error', error)
        document.getElementById('message').textContent = 'Error scheduling appointment. Please try again.';
    }
});
