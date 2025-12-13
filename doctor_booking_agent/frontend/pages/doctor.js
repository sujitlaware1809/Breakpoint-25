import { useState, useEffect } from 'react';
import styles from '../styles/DoctorDashboard.module.css';

export default function DoctorDashboard() {
  const [doctors, setDoctors] = useState([]);
  const [selectedDoctor, setSelectedDoctor] = useState(null);
  const [appointments, setAppointments] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDoctors();
    fetchStats();
  }, []);

  const fetchDoctors = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/doctors');
      const data = await res.json();
      
      if (data.status === 'success') {
        setDoctors(data.data);
      }
    } catch (error) {
      console.error('Error fetching doctors:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/stats/dashboard');
      const data = await res.json();
      
      if (data.status === 'success') {
        setStats(data.data);
      }
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const fetchDoctorAppointments = async (doctorId) => {
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:5000/api/doctor/${doctorId}/appointments`);
      const data = await res.json();
      
      if (data.status === 'success') {
        setAppointments(data.data);
        setSelectedDoctor(doctorId);
      }
    } catch (error) {
      console.error('Error fetching appointments:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <h1>👨‍⚕️ Doctor Dashboard</h1>

      {stats && (
        <div className={styles.statsGrid}>
          <div className={styles.statCard}>
            <h3>{stats.total_patients}</h3>
            <p>Total Patients</p>
          </div>
          <div className={styles.statCard}>
            <h3>{stats.total_doctors}</h3>
            <p>Total Doctors</p>
          </div>
          <div className={styles.statCard}>
            <h3>{stats.today_appointments}</h3>
            <p>Today's Appointments</p>
          </div>
          <div className={styles.statCard}>
            <h3>{stats.pending_appointments}</h3>
            <p>Pending</p>
          </div>
        </div>
      )}

      <div className={styles.doctorsList}>
        <h2>Select Doctor</h2>
        {doctors.map((doctor) => (
          <div
            key={doctor.id}
            className={`${styles.doctorCard} ${selectedDoctor === doctor.id ? styles.selected : ''}`}
            onClick={() => fetchDoctorAppointments(doctor.id)}
          >
            <h3>{doctor.name}</h3>
            <p>{doctor.specialty}</p>
            <p className={styles.clinic}>{doctor.clinic_name}</p>
          </div>
        ))}
      </div>

      {selectedDoctor && (
        <div className={styles.appointmentsSection}>
          <h2>Appointments</h2>
          {loading ? (
            <p>Loading...</p>
          ) : appointments.length > 0 ? (
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>Patient</th>
                  <th>Phone</th>
                  <th>Date</th>
                  <th>Time</th>
                  <th>Status</th>
                  <th>Reason</th>
                </tr>
              </thead>
              <tbody>
                {appointments.map((apt) => (
                  <tr key={apt.id}>
                    <td>{apt.patient_name}</td>
                    <td>{apt.patient_phone}</td>
                    <td>{apt.appointment_date}</td>
                    <td>{apt.appointment_time}</td>
                    <td>
                      <span className={`${styles.status} ${styles[apt.status]}`}>
                        {apt.status}
                      </span>
                    </td>
                    <td>{apt.reason || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>No appointments found</p>
          )}
        </div>
      )}
    </div>
  );
}
