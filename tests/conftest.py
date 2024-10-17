import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from config.db import SessionLocal

from config.db import Base


@pytest.fixture(scope="function", autouse=True)
def clean_database():
    db = SessionLocal()

    Base.metadata.drop_all(bind=db.get_bind())
    Base.metadata.create_all(bind=db.get_bind())
    
    yield db

    db.close()