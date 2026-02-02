# app/events/routes.py - COMPLETE FIXED FILE
from flask import render_template, flash, redirect, url_for, request, session, jsonify
from flask_login import login_required, current_user
from app.models import db, Event, User
from datetime import datetime, timedelta

# Import events_bp from the events package
from app.events import events_bp


@events_bp.route('/')
def events_home():
    """Main events page - shows approved events"""
    # Get filter parameters
    filter_type = request.args.get('type', 'all')
    filter_category = request.args.get('category', 'all')
    filter_date = request.args.get('date', 'upcoming')

    # Base query - only approved events
    query = Event.query.filter_by(status='approved')

    # Apply filters
    if filter_type != 'all':
        query = query.filter_by(event_type=filter_type)

    if filter_category != 'all':
        query = query.filter_by(category=filter_category)

    # Date filtering
    today = datetime.utcnow().date()
    if filter_date == 'today':
        query = query.filter(db.func.date(Event.start_date) == today)
    elif filter_date == 'week':
        week_end = today + timedelta(days=7)
        query = query.filter(db.func.date(Event.start_date).between(today, week_end))
    elif filter_date == 'month':
        month_end = today + timedelta(days=30)
        query = query.filter(db.func.date(Event.start_date).between(today, month_end))
    elif filter_date == 'past':
        query = query.filter(db.func.date(Event.start_date) < today)
    else:  # upcoming (default)
        query = query.filter(db.func.date(Event.start_date) >= today)

    # Order by date
    events = query.order_by(Event.start_date.asc()).all()

    # Calculate counts for stats
    upcoming_count = Event.query.filter_by(status='approved') \
        .filter(Event.start_date >= datetime.utcnow()).count()

    approved_count = Event.query.filter_by(status='approved').count()

    pending_count = Event.query.filter_by(status='pending').count()

    return render_template('events/home.html',
                           events=events,
                           user=current_user,
                           filter_type=filter_type,
                           filter_category=filter_category,
                           filter_date=filter_date,
                           upcoming_count=upcoming_count,
                           approved_count=approved_count,
                           pending_count=pending_count,
                           now=datetime.utcnow().date())


@events_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
    """Create a new event (requires login)"""
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        event_type = request.form.get('event_type', '').strip()
        category = request.form.get('category', '').strip()
        venue = request.form.get('venue', '').strip()
        organizer_name = request.form.get('organizer_name', '').strip()
        contact_email = request.form.get('contact_email', '').strip()
        contact_phone = request.form.get('contact_phone', '').strip()

        # Date parsing
        start_date_str = request.form.get('start_date', '').strip()
        start_time_str = request.form.get('start_time', '').strip()
        end_date_str = request.form.get('end_date', '').strip()
        end_time_str = request.form.get('end_time', '').strip()

        # Validation
        errors = []
        if not title:
            errors.append('Event title is required')
        if not description:
            errors.append('Event description is required')
        if not event_type:
            errors.append('Event type is required')
        if not venue:
            errors.append('Venue is required')
        if not start_date_str:
            errors.append('Start date is required')
        if not start_time_str:
            errors.append('Start time is required')

        if errors:
            for error in errors:
                flash(error, 'danger')
        else:
            # Parse dates
            try:
                start_datetime = datetime.strptime(f"{start_date_str} {start_time_str}", "%Y-%m-%d %H:%M")
                end_datetime = datetime.strptime(f"{end_date_str} {end_time_str}",
                                                 "%Y-%m-%d %H:%M") if end_date_str else None
            except ValueError:
                flash('Invalid date format', 'danger')
                return redirect(url_for('events.create_event'))

            # Create event
            event = Event(
                title=title,
                description=description,
                event_type=event_type,
                category=category,
                venue=venue,
                organizer_name=organizer_name or current_user.get_full_name(),
                contact_email=contact_email or current_user.email,
                contact_phone=contact_phone,
                start_date=start_datetime,
                end_date=end_datetime,
                user_id=current_user.id
            )

            db.session.add(event)
            db.session.commit()

            flash('Event submitted successfully! It will be reviewed by leadership.', 'success')
            return redirect(url_for('events.my_events'))

    return render_template('events/create.html', now=datetime.utcnow().date())


