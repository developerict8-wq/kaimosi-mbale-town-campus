from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db

class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(150), nullable=False, default='Administrator')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)

class SchoolInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(200), nullable=False, default='Your School Name')
    motto = db.Column(db.String(300)); about = db.Column(db.Text); history = db.Column(db.Text)
    vision = db.Column(db.Text); mission = db.Column(db.Text); values = db.Column(db.Text)
    principal_message = db.Column(db.Text); address = db.Column(db.String(300)); phone = db.Column(db.String(100))
    email = db.Column(db.String(150)); website = db.Column(db.String(250)); logo = db.Column(db.String(255)); hero_image = db.Column(db.String(255))
    facebook = db.Column(db.String(300)); youtube = db.Column(db.String(300)); instagram = db.Column(db.String(300))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Staff(db.Model):
    id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(150),nullable=False); position=db.Column(db.String(150)); department=db.Column(db.String(150)); bio=db.Column(db.Text); photo=db.Column(db.String(255)); created_at=db.Column(db.DateTime,default=datetime.utcnow)
class News(db.Model):
    id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(250),nullable=False); content=db.Column(db.Text,nullable=False); image=db.Column(db.String(255)); published=db.Column(db.Boolean,default=True); created_at=db.Column(db.DateTime,default=datetime.utcnow); updated_at=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
class Event(db.Model):
    id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(250),nullable=False); description=db.Column(db.Text); event_date=db.Column(db.DateTime); location=db.Column(db.String(250)); image=db.Column(db.String(255)); created_at=db.Column(db.DateTime,default=datetime.utcnow)
class Gallery(db.Model):
    id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(250)); description=db.Column(db.Text); image=db.Column(db.String(255),nullable=False); created_at=db.Column(db.DateTime,default=datetime.utcnow)
class Document(db.Model):
    id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(250),nullable=False); description=db.Column(db.Text); filename=db.Column(db.String(255),nullable=False); created_at=db.Column(db.DateTime,default=datetime.utcnow)
class ContactMessage(db.Model):
    id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(150),nullable=False); email=db.Column(db.String(150),nullable=False); phone=db.Column(db.String(100)); subject=db.Column(db.String(250)); message=db.Column(db.Text,nullable=False); read=db.Column(db.Boolean,default=False); created_at=db.Column(db.DateTime,default=datetime.utcnow)


class Department(db.Model):
    __tablename__ = "departments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180), nullable=False)
    description = db.Column(db.Text)
    head = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(220), nullable=False)
    code = db.Column(db.String(80))
    level = db.Column(db.String(100))
    duration = db.Column(db.String(100))
    entry_requirements = db.Column(db.Text)
    description = db.Column(db.Text)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    department = db.relationship("Department", backref=db.backref("courses", lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AdmissionInfo(db.Model):
    __tablename__ = "admission_info"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(220), nullable=False, default="Admissions")
    content = db.Column(db.Text)
    requirements = db.Column(db.Text)
    application_steps = db.Column(db.Text)
    important_dates = db.Column(db.Text)
    contact = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Announcement(db.Model):
    __tablename__ = "announcements"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text, nullable=False)
    published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Building(db.Model):
    __tablename__ = "buildings"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(220), nullable=False)
    category = db.Column(db.String(150))
    location = db.Column(db.String(220))
    description = db.Column(db.Text)
    facilities = db.Column(db.Text)
    status = db.Column(db.String(80), default="Active")
    image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
