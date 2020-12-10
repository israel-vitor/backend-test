import uuid

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB, UUID, ARRAY

db = SQLAlchemy()
migrate = Migrate()


class WorkflowModel(db.Model):
    __tablename__ = 'workflows'

    UUID = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    status = db.Column(db.Enum('inserted', 'consumed', name="status_enum", create_type=False))
    data = db.Column(JSONB)
    steps = db.Column(ARRAY(db.String()))

    def __init__(self, status, data, steps):
        self.status = status
        self.data = data
        self.steps = steps
