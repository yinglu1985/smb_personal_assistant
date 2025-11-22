// Admin Portal JavaScript

// Use relative URLs to work in both development and production
const API_BASE_URL = '/api';

// State
let currentWeekStart = new Date();
let allAppointments = [];
let filteredAppointments = [];
let currentAppointment = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeDateDisplay();
    loadTherapists();
    setCurrentWeekStart();
    loadData();
    setupEventListeners();
});

function initializeDateDisplay() {
    const dateElement = document.getElementById('current-date');
    const now = new Date();
    dateElement.textContent = now.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function setCurrentWeekStart() {
    const today = new Date();
    const day = today.getDay();
    const diff = today.getDate() - day; // Start from Sunday
    currentWeekStart = new Date(today.setDate(diff));
    currentWeekStart.setHours(0, 0, 0, 0);
}

function setupEventListeners() {
    // Navigation buttons
    document.getElementById('prev-week').addEventListener('click', () => {
        currentWeekStart.setDate(currentWeekStart.getDate() - 7);
        updateCalendar();
    });

    document.getElementById('next-week').addEventListener('click', () => {
        currentWeekStart.setDate(currentWeekStart.getDate() + 7);
        updateCalendar();
    });

    // Filter buttons
    document.getElementById('refresh-btn').addEventListener('click', () => {
        loadData();
    });

    document.getElementById('therapist-filter').addEventListener('change', applyFilters);
    document.getElementById('status-filter').addEventListener('change', applyFilters);
    document.getElementById('date-filter').addEventListener('change', applyFilters);

    // Modal close
    document.querySelector('.close-modal').addEventListener('click', closeModal);
    document.getElementById('appointment-modal').addEventListener('click', (e) => {
        if (e.target.id === 'appointment-modal') {
            closeModal();
        }
    });

    // Appointment actions
    document.getElementById('confirm-btn').addEventListener('click', () => updateAppointmentStatus('confirmed'));
    document.getElementById('complete-btn').addEventListener('click', () => updateAppointmentStatus('completed'));
    document.getElementById('cancel-btn').addEventListener('click', () => updateAppointmentStatus('cancelled'));
}

async function loadTherapists() {
    try {
        const response = await fetch(`${API_BASE_URL}/therapists`);
        const therapists = await response.json();

        const therapistFilter = document.getElementById('therapist-filter');
        therapists.forEach(therapist => {
            const option = document.createElement('option');
            option.value = therapist.id;
            option.textContent = therapist.name;
            therapistFilter.appendChild(option);
        });
    } catch (error) {
        console.error('Failed to load therapists:', error);
    }
}

async function loadData() {
    try {
        // Load appointments
        const appointmentsResponse = await fetch(`${API_BASE_URL}/admin/appointments?per_page=1000`);
        const appointmentsData = await appointmentsResponse.json();
        allAppointments = appointmentsData.appointments || [];

        // Load dashboard stats
        const dashboardResponse = await fetch(`${API_BASE_URL}/admin/dashboard`);
        const dashboardData = await dashboardResponse.json();

        updateStats(dashboardData.stats);
        applyFilters();
    } catch (error) {
        console.error('Failed to load data:', error);
        alert('Failed to load appointments. Please check if the server is running.');
    }
}

function applyFilters() {
    const therapistId = document.getElementById('therapist-filter').value;
    const status = document.getElementById('status-filter').value;
    const date = document.getElementById('date-filter').value;

    filteredAppointments = allAppointments.filter(apt => {
        if (therapistId && apt.therapist && apt.therapist.id != therapistId) {
            return false;
        }
        if (status && apt.status !== status) {
            return false;
        }
        if (date && apt.appointment_date !== date) {
            return false;
        }
        return true;
    });

    updateCalendar();
    updateAppointmentsList();
}

function updateStats(stats) {
    document.getElementById('total-appointments').textContent = stats.total_appointments || 0;
    document.getElementById('pending-appointments').textContent = stats.pending_appointments || 0;
    document.getElementById('confirmed-appointments').textContent = stats.confirmed_appointments || 0;

    // Calculate revenue (you can enhance this based on completed appointments)
    const revenue = allAppointments
        .filter(apt => apt.status === 'completed')
        .reduce((sum, apt) => sum + (apt.service?.price || 0), 0);
    document.getElementById('revenue').textContent = `$${revenue.toFixed(2)}`;
}

function updateCalendar() {
    const calendarGrid = document.getElementById('calendar-grid');
    const weekTitle = document.getElementById('week-title');

    // Update week title
    const weekEnd = new Date(currentWeekStart);
    weekEnd.setDate(weekEnd.getDate() + 6);

    weekTitle.textContent = `${currentWeekStart.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} - ${weekEnd.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`;

    // Clear calendar
    calendarGrid.innerHTML = '';

    // Generate 7 days
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

    for (let i = 0; i < 7; i++) {
        const dayDate = new Date(currentWeekStart);
        dayDate.setDate(dayDate.getDate() + i);

        const dayElement = createDayElement(days[i], dayDate);
        calendarGrid.appendChild(dayElement);
    }
}

function createDayElement(dayName, date) {
    const dayDiv = document.createElement('div');
    dayDiv.className = 'calendar-day';

    // Check if today
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    if (date.getTime() === today.getTime()) {
        dayDiv.classList.add('today');
    }

    // Day header
    const header = document.createElement('div');
    header.className = 'day-header';
    header.innerHTML = `
        <div>${dayName}</div>
        <div class="day-date">${date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</div>
    `;
    dayDiv.appendChild(header);

    // Get appointments for this day
    const dateStr = date.toISOString().split('T')[0];
    const dayAppointments = filteredAppointments.filter(apt => apt.appointment_date === dateStr);

    // Sort by time
    dayAppointments.sort((a, b) => a.appointment_time.localeCompare(b.appointment_time));

    // Add appointment slots
    dayAppointments.forEach(apt => {
        const slot = createAppointmentSlot(apt);
        dayDiv.appendChild(slot);
    });

    return dayDiv;
}

function createAppointmentSlot(appointment) {
    const slot = document.createElement('div');
    slot.className = `appointment-slot ${appointment.status}`;
    slot.onclick = () => showAppointmentDetails(appointment);

    const time = formatTime(appointment.appointment_time);
    const customerName = appointment.customer ? `${appointment.customer.first_name} ${appointment.customer.last_name}` : 'Unknown';
    const therapistName = appointment.therapist ? appointment.therapist.name : 'Not assigned';

    slot.innerHTML = `
        <div class="slot-time">${time}</div>
        <div class="slot-customer">${customerName}</div>
        <div class="slot-therapist">${therapistName}</div>
    `;

    return slot;
}

function formatTime(timeStr) {
    const [hours, minutes] = timeStr.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour % 12 || 12;
    return `${displayHour}:${minutes} ${ampm}`;
}

function updateAppointmentsList() {
    const tbody = document.getElementById('appointments-table-body');
    tbody.innerHTML = '';

    if (filteredAppointments.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; padding: 40px;">No appointments found</td></tr>';
        return;
    }

    // Sort by date and time (most recent first)
    const sorted = [...filteredAppointments].sort((a, b) => {
        const dateCompare = b.appointment_date.localeCompare(a.appointment_date);
        if (dateCompare !== 0) return dateCompare;
        return b.appointment_time.localeCompare(a.appointment_time);
    });

    sorted.forEach(apt => {
        const row = document.createElement('tr');
        row.style.cursor = 'pointer';
        row.onclick = () => showAppointmentDetails(apt);

        // Parse date string to avoid timezone issues (date comes as "YYYY-MM-DD")
        const [year, month, day] = apt.appointment_date.split('-');
        const dateObj = new Date(year, month - 1, day); // month is 0-indexed
        const date = dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        const time = formatTime(apt.appointment_time);
        const customer = apt.customer ? `${apt.customer.first_name} ${apt.customer.last_name}` : 'Unknown';
        const service = apt.service ? apt.service.name : 'N/A';
        const therapist = apt.therapist ? apt.therapist.name : 'Not assigned';
        const email = apt.customer ? apt.customer.email : '';
        const phone = apt.customer ? apt.customer.phone : '';

        row.innerHTML = `
            <td>${date} at ${time}</td>
            <td>${customer}</td>
            <td>${service}</td>
            <td>${therapist}</td>
            <td><span class="status-badge ${apt.status}">${apt.status}</span></td>
            <td>${email}<br>${phone}</td>
            <td>
                <button class="btn-primary btn-sm" onclick="event.stopPropagation(); showAppointmentDetails(${apt.id})">View</button>
            </td>
        `;

        tbody.appendChild(row);
    });
}

function showAppointmentDetails(appointmentId) {
    // Find appointment by ID if number passed, otherwise use the object
    const appointment = typeof appointmentId === 'number'
        ? allAppointments.find(apt => apt.id === appointmentId)
        : appointmentId;

    if (!appointment) return;

    currentAppointment = appointment;

    const modal = document.getElementById('appointment-modal');
    const details = document.getElementById('appointment-details');

    // Parse date string to avoid timezone issues (date comes as "YYYY-MM-DD")
    const [year, month, day] = appointment.appointment_date.split('-');
    const dateObj = new Date(year, month - 1, day); // month is 0-indexed
    const date = dateObj.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    const time = formatTime(appointment.appointment_time);
    const customer = appointment.customer ? `${appointment.customer.first_name} ${appointment.customer.last_name}` : 'Unknown';
    const service = appointment.service || {};
    const therapist = appointment.therapist || {};

    details.innerHTML = `
        <p><strong>Appointment ID:</strong> ${appointment.id}</p>
        <p><strong>Date:</strong> ${date}</p>
        <p><strong>Time:</strong> ${time}</p>
        <p><strong>Status:</strong> <span class="status-badge ${appointment.status}">${appointment.status}</span></p>
        <p><strong>Customer:</strong> ${customer}</p>
        <p><strong>Email:</strong> ${appointment.customer?.email || 'N/A'}</p>
        <p><strong>Phone:</strong> ${appointment.customer?.phone || 'N/A'}</p>
        <p><strong>Service:</strong> ${service.name || 'N/A'} (${service.duration_minutes || 0} min, $${service.price || 0})</p>
        <p><strong>Therapist:</strong> ${therapist.name || 'Not assigned'}</p>
        ${appointment.notes ? `<p><strong>Notes:</strong> ${appointment.notes}</p>` : ''}
    `;

    modal.classList.add('active');
}

function closeModal() {
    document.getElementById('appointment-modal').classList.remove('active');
}

async function updateAppointmentStatus(newStatus) {
    if (!currentAppointment) return;

    try {
        const response = await fetch(`${API_BASE_URL}/appointments/${currentAppointment.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: newStatus })
        });

        if (response.ok) {
            alert(`Appointment ${newStatus} successfully!`);
            closeModal();
            loadData(); // Reload all data
        } else {
            const error = await response.json();
            alert(`Failed to update appointment: ${error.error || 'Unknown error'}`);
        }
    } catch (error) {
        console.error('Error updating appointment:', error);
        alert('Failed to update appointment. Please try again.');
    }
}

// Make function available globally for onclick handlers
window.showAppointmentDetails = showAppointmentDetails;
