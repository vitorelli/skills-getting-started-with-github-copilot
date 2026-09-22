from src.app import activities


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_activities_returns_available_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    body = response.json()
    assert "Chess Club" in body
    assert body["Chess Club"]["participants"] == activities["Chess Club"]["participants"]


def test_signup_adds_participant(client):
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up student@mergington.edu for Chess Club"
    }
    assert "student@mergington.edu" in activities["Chess Club"]["participants"]


def test_duplicate_signup_is_rejected(client):
    email = "student@mergington.edu"

    first = client.post("/activities/Chess Club/signup", params={"email": email})
    second = client.post("/activities/Chess Club/signup", params={"email": email})

    assert first.status_code == 200
    assert second.status_code == 400
    assert "already" in second.json()["detail"].lower()


def test_signup_for_unknown_activity_is_rejected(client):
    response = client.post(
        "/activities/Unknown Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_requires_email(client):
    response = client.post("/activities/Chess Club/signup")

    assert response.status_code == 422


def test_unregister_removes_participant(client):
    email = "student@mergington.edu"
    client.post("/activities/Chess Club/signup", params={"email": email})

    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Removed student@mergington.edu from Chess Club"}
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_unknown_activity_is_rejected(client):
    response = client.delete(
        "/activities/Unknown Club/unregister",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_is_rejected(client):
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in this activity"


def test_unregister_requires_email(client):
    response = client.delete("/activities/Chess Club/unregister")

    assert response.status_code == 422
