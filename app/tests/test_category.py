from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

# Use an in-memory SQLite database for testing to avoid polluting the main DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create the test database tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_create_category():
    response = client.post(
        "/api/v1/categories/",
        json={"name": "Test Category", "description": "Test Description"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Category"
    assert "id" in data
    return data["id"]

def test_read_categories():
    response = client.get("/api/v1/categories/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 0

def test_read_category():
    # Create a category first
    response_create = client.post(
        "/api/v1/categories/",
        json={"name": "Test Read", "description": "Test Description"},
    )
    category_id = response_create.json()["id"]

    response = client.get(f"/api/v1/categories/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Read"
    assert data["id"] == category_id

def test_update_category():
    # Create a category first
    response_create = client.post(
        "/api/v1/categories/",
        json={"name": "Test Update", "description": "Test Description"},
    )
    category_id = response_create.json()["id"]

    response = client.put(
        f"/api/v1/categories/{category_id}",
        json={"name": "Updated Name", "description": "Updated Description"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["description"] == "Updated Description"

def test_delete_category():
    # Create a category first
    response_create = client.post(
        "/api/v1/categories/",
        json={"name": "Test Delete", "description": "Test Description"},
    )
    category_id = response_create.json()["id"]

    response = client.delete(f"/api/v1/categories/{category_id}")
    assert response.status_code == 200
    
    # Verify it's gone
    response_get = client.get(f"/api/v1/categories/{category_id}")
    assert response_get.status_code == 404
