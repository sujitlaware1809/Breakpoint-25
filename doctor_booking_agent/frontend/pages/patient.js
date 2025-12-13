import { useState, useEffect } from 'react';
import styles from '../styles/PatientDashboard.module.css';

export default function PatientDashboard() {
  const [appointments, setAppointments] = useState([]);
  const [patientInfo, setPatientInfo] = useState(null);
  const [phone, setPhone] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchPatientInfo = async () => {
    if (!phone) return;
    
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:5000/api/patient/phone/${phone}`);
      const data = await res.json();
      
      if (data.status === 'success') {
        setPatientInfo(data.data);
      }
    } catch (error) {
      console.error('Error fetching patient:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <h1>📋 Patient Dashboard</h1>
      
      <div className={styles.searchSection}>
        <input
          type="tel"
          placeholder="Enter your phone number"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          className={styles.input}
        />
        <button onClick={fetchPatientInfo} className={styles.button}>
          View My Appointments
        </button>
      </div>

      {patientInfo && (
        <div className={styles.infoCard}>
          <h2>Welcome, {patientInfo.name}!</h2>
          <p>Phone: {patientInfo.phone}</p>
          <p>Email: {patientInfo.email || 'N/A'}</p>
        </div>
      )}
    </div>
  );
}
