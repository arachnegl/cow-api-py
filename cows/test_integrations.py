from fastapi.testclient import TestClient

from cows.main import app

client = TestClient(app)


req = {
    "name": "betty",
    "sex": "Female",
    "birthdate": "2019-02-11T03:21:00.000000",
    "condition": "healthy",
    "weight": {"mass_kg": 1100, "last_measured": "2022-11-02T11:15:00.000000"},
    "feeding": {
        "amount_kg": 5,
        "cron_schedule": "0 */6 * * *",
        "last_measured": "2022-11-02T11:00:00.000000",
    },
    "milk_production": {
        "last_milk": "2022-11-02T09:00:00.000000",
        "cron_schedule": "0 8,12,16,20 * * *",
        "amount_l": 5,
    },
    "has_calves": True,
}


def test_add_a_cow():
    res = client.post("/cows", json=req)
    assert res.status_code == 200
