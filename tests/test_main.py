from fastapi.testclient import TestClient
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import models
import os

from database import Base
from main import app, get_db

if os.path.isfile("./test.db"):
    os.remove("./test.db")
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)

sample_data = [
    {"rate": 0, "amount": 0},
    {"rate": 20, "amount": 12500},
    {"rate": 40, "amount": 50000},
    {"rate": 45, "amount": 150000},
]


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


class TestClass:
    def setup_class(self):
        self.db = TestingSessionLocal()
        for s in sample_data:
            self.db.add(models.Tax(**s))
        self.db.commit()

    def teardown_class(self):
        self.db.close()

    def test_get_tax(self):
        response = client.get("/", params={"salary": 52000})
        assert response.status_code == 200, response.text
        data = response.json()
        assert data == 8300

        response = client.get("/", params={"salary": 52000, "detailed": True})
        assert response.status_code == 200, response.text
        data = response.json()

        assert data == {
            "40% on 2000 (50000 - 52000)": 800,
            "20% on 37500 (12500 - 50000)": 7500,
            "0% on 12500 (0 - 12500)": 0,
            "Total": 8300,
        }
