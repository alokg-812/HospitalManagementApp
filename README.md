# Hospitium - Hospital-Management-App
> A web application that allows Admins, Doctors, and Patients to interact with the system based on their roles.
> Built with a clean MVC architecture and Bootstrap UI

## Project Overview

Hospitium (Hospital Management System) is designed to streamline hospital workflows by enabling three major roles — **Admin**, **Doctor**, and **Patient** — each with their own dedicated dashboard and functionality.

This project focuses on user authentication, appointment management, patient history tracking, and doctor availability scheduling, all within a simple, database-driven web interface.


## Features by Role

### Admin
- Create and manage **Doctors** and **Departments**
- View all registered **Patients** and **Doctors**
- Monitor upcoming **Appointments**
- Access **Patient medical history**
- Assign doctors to departments

### Doctor
- View assigned **Appointments**
- Mark appointments as **Completed** or **Cancelled**
- Add **Diagnosis**, **Treatment**, and **Prescriptions**
- View complete **Patient Medical History**
- Manage and provide **Availability Schedule** (next 7 days)
- User-friendly dashboard with Bootstrap UI

### Patient
- Register and log in 
- Update **Profile** details (name, email, etc.)
- View and search **Doctors by specialization**
- Book, reschedule, or cancel **Appointments**
- View upcoming and past **Appointments**
- Access complete **Medical History**

## Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend Framework** | Flask (Python) |
| **Frontend** | HTML5, CSS3, Bootstrap 5 |
| **Database** | SQLite3 (via SQLAlchemy ORM) |
| **Templating Engine** | Jinja2 |
| **Version Control** | Git + GitHub |
| **Virtual Environment** | venv (Python 3.x) |

## Folder Structure
```
HOSPITALMANAGEMENTAPP/
│
├── 📄 app.py                    # Main Flask application
├── 📄 models.py                 # Database models using SQLAlchemy
│
├── 📁 instance/
│   └── 🗄️ hospital.db           # SQLite database file
│
├── 📁 static/
│   ├── 🎨 css/                  # Custom CSS files
│   └── 🖼️ images/               # Image assets
│
├── 📁 templates/
│   ├── 👨‍💼 admin/              # Admin dashboards and forms
│   ├── 👨‍⚕️ doctor/             # Doctor dashboards and forms
│   ├── 🧑‍🤝‍🧑 patient/            # Patient dashboards and forms
│   ├── 📄 base.html             # Common layout for all pages
│   ├── 🏠 index.html            # Home/landing page
│   ├── 🔐 login.html            # User login page
│   └── ✍️ signup.html           # Registration page
│
├── 🐍 Venv/                     # Python virtual environment
├── 📖 README.md                 # Project documentation
└── 📋 requirements.txt          # Python dependencies
```


## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd hospital-management-system

# OR download and extract the ZIP file
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Create Required Folders

```bash
# Create utils folder
mkdir utils

# Create templates folders
mkdir -p templates/admin templates/doctor templates/patient

# Create static folder
mkdir -p static/css static/js static/images
```

### Step 5: Initialize Database

The database will be automatically created when you first run the application. The default admin account will also be created.

### Step 6: Run the Application

```bash
python app.py
```

The application will start at `http://127.0.0.1:5000/`
