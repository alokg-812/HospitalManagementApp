from flask import Flask, render_template, request, redirect, url_for, session
import os
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configurations for our database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
from datetime import datetime, timedelta

class User(db.Model):
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

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    doctors = db.relationship("User", back_populates='department')

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))
    status = db.Column(db.String(20), default='Booked')  # Booked/Cancelled/Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    patient = db.relationship("User", foreign_keys=[patient_id], back_populates="patient_appointments")
    doctor = db.relationship("User", foreign_keys=[doctor_id], back_populates="doctor_appointments")

    # one-to-one relationship with treatment
    treatment = db.relationship("Treatment", back_populates="appointment", uselist=False)


class Treatment(db.Model):
    __tablename__ = 'treatments'
    id = db.Column(db.Integer, primary_key=True)
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    appointment = db.relationship("Appointment", back_populates="treatment")
    medicines = db.relationship("Medicine", back_populates="treatment", cascade="all, delete-orphan")


class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    dosage = db.Column(db.String(50))
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatments.id'))
    treatment = db.relationship("Treatment", back_populates="medicines")

class Availability(db.Model):
    __tablename__ = "availability"
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date = db.Column(db.String(15), nullable=False)
    slot_time = db.Column(db.String(20), nullable=False)
    is_available = db.Column(db.Boolean, default=False)

    doctor = db.relationship("User")

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/')
# def base():
#     return render_template('base.html')

@app.route('/registration', methods=["POST", "GET"])
def registration():
    if request.method == "POST":
        name = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        print(name, email, password)
        user = User.query.filter_by(username=name, email=email).first()
        if user:
            return redirect(url_for('login'))
        new_user = User(username=name, email=email, password=password, role="patient")
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')
    return render_template('registration.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["login_email"]
        password = request.form["login_password"]
        print(email, password) #logging to check the function
        user = User.query.filter_by(email=email).first()
        if user and user.password==password:
            session['email'] = user.email
            session['user_id'] = user.id
            session['role'] = user.role
            session['username'] = user.username
            
            if (user.role=='patient'):
                return redirect(url_for('patient_dashboard'))
            elif(user.role=='doctor'):
                return redirect(url_for('doctor_dashboard'))
            elif(user.role=='admin'):
                return redirect(url_for('admin_dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def get_doctors():
    doctors = User.query.filter(User.role=='doctor' and User.is_active == True).all()
    return doctors, len(doctors)

def get_patients():
    patients = User.query.filter_by(role='patient').all()
    return patients, len(patients)

@app.route('/admin_dashboard')
def admin_dashboard():
    doctor_array, total_doctors = get_doctors()
    patient_array_array, total_patients = get_patients()
    # print(total_doctors, total_patients)
    return render_template('admin/admin_dashboard.html', doctor_array=doctor_array, total_doctors=total_doctors, total_patients=total_patients)

@app.route('/doctor_list')
def doctor_list():
    doctor_array, total_doctors = get_doctors()
    return render_template('admin/doctor_list.html', doctor_array=doctor_array, total_doctors=total_doctors)

@app.route('/patient_list')
def patient_list():
    patient_array, total_patients = get_patients()
    return render_template('admin/patient_list.html', patient_array=patient_array, total_patients=total_patients)

@app.route('/admin/edit_doctor')
def edit_doctor():
    return render_template('admin/edit_doctor.html')

@app.route('/delete_doctor/<int:doctor_id>')
def delete_doctor(doctor_id):
    doctor= User.query.get_or_404(doctor_id)
    db.session.delete(doctor)
    db.session.commit()
    return redirect(url_for('doctor_list'))

@app.route('/blacklist_doctor/<int:doctor_id>')
def blacklist_doctor(doctor_id):
    doctor = User.query.get_or_404(doctor_id)
    doctor.is_active = False
    db.session.commit()
    return redirect(url_for('doctor_list'))

@app.route('/activate_doctor/<int:doctor_id>')
def activate_doctor(doctor_id):
    doctor = User.query.get_or_404(doctor_id)
    doctor.is_active = True
    db.session.commit()
    return redirect(url_for('doctor_list'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        existing_admin = User.query.filter_by(username='admin').first()
        if not existing_admin:
            admin_db = User(
                username='admin',
                password='adminPass',
                email='admin@local.com',
                role='admin'
            )
            db.session.add(admin_db)
            db.session.commit()
    app.run(debug=True)