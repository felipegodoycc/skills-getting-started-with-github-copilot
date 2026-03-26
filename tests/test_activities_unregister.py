from src import app as app_module


def test_unregister_removes_participant(client):
    activity_name = "Chess Club"
    existing_email = app_module.activities[activity_name]["participants"][0]

    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": existing_email},
    )

    assert response.status_code == 200
    assert existing_email not in app_module.activities[activity_name]["participants"]
    assert response.json()["message"] == f"Unregistered {existing_email} from {activity_name}"


def test_unregister_returns_404_for_unknown_activity(client):
    response = client.delete(
        "/activities/Nonexistent Activity/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_unknown_participant(client):
    activity_name = "Chess Club"
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": "missing@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
