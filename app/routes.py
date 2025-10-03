import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request, abort, current_app, jsonify, make_response
from app import db, mail
from app.forms import ContactForm, PostForm, JobForm
from app.models import User, Post, Job
from flask_login import current_user, login_required
from app.auth import admin_required
from flask import Blueprint
from flask_mail import Message

bp = Blueprint('main', __name__)

# --- Helper Function to Save Uploaded Images ---
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], picture_fn)

    output_size = (1200, 1200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

# --- Main Page Routes ---

@bp.route('/')
@bp.route('/home')
def index():
    recent_posts = Post.query.order_by(Post.timestamp.desc()).limit(3).all()
    return render_template('home.html', title='Home', posts=recent_posts)

@bp.route('/about')
def about():
    return render_template('about.html', title='About Us')

@bp.route('/services')
def services():
    return render_template('services.html', title='Our Services')

@bp.route('/for-clients')
def for_clients():
    return render_template('for_clients.html', title='For Clients')

@bp.route('/for-hire')
def for_hire():
    return render_template('for_hire.html', title='For Hire')

@bp.route('/careers')
def careers():
    jobs = Job.query.order_by(Job.id).all()
    return render_template('careers.html', title='Careers', jobs=jobs)

@bp.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            msg_to_company = Message(
                subject=f"SPIConsulting New Contact Form Submission from {form.name.data}",
                sender=current_app.config['MAIL_USERNAME'],
                recipients=current_app.config['ADMINS']
            )
            msg_to_company.body = f"""
            Name: {form.name.data}
            Email: {form.email.data}
            Service of Interest: {dict(form.service.choices).get(form.service.data)}
            Message: {form.message.data}
            """
            mail.send(msg_to_company)

            msg_to_user = Message(
                subject="Thank you for contacting SkilledProfessionalsIndia Consulting",
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[form.email.data]
            )
            msg_to_user.body = "Thank you for your message! We will get back to you shortly."
            mail.send(msg_to_user)

            flash('Thank you for your message! A confirmation has been sent to your email.', 'success')
        except Exception as e:
            current_app.logger.error(f"Mail sending failed: {e}")
            flash('Sorry, there was an error sending your message. Please try again later.', 'danger')
        return redirect(url_for('main.contact'))
    return render_template('contact.html', title='Contact Us', form=form)

@bp.route('/terms')
def terms():
    return render_template('terms.html', title='Terms of Service')

@bp.route('/privacy')
def privacy():
    return render_template('privacy.html', title='Privacy Policy')

# --- Blog Post Routes (CRUD - Admin Only) ---

@bp.route('/blog')
def blog():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('blog.html', title='Blog', posts=posts)

@bp.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@bp.route('/create_post', methods=['GET', 'POST'])
@login_required
@admin_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        image_filename = 'default_post.jpg'
        if form.image_upload.data:
            image_filename = save_picture(form.image_upload.data)
        elif form.image_url.data:
            image_filename = form.image_url.data
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=current_user,
            image_file=image_filename
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.blog'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@bp.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
@admin_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if not current_user.is_admin:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.image_upload.data:
            post.image_file = save_picture(form.image_upload.data)
        elif form.image_url.data:
            post.image_file = form.image_url.data
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        if post.image_file and post.image_file.startswith('http'):
            form.image_url.data = post.image_file
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if not current_user.is_admin:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', 'success')
    return redirect(url_for('main.blog'))

# --- Job Posting Routes (CRUD - Admin Only) ---

@bp.route('/career/<int:job_id>')
def job_opening(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job_opening.html', title=job.title, job=job)

@bp.route('/create_job', methods=['GET', 'POST'])
@login_required
@admin_required
def create_job():
    form = JobForm()
    if form.validate_on_submit():
        job = Job(title=form.title.data, location=form.location.data, job_type=form.job_type.data, description=form.description.data)
        db.session.add(job)
        db.session.commit()
        flash('The job posting has been created.', 'success')
        return redirect(url_for('main.careers'))
    return render_template('create_job.html', title='Create Job Posting', form=form)

@bp.route('/job/<int:job_id>/update', methods=['GET', 'POST'])
@login_required
@admin_required
def update_job(job_id):
    job = Job.query.get_or_404(job_id)
    form = JobForm()
    if form.validate_on_submit():
        job.title = form.title.data
        job.location = form.location.data
        job.job_type = form.job_type.data
        job.description = form.description.data
        db.session.commit()
        flash('The job posting has been updated.', 'success')
        return redirect(url_for('main.job_opening', job_id=job.id))
    elif request.method == 'GET':
        form.title.data = job.title
        form.location.data = job.location
        form.job_type.data = job.job_type
        form.description.data = job.description
    return render_template('create_job.html', title='Update Job Posting', form=form)

@bp.route('/job/<int:job_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash('The job posting has been deleted.', 'success')
    return redirect(url_for('main.careers'))

# --- Admin Data Export Route ---

@bp.route('/export/download')
@login_required
@admin_required
def download_export():
    try:
        users = User.query.all()
        users_data = [{'id': u.id, 'username': u.username, 'email': u.email, 'is_admin': u.is_admin} for u in users]
        posts = Post.query.all()
        posts_data = [{'id': p.id, 'title': p.title, 'content': p.content, 'timestamp': p.timestamp.isoformat(), 'author_username': p.author.username} for p in posts]
        jobs = Job.query.all()
        jobs_data = [{'id': j.id, 'title': j.title, 'location': j.location, 'job_type': j.job_type, 'description': j.description} for j in jobs]
        full_export = {'users': users_data, 'posts': posts_data, 'jobs': jobs_data}
        response = jsonify(full_export)
        response.headers['Content-Disposition'] = 'attachment; filename=full_database_export.json'
        return response
    except Exception as e:
        flash(f'An error occurred during the export: {e}', 'danger')
        return redirect(url_for('main.index'))
    
    
    
    

# --- UPDATED ROUTE TO GENERATE SITEMAP.XML ---
@bp.route('/sitemap.xml')
def sitemap():
    """Generates the sitemap.xml file dynamically."""
    base_url = request.url_root
    lastmod_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+00:00')

    # Get all published blog posts
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    
    # Get all active job openings
    jobs = Job.query.order_by(Job.id).all()

    # List of static pages to include
    static_pages = [
        'main.home', 'main.about', 'main.services', 'main.for_clients',
        'main.for_hire', 'main.careers', 'main.blog', 'main.contact',
        'main.terms', 'main.privacy',
        'auth.login', 'auth.register'
    ]

    # Render the sitemap template
    sitemap_xml = render_template('sitemap.xml', 
                                  posts=posts, 
                                  jobs=jobs, 
                                  static_pages=static_pages,
                                  base_url=base_url,
                                  lastmod_date=lastmod_date)
    
    # Create a response with the correct XML content type
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'
    
    return response

