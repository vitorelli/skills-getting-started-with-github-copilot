from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def reset_activities():
    activities.clear()
    activities["Chess Club"] = {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu"],
    }


def test_duplicate_signup_is_rejected():
    reset_activities()

    first = client.post("/activities/Chess Club/signup?email=student@mergington.edu")
    assert first.status_code == 200

    second = client.post("/activities/Chess Club/signup?email=student@mergington.edu")
    assert second.status_code == 400
    assert "already" in second.json()["detail"].lower()


def test_unregistered_participant_is_removed():
    reset_activities()

    client.post("/activities/Chess Club/signup?email=student@mergington.edu")

    response = client.delete("/activities/Chess Club/unregister?email=student@mergington.edu")
    assert response.status_code == 200
    assert "student@mergington.edu" not in activities["Chess Club"]["participants"]
