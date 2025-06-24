import http from 'k6/http';
import { check, sleep } from 'k6';

// Current date/time tracking for linear increment
let currentDate = new Date('2025-06-22'); // Starting from current date
let currentHour = 8;  // Start at 8 AM
let currentMinute = 0;
let currentSalleNumber = 1; // Track salle numbers
let currentReservationNumber = 1; // Track reservation numbers

function getNextDateTime() {
  // Format current values
  const date = currentDate.toISOString().split('T')[0];
  const time = `${String(currentHour).padStart(2, '0')}:${String(currentMinute).padStart(2, '0')}:00`;

  // Increment for next call
  currentMinute += 15;
  if (currentMinute >= 60) {
    currentMinute = 0;
    currentHour++;
    if (currentHour >= 18) { // Reset to 8 AM and move to next day
      currentHour = 8;
      currentDate.setDate(currentDate.getDate() + 1);
    }
  }

  return { date, time };
}

function generateRandomString() {
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < 16; i++) {
    result += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return result;
}

export const options = {
  stages: [
    { duration: '30s', target: 10 }, // Ramp up to 10 users over 30 seconds
    { duration: '1m', target: 10 },  // Stay at 10 users for 1 minute
    { duration: '30s', target: 0 },  // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<1000'], // 95% of requests should be below 1000ms
    http_req_failed: ['rate<0.01'],   // Less than 1% of requests should fail
  },
};

const BASE_URL = 'http://localhost:8001';

export default function () {
  // Test POST salle with incremental number
  const salleData = JSON.stringify({
    nom: `Salle ${currentSalleNumber}`,
    capacite: Math.floor(Math.random() * 50) + 20,
    localisation: "Bâtiment A",
    disponible: true
  });

  let sallePostResponse = http.post(
    `${BASE_URL}/salle/`, 
    salleData,
    { headers: { 'Content-Type': 'application/json' } }
  );

  // Check if salle creation was successful and get the ID
  let createdSalleId;
  const salleCreated = check(sallePostResponse, {
    'salle post status is 201': (r) => r.status === 201,
    'salle post response time OK': (r) => r.timings.duration < 500,
  });

  if (salleCreated) {
    try {
      const responseBody = JSON.parse(sallePostResponse.body);
      createdSalleId = responseBody.data.id;
      if (!createdSalleId) {
        console.error('Salle ID not found in response:', responseBody);
        return; // Skip the rest of this iteration
      }
    } catch (e) {
      console.error('Failed to parse salle response:', e);
      return; // Skip the rest of this iteration
    }
  } else {
    console.error('Failed to create salle:', sallePostResponse.body, 'Status:', sallePostResponse.status);
    return; // Skip the rest of this iteration
  }

  // Test POST reservation using created salle ID
  const nextDateTime = getNextDateTime();
  const reservationData = JSON.stringify({
    salle_id: createdSalleId,
    date: nextDateTime.date,
    heure: nextDateTime.time,
    utilisateur: generateRandomString()
  });
  
  let reservationPostResponse = http.post(
    `${BASE_URL}/reservation/`, 
    reservationData,
    { headers: { 'Content-Type': 'application/json' } }
  );
  check(reservationPostResponse, {
    'reservation post status is 201': (r) => r.status === 201,
    'reservation post response time OK': (r) => r.timings.duration < 500,
  });

  // Test GET endpoints
  let sallesResponse = http.get(`${BASE_URL}/salle/`);
  check(sallesResponse, {
    'salles status is 200': (r) => r.status === 200,
    'salles response time OK': (r) => r.timings.duration < 500,
  });

  let reservationsResponse = http.get(`${BASE_URL}/reservation/`);
  check(reservationsResponse, {
    'reservations status is 200': (r) => r.status === 200,
    'reservations response time OK': (r) => r.timings.duration < 500,
  });

  // Only proceed with PUT and DELETE if we have a valid salle ID
  if (createdSalleId) {
    // Test PUT endpoints using actual salle ID
    const salleUpdateData = JSON.stringify({
      nom: `Salle ${currentSalleNumber} Updated`,
      capacite: 35
    });
    
    let sallePutResponse = http.put(
      `${BASE_URL}/salle/${createdSalleId}`,
      salleUpdateData,
      { headers: { 'Content-Type': 'application/json' } }
    );
    check(sallePutResponse, {
      'salle put status is 200': (r) => r.status === 200,
      'salle put response time OK': (r) => r.timings.duration < 500,
    });

    // Test DELETE endpoints using actual salle ID
    let salleDeleteResponse = http.del(`${BASE_URL}/salle/${createdSalleId}`);
    check(salleDeleteResponse, {
      'salle delete status is 204': (r) => r.status === 204,
      'salle delete response time OK': (r) => r.timings.duration < 500,
    });
  }

  // Get the created reservation ID from response
  let createdReservationId;
  if (reservationPostResponse.status === 201) {
    try {
      createdReservationId = JSON.parse(reservationPostResponse.body).id;
    } catch (e) {
      console.error('Failed to parse reservation response:', e);
    }
  }

  // Only delete reservation if we have its ID
  if (createdReservationId) {
    let reservationDeleteResponse = http.del(`${BASE_URL}/reservation/${createdReservationId}`);
    check(reservationDeleteResponse, {
      'reservation delete status is 204': (r) => r.status === 204,
      'reservation delete response time OK': (r) => r.timings.duration < 500,
    });
  }

  // Increment our counters for the next iteration
  currentSalleNumber++;
  currentReservationNumber++;

  // Random sleep between requests
  sleep(1);
}