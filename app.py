from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configurations for our database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    role = db.Column(db.String(50), nullable=False) # role like admin / doctor / patient
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    qualification = db.Column(db.String(200))
    experience_years = db.Column(db.Integer)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    department = db.relationship("Department", back_populates='doctors')
    doctor_appointments = db.relationship("Appointment",foreign_keys="Appointment.doctor_id",back_populates="doctor")
    patient_appointments = db.relationship("Appointment",foreign_keys="Appointment.patient_id",back_populates="patient")
    is_active = db.Column(db.Boolean, default=True)