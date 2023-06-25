import http from 'k6/http';
import { sleep } from 'k6';

export default function () {
  // GET /cows
  http.get('http://localhost:8000/cows');

  // POST /cows
  const payload = JSON.stringify({
    name: "betty",
    sex: "Female",
    birthdate: "2019-02-11T03:21:00.000000",
    condition: "healthy",
    weight: {"mass_kg": 1100, "last_measured": "2022-11-02T11:15:00.000000"},
    feeding: {
        amount_kg: 5,
        cron_schedule: "0 */6 * * *",
        last_measured: "2022-11-02T11:00:00.000000",
    },
    milk_production: {
        last_milk: "2022-11-02T09:00:00.000000",
        cron_schedule: "0 8,12,16,20 * * *",
        amount_l: 5,
    },
    has_calves: true,
  });
  const headers = { 'Content-Type': 'application/json' };
  http.post('http://localhost:8000/cows', payload, { headers });

  // PUT /cows/{cow_id}
  // const updatedPayload = JSON.stringify({
  //   name: 'Updated Cow',
  //   weight: 550,
  //   milk_production: 12
  // });
  //const updateHeaders = { 'Content-Type': 'application/json' };
  //http.put('http://localhost:8000/cows/1', updatedPayload, { headers: updateHeaders });

  // Wait for 1 second between requests
  sleep(1);
}

