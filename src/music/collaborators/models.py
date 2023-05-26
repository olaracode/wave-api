from src.Server.database import db


class Collaborator(db.Model):
    __tablename__ = "collaborator"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    user = db.relationship("User", backref="collaborator", lazy=True)

    def __repr__(self):
        return f"Collaborators('{self.user_id}', '{self.project_id}')"

    def __str__(self):
        return f"{self.user_id} {self.project_id}"

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "project_id": self.project_id,
        }
