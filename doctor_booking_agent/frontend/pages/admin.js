import { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import styles from '../styles/Admin.module.css';

export default function Admin() {
  const [stats, setStats] = useState(null);
  const [appointments, setAppointments] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [patients, setPatients] = useState([]);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetchStats();
    fetchAppointments();
    fetchDoctors();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/stats/dashboard');
      const data = await res.json();
      if (data.status === 'success') {
        setStats(data.data);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const fetchAppointments = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/appointments');
      const data = await res.json();
      if (data.status === 'success') {
        setAppointments(data.data);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const fetchDoctors = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/doctors');
      const data = await res.json();
      if (data.status === 'success') {
        setDoctors(data.data);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className={styles.container}>
      <Head>
        <title>Admin Dashboard - Hospital Management</title>
      </Head>

      <div className={styles.header}>
        <h1>🏥 Hospital Management System</h1>
        <div className={styles.nav}>
          <Link href="/">Patient Booking</Link>
          <Link href="/doctor">Doctor Dashboard</Link>
          <Link href="/admin">Admin Panel</Link>
        </div>
      </div>

      <div className={styles.tabs}>
        <button
          className={activeTab === 'overview' ? styles.active : ''}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={activeTab === 'appointments' ? styles.active : ''}
          onClick={() => setActiveTab('appointments')}
        >
          Appointments
        </button>
        <button
          className={activeTab === 'doctors' ? styles.active : ''}
          onClick={() => setActiveTab('doctors')}
        >
          Doctors
        </button>
      </div>

      {activeTab === 'overview' && stats && (
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
            <h3>{stats.total_appointments}</h3>
            <p>Total Appointments</p>
          </div>
          <div className={styles.statCard}>
            <h3>{stats.today_appointments}</h3>
            <p>Today's Appointments</p>
          </div>
          <div className={styles.statCard}>
            <h3>{stats.pending_appointments}</h3>
            <p>Pending</p>
          </div>
          <div className={styles.statCard}>
            <h3>{stats.completed_appointments}</h3>
            <p>Completed</p>
          </div>
        </div>
      )}

      {activeTab === 'appointments' && (
        <div className={styles.tableSection}>
          <h2>All Appointments</h2>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>ID</th>
                <th>Patient</th>
                <th>Doctor</th>
                <th>Date</th>
                <th>Time</th>
                <th>Status</th>
                <th>Confirmation</th>
              </tr>
            </thead>
            <tbody>
              {appointments.map((apt) => (
                <tr key={apt.id}>
                  <td>{apt.id}</td>
                  <td>{apt.patient_name}</td>
                  <td>{apt.doctor_name}</td>
                  <td>{apt.date}</td>
                  <td>{apt.time}</td>
                  <td>
                    <span className={`${styles.badge} ${styles[apt.status]}`}>
                      {apt.status}
                    </span>
                  </td>
                  <td>{apt.confirmation_number}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {activeTab === 'doctors' && (
        <div className={styles.doctorsGrid}>
          {doctors.map((doc) => (
            <div key={doc.id} className={styles.doctorCard}>
              <h3>{doc.name}</h3>
              <p className={styles.specialty}>{doc.specialty}</p>
              <p>{doc.clinic_name}</p>
              <p className={styles.time}>{doc.available_time}</p>
              <p className={styles.fee}>₹{doc.consultation_fee}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
