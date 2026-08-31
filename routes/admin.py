import os,uuid
from datetime import datetime
from flask import Blueprint,render_template,request,redirect,url_for,flash,current_app
from flask_login import login_user,logout_user,login_required
from extensions import db
from models import Admin,SchoolInfo,Staff,News,Event,Gallery,Document,ContactMessage,Department,Course,AdmissionInfo,Announcement,Building
from werkzeug.utils import secure_filename
admin_bp=Blueprint('admin',__name__,url_prefix='/admin'); IMAGE={'png','jpg','jpeg','gif','webp'}; DOC={'pdf','doc','docx','xls','xlsx','ppt','pptx'}
def save_upload(f,allowed):
    if not f or not f.filename:return None
    ext=f.filename.rsplit('.',1)[-1].lower() if '.' in f.filename else ''
    if ext not in allowed:return None
    name=uuid.uuid4().hex+'.'+ext; f.save(os.path.join(current_app.config['UPLOAD_FOLDER'],name)); return name
def delete_upload(name):
    if name:
        p=os.path.join(current_app.config['UPLOAD_FOLDER'],name)
        if os.path.exists(p):os.remove(p)
@admin_bp.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        u=Admin.query.filter_by(username=request.form.get('username','').strip()).first()
        if u and u.check_password(request.form.get('password','')):login_user(u);return redirect(url_for('admin.dashboard'))
        flash('Invalid username or password.','danger')
    return render_template('admin/login.html')
@admin_bp.route('/logout')
@login_required
def logout():logout_user();return redirect(url_for('admin.login'))
@admin_bp.route('/')
@login_required
def dashboard():return render_template('admin/dashboard.html',staff_count=Staff.query.count(),news_count=News.query.count(),event_count=Event.query.count(),gallery_count=Gallery.query.count(),document_count=Document.query.count(),message_count=ContactMessage.query.count(),course_count=Course.query.count(),department_count=Department.query.count(),announcement_count=Announcement.query.count(),building_count=Building.query.count())
@admin_bp.route('/school',methods=['GET','POST'])
@login_required
def school():
    x=SchoolInfo.query.first() or SchoolInfo(school_name='YOUR SCHOOL NAME'); db.session.add(x)
    if request.method=='POST':
        for f in ['school_name','motto','about','history','vision','mission','values','principal_message','address','phone','email','website','facebook','youtube','instagram']:setattr(x,f,request.form.get(f,'').strip())
        logo=save_upload(request.files.get('logo'),IMAGE); hero=save_upload(request.files.get('hero_image'),IMAGE)
        if logo:delete_upload(x.logo);x.logo=logo
        if hero:delete_upload(x.hero_image);x.hero_image=hero
        db.session.commit();flash('School information saved.','success');return redirect(url_for('admin.school'))
    return render_template('admin/school.html',item=x)

def crud_list(model,template): return render_template(template,items=model.query.order_by(model.id.desc()).all())
@admin_bp.route('/staff')
@login_required
def staff_list():return crud_list(Staff,'admin/staff_list.html')
@admin_bp.route('/staff/add',methods=['GET','POST'])
@login_required
def staff_add():
    if request.method=='POST':db.session.add(Staff(name=request.form.get('name','').strip(),position=request.form.get('position','').strip(),department=request.form.get('department','').strip(),bio=request.form.get('bio','').strip(),photo=save_upload(request.files.get('photo'),IMAGE)));db.session.commit();flash('Staff member added.','success');return redirect(url_for('admin.staff_list'))
    return render_template('admin/staff_form.html',item=None)
@admin_bp.route('/staff/<int:id>/edit',methods=['GET','POST'])
@login_required
def staff_edit(id):
    x=db.session.get(Staff,id)
    if not x:return 'Not found',404
    if request.method=='POST':x.name=request.form.get('name','').strip();x.position=request.form.get('position','').strip();x.department=request.form.get('department','').strip();x.bio=request.form.get('bio','').strip();p=save_upload(request.files.get('photo'),IMAGE);delete_upload(x.photo) if p else None;x.photo=p or x.photo;db.session.commit();flash('Staff updated.','success');return redirect(url_for('admin.staff_list'))
    return render_template('admin/staff_form.html',item=x)
@admin_bp.route('/staff/<int:id>/delete',methods=['POST'])
@login_required
def staff_delete(id):
    x=db.session.get(Staff,id)
    if x:delete_upload(x.photo);db.session.delete(x);db.session.commit()
    return redirect(url_for('admin.staff_list'))