@events_bp.route('/my-events')
@login_required
def my_events():
    """Show events created by current user"""
    events = Event.query.filter_by(user_id=current_user.id) \
        .order_by(Event.created_at.desc()) \
        .all()

    return render_template('events/my_events.html', events=events, user=current_user)


@events_bp.route('/pending')
@login_required
def pending_events():
    """Show pending events (admin/leader only)"""
    if not current_user.can_approve_events():
        flash('You do not have permission to access this page', 'danger')
        return redirect(url_for('events.events_home'))

    pending_events = Event.query.filter_by(status='pending') \
        .order_by(Event.created_at.asc()) \
        .all()

    return render_template('events/pending.html',
                           events=pending_events,
                           user=current_user)


@events_bp.route('/approve/<int:event_id>', methods=['POST'])
@login_required
def approve_event(event_id):
    """Approve an event (admin/leader only)"""
    if not current_user.can_approve_events():
        return jsonify({'success': False, 'error': 'Not authorized'}), 403

    event = Event.query.get_or_404(event_id)

    if event.status != 'pending':
        return jsonify({'success': False, 'error': 'Event is not pending'}), 400

    # Approve the event
    event.status = 'approved'
    event.approved_by = current_user.id
    event.approved_at = datetime.utcnow()
    event.rejection_reason = None

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Event approved successfully'
    })


@events_bp.route('/reject/<int:event_id>', methods=['POST'])
@login_required
def reject_event(event_id):
    """Reject an event (admin/leader only)"""
    if not current_user.can_approve_events():
        return jsonify({'success': False, 'error': 'Not authorized'}), 403

    event = Event.query.get_or_404(event_id)

    if event.status != 'pending':
        return jsonify({'success': False, 'error': 'Event is not pending'}), 400

    rejection_reason = request.json.get('reason', '').strip()

    if not rejection_reason:
        return jsonify({'success': False, 'error': 'Rejection reason is required'}), 400

    # Reject the event
    event.status = 'rejected'
    event.approved_by = current_user.id
    event.approved_at = datetime.utcnow()
    event.rejection_reason = rejection_reason

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Event rejected successfully'
    })


@events_bp.route('/calendar')
def events_calendar():
    """Events calendar view"""
    # Get all approved events
    events = Event.query.filter_by(status='approved') \
        .filter(Event.start_date >= datetime.utcnow()) \
        .order_by(Event.start_date.asc()) \
        .all()

    # Format events for calendar
    calendar_events = []
    for event in events:
        calendar_events.append({
            'id': event.id,
            'title': event.title,
            'start': event.start_date.isoformat(),
            'end': event.end_date.isoformat() if event.end_date else None,
            'url': f"/events/{event.id}",
            'color': get_event_color(event.event_type),
            'description': event.description[:100] + '...' if len(event.description) > 100 else event.description
        })

    return render_template('events/calendar.html',
                           calendar_events=calendar_events,
                           user=current_user)


@events_bp.route('/<int:event_id>')
def view_event(event_id):
    """View a single event"""
    event = Event.query.get_or_404(event_id)

    # Only show approved events to non-admins
    if event.status != 'approved' and (not current_user.is_authenticated or not current_user.can_approve_events()):
        if current_user.is_authenticated and event.user_id == current_user.id:
            # User can view their own pending/rejected events
            pass
        else:
            flash('This event is not available', 'warning')
            return redirect(url_for('events.events_home'))

    return render_template('events/view.html',
                           event=event,
                           user=current_user)


@events_bp.route('/delete/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    """Delete an event (owner or admin only)"""
    event = Event.query.get_or_404(event_id)

    # Check permissions
    if event.user_id != current_user.id and not current_user.can_approve_events():
        return jsonify({'success': False, 'error': 'Not authorized'}), 403

    db.session.delete(event)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Event deleted successfully'})


# Helper function
def get_event_color(event_type):
    colors = {
        'academic': '#0056b3',  # Blue
        'sports': '#28a745',  # Green
        'cultural': '#ffc107',  # Yellow
        'religious': '#17a2b8',  # Teal
        'social': '#dc3545',  # Red
        'workshop': '#6f42c1',  # Purple
        'seminar': '#20c997',  # Teal green
        'competition': '#fd7e14'  # Orange
    }
    return colors.get(event_type, '#6c757d')  # Default gray