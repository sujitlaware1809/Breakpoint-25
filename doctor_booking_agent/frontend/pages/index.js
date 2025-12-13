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
      <div className={styles.header}>
        <div className={styles.logo}>HealthCare</div>
        <a href="/doctor-login" className={styles.doctorLink}>Doctor Login</a>
      </div>
      <div className={styles.main}>
        <h1>Book Appointment</h1>
        <p className={styles.subtitle}>Schedule via voice call</p>

        {callId ? (
          <div className={styles.success}>
            <h3>Call Initiated</h3>
            <p>Call ID: <strong>{callId}</strong></p>
            <p>You will receive a call shortly</p>
            <button 
              onClick={() => setCallId(null)}
            >
              Book Another
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className={styles.form}>
            <div className={styles.formGroup}>
              <label>Phone Number</label>
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
              <select
                value={specialty}
                onChange={(e) => setSpecialty(e.target.value)}
              >
                <option value="">Select specialty</option>
                <option value="General Medicine">General Medicine</option>
                <option value="Cardiology">Cardiology</option>
                <option value="Dermatology">Dermatology</option>
                <option value="Orthopedics">Orthopedics</option>
                <option value="Pediatrics">Pediatrics</option>
                <option value="ENT">ENT</option>
              </select>
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
