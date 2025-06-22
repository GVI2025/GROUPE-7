import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 }, // Ramp up to 20 users over 30 seconds
    { duration: '1m', target: 20 },  // Stay at 20 users for 1 minute
    { duration: '30s', target: 0 },  // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests should be below 500ms
    http_req_failed: ['rate<0.01'],   // Less than 1% of requests should fail
  },
};

const BASE_URL = 'http://localhost:8001';

export default function () {
  // Test POST emplacement
  const emplacementData = JSON.stringify({
    name: 'Test Location',
    type: 'STORAGE'
  });
  
  let emplacementPostResponse = http.post(
    `${BASE_URL}/emplacements/`, 
    emplacementData,
    { headers: { 'Content-Type': 'application/json' } }
  );
  check(emplacementPostResponse, {
    'emplacement post status is 201': (r) => r.status === 201,
    'emplacement post response time OK': (r) => r.timings.duration < 500,
  });

  // Test POST salle
  const salleData = JSON.stringify({
    nom: "Salle 101",
    capacite: 30,
    localisation: "Bâtiment A",
    disponible: true
  });
  
  let sallePostResponse = http.post(
    `${BASE_URL}/salle/`, 
    salleData,
    { headers: { 'Content-Type': 'application/json' } }
  );
  check(sallePostResponse, {
    'salle post status is 201': (r) => r.status === 201,
    'salle post response time OK': (r) => r.timings.duration < 500,
  });

  // Test POST reservation
  const reservationData = JSON.stringify({
    salle_id: "salle_1",
    date: "2025-06-18",
    heure: "14:00:00",
    utilisateur: "John Doe"
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

  // Test PUT endpoints
  const salleUpdateData = JSON.stringify({
    nom: "Salle 102",
    capacite: 35
  });
  
  let sallePutResponse = http.put(
    `${BASE_URL}/salle/abc123`,
    salleUpdateData,
    { headers: { 'Content-Type': 'application/json' } }
  );
  check(sallePutResponse, {
    'salle put status is 200': (r) => r.status === 200,
    'salle put response time OK': (r) => r.timings.duration < 500,
  });

  // Test DELETE endpoints
  let salleDeleteResponse = http.del(`${BASE_URL}/salle/abc123`);
  check(salleDeleteResponse, {
    'salle delete status is 204': (r) => r.status === 204,
    'salle delete response time OK': (r) => r.timings.duration < 500,
  });

  let reservationDeleteResponse = http.del(`${BASE_URL}/reservation/123`);
  check(reservationDeleteResponse, {
    'reservation delete status is 204': (r) => r.status === 204,
    'reservation delete response time OK': (r) => r.timings.duration < 500,
  });

  // Random sleep between requests
  sleep(1);
}