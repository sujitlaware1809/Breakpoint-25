import React, { useState, useEffect } from 'react';
import styles from '../styles/Doctor.module.css';

export default function DoctorLogin() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [doctor, setDoctor] = useState(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [appointments, setAppointments] = useState([]);
  const [availabilitySlots, setAvailabilitySlots] = useState([]);
  const [newSlotDate, setNewSlotDate] = useState('');
  const [newSlotTime, setNewSlotTime] = useState('10:00 AM');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

  // Check if already logged in
  useEffect(() => {
    const savedDoctor = localStorage.getItem('doctor');
    if (savedDoctor) {
      const doctorData = JSON.parse(savedDoctor);
      setDoctor(doctorData);
      setIsLoggedIn(true);
      fetchAppointments(doctorData.id);
      fetchAvailability(doctorData.id);
    }
  }, []);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_URL}/api/doctor/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setDoctor(data.doctor);
        setIsLoggedIn(true);
        localStorage.setItem('doctor', JSON.stringify(data.doctor));
        fetchAppointments(data.doctor.id);
        fetchAvailability(data.doctor.id);
      } else {
        setError(data.error || 'Login failed');
      }
    } catch (err) {
      setError('Cannot connect to server. Make sure Flask backend is running on port 5000');
    } finally {
      setLoading(false);
    }
  };

  const fetchAppointments = async (doctorId) => {
    try {
      // Check cache first (5 minute TTL)
      const cacheKey = `appointments_${doctorId}`;
      const cached = sessionStorage.getItem(cacheKey);
      const cacheTime = sessionStorage.getItem(`${cacheKey}_time`);
      
      if (cached && cacheTime && (Date.now() - parseInt(cacheTime)) < 300000) {
        setAppointments(JSON.parse(cached));
        return;
      }

      const response = await fetch(`${API_URL}/api/doctor/${doctorId}/appointments`);
      const data = await response.json();
      if (data.status === 'success') {
        // Format appointments with proper date display
        const formattedAppointments = data.data.map(apt => ({
          ...apt,
          appointment_date: new Date(apt.appointment_date).toLocaleDateString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
          })
        }));
        setAppointments(formattedAppointments);
        
        // Cache the results
        sessionStorage.setItem(cacheKey, JSON.stringify(formattedAppointments));
        sessionStorage.setItem(`${cacheKey}_time`, Date.now().toString());
      }
    } catch (err) {
      console.error('Failed to fetch appointments:', err);
    }
  };

  const fetchAvailability = async (doctorId) => {
    try {
      const response = await fetch(`${API_URL}/api/doctor/${doctorId}/availability`);
      const data = await response.json();
      if (data.success) {
        setAvailabilitySlots(data.slots);
      }
    } catch (err) {
      console.error('Failed to fetch availability:', err);
    }
  };

  const addAvailabilitySlot = async (e) => {
    e.preventDefault();
    if (!newSlotDate) return;

    try {
      const response = await fetch(`${API_URL}/api/doctor/${doctor.id}/availability`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          date: newSlotDate,
          time_slots: [newSlotTime],
          max_patients: 1
        })
      });

      const data = await response.json();
      if (data.success) {
        fetchAvailability(doctor.id);
        setNewSlotDate('');
        alert('Availability slot added!');
      }
    } catch (err) {
      alert('Failed to add slot');
    }
  };

  const deleteSlot = async (slotId) => {
    if (!confirm('Delete this slot?')) return;

    try {
      const response = await fetch(`${API_URL}/api/doctor/${doctor.id}/availability/${slotId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        fetchAvailability(doctor.id);
        alert('Slot deleted');
      }
    } catch (err) {
      alert('Failed to delete slot');
    }
  };

  const toggleAvailability = async () => {
    try {
      const response = await fetch(`${API_URL}/api/doctor/${doctor.id}/toggle-availability`, {
        method: 'POST'
      });

      const data = await response.json();
      if (data.success) {
        setDoctor({ ...doctor, is_available: data.is_available });
        alert(data.message);
      }
    } catch (err) {
      alert('Failed to toggle availability');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('doctor');
    setIsLoggedIn(false);
    setDoctor(null);
    setAppointments([]);
  };

  if (!isLoggedIn) {
    return (
      <div className={styles.container}>
        <div className={styles.header}>
          <div className={styles.logo}>HealthCare</div>
          <a href="/" className={styles.homeLink}>Patient Booking</a>
        </div>
        <div className={styles.loginBox}>
          <div className={styles.loginImage}>
            <img src="/docter.png" alt="Doctor" />
          </div>
          <h1>Doctor Portal</h1>
          <p className={styles.welcome}>Sign in to manage your appointments</p>
          {error && <div className={styles.error}>{error}</div>}
          <form onSubmit={handleLogin}>
            <div className={styles.formGroup}>
              <label>Email</label>
              <input
                type="email"
                placeholder="doctor@hospital.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className={styles.formGroup}>
              <label>Password</label>
              <input
                type="password"
                placeholder="Enter password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <button type="submit" disabled={loading}>
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </form>
          <p className={styles.hint}>
            Test: rajkumar@hospital.com / password123
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.logo}>HealthCare</div>
        <div className={styles.doctorInfo}>
          <span>Dr. {doctor.name}</span>
          <span className={styles.specialty}>{doctor.specialty}</span>
        </div>
        <button onClick={handleLogout} className={styles.logoutBtn}>Logout</button>
      </div>

      <div className={styles.dashboard}>
        {/* Availability Section */}
        <div className={styles.section}>
          <div className={styles.sectionHeader}>
            <h2>Availability</h2>
            <button onClick={toggleAvailability} className={styles.toggleBtn}>
              {doctor.is_available ? '✓ Available' : '○ Unavailable'}
            </button>
          </div>

          <form onSubmit={addAvailabilitySlot} className={styles.slotForm}>
            <div className={styles.inputGroup}>
              <input
                type="date"
                value={newSlotDate}
                onChange={(e) => setNewSlotDate(e.target.value)}
                min={new Date().toISOString().split('T')[0]}
                required
              />
              <select value={newSlotTime} onChange={(e) => setNewSlotTime(e.target.value)}>
                <option>9:00 AM</option>
                <option>10:00 AM</option>
                <option>11:00 AM</option>
                <option>12:00 PM</option>
                <option>2:00 PM</option>
                <option>3:00 PM</option>
                <option>4:00 PM</option>
                <option>5:00 PM</option>
              </select>
            </div>
            <button type="submit">Add Slot</button>
          </form>

          <div className={styles.slotsList}>
            <h3>Available Slots</h3>
            {availabilitySlots.filter(s => !s.is_booked).map(slot => (
              <div key={slot.id} className={styles.slotItem}>
                <span>{slot.date} at {slot.time_slot}</span>
                <button onClick={() => deleteSlot(slot.id)} className={styles.deleteBtn}>
                  Delete
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Appointments Section */}
        <div className={styles.section}>
          <div className={styles.sectionHeader}>
            <h2>Appointments</h2>
            <span className={styles.badge}>{appointments.length}</span>
          </div>
          <div className={styles.appointmentsList}>
            {appointments.length === 0 ? (
              <p className={styles.noData}>No appointments scheduled</p>
            ) : (
              appointments.map(apt => (
                <div key={apt.id} className={styles.appointmentCard}>
                  <div className={styles.aptHeader}>
                    <strong>{apt.patient_name || 'Patient'}</strong>
                    <span className={`${styles.status} ${styles[apt.status]}`}>
                      {apt.status}
                    </span>
                  </div>
                  <div className={styles.aptDetails}>
                    <p><strong>Date:</strong> {apt.appointment_date}</p>
                    <p><strong>Time:</strong> {apt.appointment_time}</p>
                    <p><strong>Phone:</strong> {apt.patient_phone}</p>
                    {apt.reason && <p><strong>Reason:</strong> {apt.reason}</p>}
                    {apt.symptoms && <p><strong>Symptoms:</strong> {apt.symptoms}</p>}
                    {apt.special_notes && <p><strong>Notes:</strong> {apt.special_notes}</p>}
                    <p><strong>Confirmation:</strong> {apt.confirmation_number}</p>
                    {apt.call_status && <p><strong>Call Status:</strong> {apt.call_status}</p>}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
