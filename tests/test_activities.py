def test_get_activities_returns_available_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert "participants" in activities["Chess Club"]


def test_signup_adds_participant(client):
    email = "new.student@mergington.edu"

    response = client.post("/activities/Soccer%20Team/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Soccer Team"}
    assert email in client.get("/activities").json()["Soccer Team"]["participants"]


def test_signup_rejects_duplicate_participant(client):
    email = "new.student@mergington.edu"
    url = "/activities/Soccer%20Team/signup"

    assert client.post(url, params={"email": email}).status_code == 200
    response = client.post(url, params={"email": email})

    assert response.status_code == 400
    assert client.get("/activities").json()["Soccer Team"]["participants"].count(email) == 1


def test_signup_rejects_unknown_activity(client):
    response = client.post("/activities/Unknown%20Activity/signup", params={"email": "student@example.com"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_participant(client):
    email = "daniel@mergington.edu"

    response = client.delete("/activities/Chess%20Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from Chess Club"}
    assert email not in client.get("/activities").json()["Chess Club"]["participants"]


def test_unregister_rejects_unknown_activity(client):
    response = client.delete("/activities/Unknown%20Activity/signup", params={"email": "student@example.com"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_rejects_student_not_signed_up(client):
    email = "not.signed.up@mergington.edu"

    response = client.delete("/activities/Soccer%20Team/signup", params={"email": email})

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"