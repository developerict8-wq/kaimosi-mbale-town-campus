from flask import Blueprint, render_template, request, redirect, url_for, current_app, send_from_directory, flash
from models import SchoolInfo, Staff, News, Event, Gallery, Document, ContactMessage, Department, Course, AdmissionInfo, Announcement, Building
from extensions import db
public_bp=Blueprint('public',__name__)
@public_bp.context_processor
def inject_school(): return {'school':SchoolInfo.query.first()}
@public_bp.route('/')
def home(): return render_template('public/home.html',news=News.query.filter_by(published=True).order_by(News.created_at.desc()).limit(6).all(),events=Event.query.order_by(Event.event_date.asc()).limit(6).all(),gallery=Gallery.query.order_by(Gallery.created_at.desc()).limit(8).all(),staff=Staff.query.order_by(Staff.name).limit(8).all())
@public_bp.route('/about')
def about(): return render_template('public/about.html')
@public_bp.route('/staff')
def staff(): return render_template('public/staff.html',staff=Staff.query.order_by(Staff.name).all())
@public_bp.route('/news')
def news(): return render_template('public/news.html',news=News.query.filter_by(published=True).order_by(News.created_at.desc()).all())
@public_bp.route('/events')
def events(): return render_template('public/events.html',events=Event.query.order_by(Event.event_date.asc()).all())
@public_bp.route('/gallery')
def gallery(): return render_template('public/gallery.html',gallery=Gallery.query.order_by(Gallery.created_at.desc()).all())
@public_bp.route('/downloads')
def downloads(): return render_template('public/documents.html',documents=Document.query.order_by(Document.created_at.desc()).all())
@public_bp.route('/contact',methods=['GET','POST'])
def contact():
    if request.method=='POST':
        msg=ContactMessage(name=request.form.get('name','').strip(),email=request.form.get('email','').strip(),phone=request.form.get('phone','').strip(),subject=request.form.get('subject','').strip(),message=request.form.get('message','').strip())
        if not msg.name or not msg.email or not msg.message: flash('Please fill in name, email and message.','danger')
        else: db.session.add(msg); db.session.commit(); flash('Your message has been sent successfully.','success'); return redirect(url_for('public.contact'))
    return render_template('public/contact.html')
@public_bp.route('/uploads/<path:filename>')
def uploaded_file(filename): return send_from_directory(current_app.config['UPLOAD_FOLDER'],filename)

@public_bp.route('/academics')
def academics():
    return render_template('public/academics.html', departments=Department.query.order_by(Department.name).all(), courses=Course.query.order_by(Course.name).all())

@public_bp.route('/courses/<int:id>')
def course_detail(id):
    course=Course.query.get_or_404(id)
    return render_template('public/course_detail.html', course=course)

@public_bp.route('/admissions')
def admissions():
    return render_template('public/admissions.html', item=AdmissionInfo.query.first())

@public_bp.route('/announcements')
def announcements():
    return render_template('public/announcements.html', items=Announcement.query.filter_by(published=True).order_by(Announcement.created_at.desc()).all())

@public_bp.route('/buildings')
def buildings():
    return render_template('public/buildings.html', buildings=Building.query.order_by(Building.name).all())
@public_bp.route('/buildings/<int:id>')
def building_detail(id):
    return render_template('public/building_detail.html', building=Building.query.get_or_404(id))