def news_edit_common(x):
    x.title=request.form.get('title','').strip();x.content=request.form.get('content','').strip();x.published=request.form.get('published')=='on';p=save_upload(request.files.get('image'),IMAGE)
    if p:delete_upload(x.image);x.image=p
@admin_bp.route('/news')
@login_required
def news_list():return crud_list(News,'admin/news_list.html')
@admin_bp.route('/news/add',methods=['GET','POST'])
@login_required
def news_add():
    if request.method=='POST':x=News(title='',content='');news_edit_common(x);db.session.add(x);db.session.commit();flash('News added.','success');return redirect(url_for('admin.news_list'))
    return render_template('admin/news_form.html',item=None)
@admin_bp.route('/news/<int:id>/edit',methods=['GET','POST'])
@login_required
def news_edit(id):
    x=db.session.get(News,id)
    if not x:return 'Not found',404
    if request.method=='POST':news_edit_common(x);db.session.commit();flash('News updated.','success');return redirect(url_for('admin.news_list'))
    return render_template('admin/news_form.html',item=x)
@admin_bp.route('/news/<int:id>/delete',methods=['POST'])
@login_required
def news_delete(id):
    x=db.session.get(News,id)
    if x:delete_upload(x.image);db.session.delete(x);db.session.commit()
    return redirect(url_for('admin.news_list'))

@admin_bp.route('/events')
@login_required
def events_list():return crud_list(Event,'admin/events_list.html')
@admin_bp.route('/events/add',methods=['GET','POST'])
@login_required
def event_add():
    if request.method=='POST':
        dt=None
        try:dt=datetime.fromisoformat(request.form.get('event_date','')) if request.form.get('event_date') else None
        except ValueError:pass
        db.session.add(Event(title=request.form.get('title','').strip(),description=request.form.get('description','').strip(),event_date=dt,location=request.form.get('location','').strip(),image=save_upload(request.files.get('image'),IMAGE)));db.session.commit();flash('Event added.','success');return redirect(url_for('admin.events_list'))
    return render_template('admin/event_form.html',item=None)
@admin_bp.route('/events/<int:id>/edit',methods=['GET','POST'])
@login_required
def event_edit(id):
    x=db.session.get(Event,id)
    if not x:return 'Not found',404
    if request.method=='POST':
        x.title=request.form.get('title','').strip();x.description=request.form.get('description','').strip();x.location=request.form.get('location','').strip()
        try:x.event_date=datetime.fromisoformat(request.form.get('event_date','')) if request.form.get('event_date') else None
        except ValueError:pass
        p=save_upload(request.files.get('image'),IMAGE)
        if p:delete_upload(x.image);x.image=p
        db.session.commit();flash('Event updated.','success');return redirect(url_for('admin.events_list'))
    return render_template('admin/event_form.html',item=x)
@admin_bp.route('/events/<int:id>/delete',methods=['POST'])
@login_required
def event_delete(id):
    x=db.session.get(Event,id)
    if x:delete_upload(x.image);db.session.delete(x);db.session.commit()
    return redirect(url_for('admin.events_list'))

@admin_bp.route('/gallery')
@login_required
def gallery_list():return crud_list(Gallery,'admin/gallery_list.html')
@admin_bp.route('/gallery/add',methods=['GET','POST'])
@login_required
def gallery_add():
    if request.method=='POST':
        p=save_upload(request.files.get('image'),IMAGE)
        if not p:flash('Choose a valid image.','danger');return render_template('admin/gallery_form.html')
        db.session.add(Gallery(title=request.form.get('title','').strip(),description=request.form.get('description','').strip(),image=p));db.session.commit();flash('Photo uploaded.','success');return redirect(url_for('admin.gallery_list'))
    return render_template('admin/gallery_form.html')
@admin_bp.route('/gallery/<int:id>/delete',methods=['POST'])
@login_required
def gallery_delete(id):
    x=db.session.get(Gallery,id)
    if x:delete_upload(x.image);db.session.delete(x);db.session.commit()
    return redirect(url_for('admin.gallery_list'))

