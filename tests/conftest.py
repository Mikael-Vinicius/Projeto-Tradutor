import pytest
from src.database.db import db


@pytest.fixture(autouse=True)
def set_test_environment():
    db.get_collection("languages").drop()
    db.get_collection("history").drop()
    db.get_collection("users").drop()
    yield
