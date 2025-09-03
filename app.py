from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Teacher, Section, StudentQuery
from config import Config
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config.from_object(Config)


UPLOAD_FOLDER = os.path.join("static", "images")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables
with app.app_context():
    db.create_all()
    # Create admin user if not exists
    if not User.query.filter_by(username='rahul59singh').first():
        admin = User(username='admin', email='princerathaur1302@gmail.com', role='admin')
        admin.set_password('RSMUW@$&59maths')
        db.session.add(admin)
        db.session.commit()

# Routes
@app.route('/')
def index():
    teachers = Teacher.query.all()
    sections = Section.query.all()
    return render_template('index.html', teachers=teachers, sections=sections)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = 'student'  # Default role for registrations
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful. Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            if user.role == 'admin':
                return redirect(next_page or url_for('admin_dashboard'))
            elif user.role == 'teacher':
                return redirect(next_page or url_for('teacher_dashboard'))
            else:
                return redirect(next_page or url_for('index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        
        query = StudentQuery(student_name=name, email=email, phone=phone, message=message)
        db.session.add(query)
        db.session.commit()
        
        flash('Your query has been submitted. We will contact you soon.')
        return redirect(url_for('index'))

# Admin routes
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied')
        return redirect(url_for('index'))
    
    teachers = Teacher.query.count()
    sections = Section.query.count()
    queries = StudentQuery.query.count()
    new_queries = StudentQuery.query.filter_by(status='new').count()
    
    return render_template('admin_dashboard.html', 
                          teachers=teachers, 
                          sections=sections, 
                          queries=queries,
                          new_queries=new_queries)

@app.route('/admin/teachers')
@login_required
def manage_teachers():
    if current_user.role != 'admin':
        flash('Access denied')
        return redirect(url_for('index'))
    
    teachers = Teacher.query.all()
    return render_template('manage_teachers.html', teachers=teachers)


@app.route('/admin/teachers/add', methods=['GET', 'POST'])
@login_required
def add_teacher():
    if current_user.role != 'admin':
        flash('Access denied')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['subject']
        qualification = request.form['qualification']
        experience = request.form['experience']
        description = request.form['description']
        
        teacher = Teacher(
            name=name, 
            subject=subject, 
            qualification=qualification,
            experience=experience,
            description=description
        )
        
        # ✅ Image Upload
        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename != '':
                filename = secure_filename(image.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                image.save(filepath)   # 👈 Image save ho jayegi static/images me
                teacher.image = filename   # filename DB me save hoga
        
        db.session.add(teacher)
        db.session.commit()
        
        flash('Teacher added successfully')
        return redirect(url_for('manage_teachers'))
    
    return render_template('add_teacher.html')

@app.route('/admin/teachers/delete/<int:id>')
@login_required
def delete_teacher(id):
    if current_user.role != 'admin':
        flash('Access denied')
        return redirect(url_for('index'))
    
    teacher = Teacher.query.get_or_404(id)
    db.session.delete(teacher)
    db.session.commit()
    
    flash('Teacher deleted successfully')
    return redirect(url_for('manage_teachers'))

@app.route('/admin/sections')
@login_required
def manage_sections():
    if current_user.role != 'admin':
        flash('Access denied')
        return redirect(url_for('index'))
    
    sections = Section.query.all()
    return render_template('manage_sections.html', sections=sections)

@app.route('/admin/sections/add', methods=['GET', 'POST'])
@login_required
def add_section():
    if current_user.role != 'admin':
        flash('Access denied')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        grade = request.form['grade']
        
        section = Section(
            title=title, 
            description=description,
            grade=grade
        )
        
        # ✅ Image Upload
        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename != '':
                filename = secure_filename(image.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                image.save(filepath)   # 👈 Image file static/images me save hogi
                section.image = filename   # filename DB me store hoga
        
        db.session.add(section)
        db.session.commit()
        
        flash('Section added successfully')
        return redirect(url_for('manage_sections'))
    
    return render_template('add_section.html')

@app.route('/admin/sections/delete/<int:id>')
@login_required
def delete_section(id):
    if current_user.role != 'admin':
        flash('Access denied')
        return redirect(url_for('index'))
    
    section = Section.query.get_or_404(id)
    db.session.delete(section)
    db.session.commit()
    
    flash('Section deleted successfully')
    return redirect(url_for('manage_sections'))

@app.route('/admin/queries')
@login_required
def student_queries():
    if current_user.role != 'admin' and current_user.role != 'teacher':
        flash('Access denied')
        return redirect(url_for('index'))
    
    queries = StudentQuery.query.order_by(StudentQuery.created_at.desc()).all()
    return render_template('student_queries.html', queries=queries)

@app.route('/admin/queries/update_status/<int:id>/<status>')
@login_required
def update_query_status(id, status):
    if current_user.role != 'admin' and current_user.role != 'teacher':
        flash('Access denied')
        return redirect(url_for('index'))
    
    query = StudentQuery.query.get_or_404(id)
    query.status = status
    db.session.commit()
    
    flash('Query status updated')
    return redirect(url_for('student_queries'))

# Teacher routes
@app.route('/teacher/dashboard')
@login_required
def teacher_dashboard():
    if current_user.role != 'teacher':
        flash('Access denied')
        return redirect(url_for('index'))
    
    queries = StudentQuery.query.count()
    new_queries = StudentQuery.query.filter_by(status='new').count()
    
    return render_template('teacher_dashboard.html', 
                          queries=queries,
                          new_queries=new_queries)

if __name__ == '__main__':
    app.run(debug=True)
