from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_rejects_activity_over_capacity():
    activity_name = "Chess Club"
    original = client.get("/activities").json()[activity_name]
    participants = original["participants"][:]

    for email in [
        "new1@mergington.edu",
        "new2@mergington.edu",
        "new3@mergington.edu",
        "new4@mergington.edu",
        "new5@mergington.edu",
        "new6@mergington.edu",
        "new7@mergington.edu",
        "new8@mergington.edu",
        "new9@mergington.edu",
        "new10@mergington.edu",
        "new11@mergington.edu",
        "new12@mergington.edu",
    ]:
        if len(client.get("/activities").json()[activity_name]["participants"]) >= original["max_participants"]:
            break
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200, response.text

    response = client.post(f"/activities/{activity_name}/signup?email=overflow@mergington.edu")
    assert response.status_code == 400
    assert "full" in response.json()["detail"].lower()

    client.delete(f"/activities/{activity_name}/unregister?email=new1@mergington.edu")
    client.delete(f"/activities/{activity_name}/unregister?email=new2@mergington.edu")
    client.delete(f"/activities/{activity_name}/unregister?email=new3@mergington.edu")
    client.delete(f"/activities/{activity_name}/unregister?email=new4@mergington.edu")
    client.delete(f"/activities/{activity_name}/unregister?email=new5@mergington.edu")
    client.delete(f"/activities/{activity_name}/unregister?email=new6@mergington.edu")
    client.delete(f"/activities/{activity_name}/unregister?email=new7@mergington.edu")
    client.delete(f"/activities/{activity_name}/unregister?email=new8@mergington.edu")
    client.delete(f"/activities/{activity_name}/unregister?email=new9@mergington.edu")
    client.delete(f"/activities/{activity_name}/unregister?email=new10@mergington.edu")
    client.delete(f"/activities/{activity_name}/unregister?email=new11@mergington.edu")
    client.delete(f"/activities/{activity_name}/unregister?email=new12@mergington.edu")

    # restore original state
    for participant in participants:
        if participant not in client.get("/activities").json()[activity_name]["participants"]:
            client.post(f"/activities/{activity_name}/signup?email={participant}")


def test_signup_rejects_invalid_email_domain():
    response = client.post("/activities/Chess Club/signup?email=student@gmail.com")
    assert response.status_code == 400
    assert "school" in response.json()["detail"].lower() or "email" in response.json()["detail"].lower()
