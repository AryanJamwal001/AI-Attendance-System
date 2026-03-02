from flask import Blueprint, render_template, Response, redirect, url_for
from datetime import datetime
from .camera import generate_frames, get_current_name
from .models import db, Attendance

main = Blueprint('main', __name__)

@main.route('/')
def home():
    records = Attendance.query.all()
    return render_template('dashboard.html', records=records)

@main.route('/attendance')
def attendance():
    return render_template('attendance.html')

@main.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@main.route('/mark/<name>')
def mark(name):
    today = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M:%S")

    existing = Attendance.query.filter_by(name=name, date=today).first()

    if not existing:
        new_entry = Attendance(name=name, date=today, time=now_time)
        db.session.add(new_entry)
        db.session.commit()

    return redirect(url_for('main.home'))

@main.route('/current_name')
def current_name():
    return {"name": get_current_name()}
