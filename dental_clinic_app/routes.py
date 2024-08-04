from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from dental_clinic_app import app, db
from dental_clinic_app.models import User, Appointment
from dental_clinic_app.forms import LoginForm, RegistrationForm, AppointmentForm
from datetime import datetime, timedelta

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    today = datetime.now().date()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())
    
    # Formato de fecha para mostrar
    today_formatted = f"Hoy: {today.strftime('%d/%m/%Y')}"
    
    # Obtener todas las citas del mes actual para el calendario
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    month_appointments = Appointment.query.filter(
        Appointment.date >= start_of_month,
        Appointment.date <= end_of_month
    ).all()
    
    # Formatear las citas para FullCalendar
    events = [
        {
            'title': appointment.patient_name,
            'start': appointment.date.isoformat(),
            'allDay': False
        } for appointment in month_appointments
    ]
    
    # Obtener las citas del día actual
    today_appointments = Appointment.query.filter(
        Appointment.date >= start_of_day,
        Appointment.date <= end_of_day
    ).order_by(Appointment.date).all()
    
    # Crear el cronograma diario
    hours = []
    for h in range(7, 20):
        if h == 12:
            hours.append("12:00 PM")
        elif h < 12:
            hours.append(f"{h:02d}:00 AM")
        else:
            hours.append(f"{h-12:02d}:00 PM")
    
    daily_schedule = []
    for hour in hours:
        hour_time = datetime.strptime(hour, "%I:%M %p").time()
        hour_appointments = [apt for apt in today_appointments if apt.date.time().hour == hour_time.hour]
        daily_schedule.append((hour, hour_appointments))
    
    return render_template('dashboard.html', 
                           today_formatted=today_formatted,
                           events=events,
                           daily_schedule=daily_schedule)


@app.route('/appointment', methods=['GET', 'POST'])
@login_required
def appointment():
    form = AppointmentForm()
    if form.validate_on_submit():
        appointment = Appointment(
            patient_name=form.patient_name.data,
            date=form.date.data,
            doctor=form.doctor.data,
            code=form.code.data,
            affiliation=form.affiliation.data,
            phone=form.phone.data,
            subject=form.subject.data
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment scheduled successfully')
        return redirect(url_for('dashboard'))
    return render_template('appointment.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/update_schedule', methods=['POST'])
@login_required
def update_schedule():
    time_unit = request.json['timeUnit']
    # Aquí implementarías la lógica para actualizar el cronograma basado en la nueva unidad de tiempo
    # Por ahora, simplemente devolvemos un mensaje de éxito
    return jsonify({'status': 'success', 'message': f'Cronograma actualizado con unidad de tiempo: {time_unit} minutos'})