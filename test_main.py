import pytest, random, string
from fastapi.testclient import TestClient
from bson import ObjectId
from movie_app.main import app
from movie_app.auth import get_current_user

## Note that for the tests to pass, a user will have to be signed up and logged in the app.

client = TestClient(app) 

@pytest.fixture(scope="module")
def client():
    with TestClient (app) as c:
        yield c

@pytest.mark.parametrize("username, password, full_name", [("username", "password", "full_name")])
def test_signup(client, username, password, full_name):
    # Create a new user
    user_data = {"username": username, "full_name": full_name, "password": password}
    
    # Test successful signup
    response = client.post("/signup", json=user_data)
    print(response.json())
    assert response.status_code == 200
    # data = response.json()
    # assert data["username"] == username

    # Test username already registered
    response = client.post("/signup", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

    # Test invalid request body
    response = client.post("/signup", json={"invalid": "data"})
    assert response.status_code == 422
    
@pytest.fixture
def test_user(client):
    unique_username = "testuser_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    user_data = {"username": unique_username, "full_name": "Test User", "password": "password"}
    # Create a new test user in the system
    # user_data = {"username": "michaeluser", "full_name": "Michael User", "password": "password"}
    response = client.post("/signup", json=user_data)
    if response.status_code != 200:
        print("Response:", response.json()) 
    assert response.status_code == 200
    return user_data

def test_login_success(client, test_user):
    # Test successful login with valid credentials
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    response = client.post("/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"   

def test_login_invalid_credentials(client):
    # Test login with invalid credentials
    login_data = {
        "username": "invaliduser",
        "password": "wrongpassword"
    }
    response = client.post("/login", data=login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_create_movie_missing_fields(client):
    # Test with missing fields
    incomplete_movie_data = {
        "title": "Test Movie",
    }
    response = client.post("/movies", json=incomplete_movie_data)
    assert response.status_code == 401  # incomplete data

def test_create_movie_unauthenticated(client):
    # Test without the dependency override (unauthenticated)
    app.dependency_overrides.pop(get_current_user, None)  # Remove the override
    movie_data = {
        "title": "Test Movie",
    }   
    response = client.post("/movies", json=movie_data)
    assert response.status_code == 401  # Unauthorized

def test_get_movie_by_id(client):
    movie_id = str(ObjectId())
    # Use the test_login_success_client fixture
    response = client.get(f"/movies/{movie_id}")
    assert response.status_code == 200
    
def test_get_all_movies(client):
    response = client.get("/movies")
    assert response.status_code == 200
    
def test_create_movie(client, test_user):
    login_data = {"username": test_user["username"], "password": test_user["password"]}
    response = client.post("/login", data=login_data)
    if response.status_code != 200:
        print("Response:", response.json()) 
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    movie_data = {
        "title": "Test Movie",
        "description": "description",
        "user_id": test_user["username"],
    }
    response = client.post("/movies", json=movie_data, headers=headers)
    assert response.status_code == 200
    return response.json()["data"]["id"], headers  

def test_update_movie(client, test_user):
    movie_id, headers = test_create_movie(client, test_user)
    movie_data = {
    "user_id": test_user["username"],
    "title": "Updated Test Movie",
    "rating": "5.0",
    "description": "This is an updated test movie",
    "comment": "This movie is updated"
    }
    response = client.put(f"/movies/{movie_id}", json= movie_data, headers=headers)
    assert response.status_code == 200

def test_create_comment(client, test_user):
    movie_id, headers = test_create_movie(client, test_user)
    comment_data = {
    "comment": "This is a test comment",
    "movie_id": "movie_id"
    }  
    response = client.post(f"/movies/{movie_id}/comments", json=comment_data, headers=headers)
    assert response.status_code == 200

def test_get_comments_by_movie(client, test_user):
    movie_id, headers = test_create_movie(client, test_user)
    response = client.get(f"/movies/{movie_id}/comments", headers=headers)
    assert response.status_code == 200

def test_create_rating(client, test_user):
    movie_id, headers = test_create_movie(client, test_user)
    rating_data = {
    "rating": 5.0,
    "movie_id": "movie_id"
    }
    response = client.post(f"/movies/{movie_id}/ratings", json=rating_data, headers=headers)
    assert response.status_code == 200

def test_get_ratings_by_movie(client, test_user):
    movie_id, headers = test_create_movie(client, test_user)
    response = client.get(f"/movies/{movie_id}/ratings", headers=headers)
    assert response.status_code == 200
    
def test_get_ratings_by_movie(client, test_user):
    movie_id, headers = test_create_movie(client, test_user)
    
    # Create a rating for the movie
    rating_data = {
        "rating": 5.0,
        "movie_id": movie_id
    }
    client.post(f"/movies/{movie_id}/ratings", json=rating_data, headers=headers)
    response = client.get(f"/movies/{movie_id}/ratings", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["average_rating"] == rating_data["rating"]
    
