from app import app
from extensions import db
from models import Admin, SchoolInfo, AdmissionInfo, Building
with app.app_context():
    db.create_all()
    admin=Admin.query.filter_by(username='admin').first()
    if not admin:
        admin=Admin(username='admin',full_name='System Administrator'); admin.set_password('admin123'); db.session.add(admin)
    if not SchoolInfo.query.first():
        db.session.add(SchoolInfo(school_name='YOUR SCHOOL NAME',motto='Excellence in Education',about='Welcome to our school website. Update this information from the administration dashboard.',vision='To be a leading centre of excellence in education.',mission='To provide quality education and develop responsible, confident and capable learners.',values='Integrity, Discipline, Excellence, Respect, Teamwork'))
    db.session.commit()
    print('Database ready. Admin username: admin  password: admin123')