@admin_bp.route('/documents')
@login_required
def documents_list():return crud_list(Document,'admin/documents_list.html')
@admin_bp.route('/documents/add',methods=['GET','POST'])
@login_required
def document_add():
    if request.method=='POST':
        p=save_upload(request.files.get('file'),DOC)
        if not p:flash('Choose a valid document.','danger');return render_template('admin/document_form.html')
        db.session.add(Document(title=request.form.get('title','').strip(),description=request.form.get('description','').strip(),filename=p));db.session.commit();flash('Document uploaded.','success');return redirect(url_for('admin.documents_list'))
    return render_template('admin/document_form.html')
@admin_bp.route('/documents/<int:id>/delete',methods=['POST'])
@login_required
def document_delete(id):
    x=db.session.get(Document,id)
    if x:delete_upload(x.filename);db.session.delete(x);db.session.commit()
    return redirect(url_for('admin.documents_list'))

@admin_bp.route('/messages')
@login_required
def messages():return render_template('admin/messages.html',items=ContactMessage.query.order_by(ContactMessage.created_at.desc()).all())
@admin_bp.route('/messages/<int:id>/read',methods=['POST'])
@login_required
def message_read(id):
    x=db.session.get(ContactMessage,id)
    if x:x.read=True;db.session.commit()
    return redirect(url_for('admin.messages'))
@admin_bp.route('/messages/<int:id>/delete',methods=['POST'])
@login_required
def message_delete(id):
    x=db.session.get(ContactMessage,id)
    if x:db.session.delete(x);db.session.commit()
    return redirect(url_for('admin.messages'))


# ---------------- Academics ----------------
@admin_bp.route('/departments')
@login_required
def departments():
    return render_template('admin/departments.html', items=Department.query.order_by(Department.name).all())

@admin_bp.route('/departments/add', methods=['GET','POST'])
@login_required
def department_add():
    if request.method == 'POST':
        x=Department(name=request.form.get('name','').strip(), description=request.form.get('description','').strip(), head=request.form.get('head','').strip())
        if not x.name:
            flash('Department name is required.','danger')
        else:
            db.session.add(x); db.session.commit(); flash('Department added.','success'); return redirect(url_for('admin.departments'))
    return render_template('admin/department_form.html', item=None)

@admin_bp.route('/departments/<int:id>/edit', methods=['GET','POST'])
@login_required
def department_edit(id):
    x=db.session.get(Department,id)
    if not x: return 'Not found',404
    if request.method == 'POST':
        x.name=request.form.get('name','').strip(); x.description=request.form.get('description','').strip(); x.head=request.form.get('head','').strip()
        db.session.commit(); flash('Department updated.','success'); return redirect(url_for('admin.departments'))
    return render_template('admin/department_form.html', item=x)

@admin_bp.route('/departments/<int:id>/delete', methods=['POST'])
@login_required
def department_delete(id):
    x=db.session.get(Department,id)
    if x:
        for c in list(x.courses): db.session.delete(c)
        db.session.delete(x); db.session.commit()
    return redirect(url_for('admin.departments'))

@admin_bp.route('/courses')
@login_required
def courses():
    return render_template('admin/courses.html', items=Course.query.order_by(Course.name).all(), departments=Department.query.order_by(Department.name).all())

@admin_bp.route('/courses/add', methods=['GET','POST'])
@login_required
def course_add():
    if request.method == 'POST':
        x=Course(name=request.form.get('name','').strip(), code=request.form.get('code','').strip(), level=request.form.get('level','').strip(),
                 duration=request.form.get('duration','').strip(), entry_requirements=request.form.get('entry_requirements','').strip(),
                 description=request.form.get('description','').strip(), department_id=request.form.get('department_id') or None)
        if not x.name: flash('Course name is required.','danger')
        else: db.session.add(x); db.session.commit(); flash('Course added.','success'); return redirect(url_for('admin.courses'))
    return render_template('admin/course_form.html', item=None, departments=Department.query.order_by(Department.name).all())

@admin_bp.route('/courses/<int:id>/edit', methods=['GET','POST'])
@login_required
def course_edit(id):
    x=db.session.get(Course,id)
    if not x: return 'Not found',404
    if request.method == 'POST':
        x.name=request.form.get('name','').strip(); x.code=request.form.get('code','').strip(); x.level=request.form.get('level','').strip()
        x.duration=request.form.get('duration','').strip(); x.entry_requirements=request.form.get('entry_requirements','').strip()
        x.description=request.form.get('description','').strip(); x.department_id=request.form.get('department_id') or None
        db.session.commit(); flash('Course updated.','success'); return redirect(url_for('admin.courses'))
    return render_template('admin/course_form.html', item=x, departments=Department.query.order_by(Department.name).all())

