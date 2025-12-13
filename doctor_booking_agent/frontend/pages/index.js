import React, { useState } from 'react';
import styles from '../styles/Home.module.css';

export default function Home() {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [doctorName, setDoctorName] = useState('');
  const [specialty, setSpecialty] = useState('');
  const [loading, setLoading] = useState(false);
  const [callId, setCallId] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const response = await fetch('/api/booking', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          phone_number: phoneNumber,
          doctor_name: doctorName || 'Dr. Raj Kumar',
          specialty: specialty || 'General Medicine'
        })
      });

      const data = await response.json();
      
      if (data.success) {
        setCallId(data.call_id);
        setPhoneNumber('');
        setDoctorName('');
        setSpecialty('');
      } else {
        setError(data.error || 'Failed to initiate call');
      }
    } catch (err) {
      setError('Error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.main}>
        <h1>Doctor Appointment Booking</h1>
        <p className={styles.subtitle}>Schedule your appointment via voice call</p>

        {callId ? (
          <div className={styles.success}>
            <h2>Call Initiated Successfully!</h2>
            <p>Call ID: <strong>{callId}</strong></p>
            <p>You will receive a call shortly on {phoneNumber}</p>
            <button 
              className={styles.button}
              onClick={() => setCallId(null)}
            >
              Book Another Appointment
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className={styles.form}>
            <div className={styles.formGroup}>
              <label>Phone Number *</label>
              <input
                type="tel"
                placeholder="+91XXXXXXXXXX"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                required
              />
            </div>

            <div className={styles.formGroup}>
              <label>Doctor Name (Optional)</label>
              <input
                type="text"
                placeholder="Dr. Raj Kumar"
                value={doctorName}
                onChange={(e) => setDoctorName(e.target.value)}
              />
            </div>

            <div className={styles.formGroup}>
              <label>Specialty (Optional)</label>
              <input
                type="text"
                placeholder="General Medicine"
                value={specialty}
                onChange={(e) => setSpecialty(e.target.value)}
              />
            </div>

            {error && <div className={styles.error}>{error}</div>}

            <button 
              type="submit" 
              className={styles.button}
              disabled={loading}
            >
              {loading ? 'Initiating Call...' : 'Initiate Call'}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
