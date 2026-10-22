from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AnalysisJob(db.Model):
    __tablename__ = 'analysis_jobs'

    id = db.Column(db.String(36), primary_key=True)  
    status = db.Column(db.String(20), default='processing', nullable=False) 
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    findings = db.relationship('TokenFinding', backref='job', lazy=True, cascade="all, delete-orphan")


class TokenFinding(db.Model):
    __tablename__ = 'token_findings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.String(36), db.ForeignKey('analysis_jobs.id'), nullable=False)
    file_path = db.Column(db.Text, nullable=False)
    token = db.Column(db.String(255), nullable=False)
    occurrences = db.Column(db.Integer, default=1, nullable=False)