@admin_bp.route('/courses/<int:id>/delete', methods=['POST'])
@login_required
def course_delete(id):
    x=db.session.get(Course,id)
    if x: db.session.delete(x); db.session.commit()
    return redirect(url_for('admin.courses'))

# ---------------- Admissions ----------------
@admin_bp.route('/admissions', methods=['GET','POST'])
@login_required
def admissions():
    x=AdmissionInfo.query.first()
    if not x:
        x=AdmissionInfo(); db.session.add(x)
    if request.method=='POST':
        x.title=request.form.get('title','').strip() or 'Admissions'
        x.content=request.form.get('content','').strip(); x.requirements=request.form.get('requirements','').strip()
        x.application_steps=request.form.get('application_steps','').strip(); x.important_dates=request.form.get('important_dates','').strip(); x.contact=request.form.get('contact','').strip()
        db.session.commit(); flash('Admissions information saved.','success'); return redirect(url_for('admin.admissions'))
    return render_template('admin/admissions.html', item=x)

@admin_bp.route('/announcements')
@login_required
def announcements():
    return render_template('admin/announcements.html', items=Announcement.query.order_by(Announcement.created_at.desc()).all())

@admin_bp.route('/announcements/add', methods=['GET','POST'])
@login_required
def announcement_add():
    if request.method=='POST':
        x=Announcement(title=request.form.get('title','').strip(), content=request.form.get('content','').strip(), published=request.form.get('published')=='on')
        db.session.add(x); db.session.commit(); flash('Announcement added.','success'); return redirect(url_for('admin.announcements'))
    return render_template('admin/announcement_form.html', item=None)

@admin_bp.route('/announcements/<int:id>/edit', methods=['GET','POST'])
@login_required
def announcement_edit(id):
    x=db.session.get(Announcement,id)
    if not x:return 'Not found',404
    if request.method=='POST':
        x.title=request.form.get('title','').strip(); x.content=request.form.get('content','').strip(); x.published=request.form.get('published')=='on'
        db.session.commit(); flash('Announcement updated.','success'); return redirect(url_for('admin.announcements'))
    return render_template('admin/announcement_form.html', item=x)

@admin_bp.route('/announcements/<int:id>/delete', methods=['POST'])
@login_required
def announcement_delete(id):
    x=db.session.get(Announcement,id)
    if x:db.session.delete(x);db.session.commit()
    return redirect(url_for('admin.announcements'))

# ---------------- Buildings & Facilities ----------------
@admin_bp.route('/buildings')
@login_required
def buildings():
    return render_template('admin/buildings.html', items=Building.query.order_by(Building.id.desc()).all())

@admin_bp.route('/buildings/add', methods=['GET','POST'])
@login_required
def building_add():
    if request.method == 'POST':
        x=Building(name=request.form.get('name','').strip(), category=request.form.get('category','').strip(),
                   location=request.form.get('location','').strip(), description=request.form.get('description','').strip(),
                   facilities=request.form.get('facilities','').strip(), status=request.form.get('status','Active').strip(),
                   image=save_upload(request.files.get('image'), IMAGE))
        if not x.name:
            flash('Building name is required.','danger')
        else:
            db.session.add(x); db.session.commit(); flash('Building added.','success'); return redirect(url_for('admin.buildings'))
    return render_template('admin/building_form.html', item=None)

@admin_bp.route('/buildings/<int:id>/edit', methods=['GET','POST'])
@login_required
def building_edit(id):
    x=db.session.get(Building,id)
    if not x:return 'Not found',404
    if request.method == 'POST':
        x.name=request.form.get('name','').strip(); x.category=request.form.get('category','').strip()
        x.location=request.form.get('location','').strip(); x.description=request.form.get('description','').strip()
        x.facilities=request.form.get('facilities','').strip(); x.status=request.form.get('status','Active').strip()
        new=save_upload(request.files.get('image'),IMAGE)
        if new: delete_upload(x.image); x.image=new
        db.session.commit(); flash('Building updated.','success'); return redirect(url_for('admin.buildings'))
    return render_template('admin/building_form.html', item=x)

@admin_bp.route('/buildings/<int:id>/delete', methods=['POST'])
@login_required
def building_delete(id):
    x=db.session.get(Building,id)
    if x: delete_upload(x.image); db.session.delete(x); db.session.commit()
    return redirect(url_for('admin.buildings'))
