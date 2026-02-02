# app/main/routes.py - FIXED
from flask import render_template, flash, redirect, url_for, request, session, jsonify
from flask_login import login_required, current_user
from app.models import Post, User, Comment, PostReaction
from app import db
from datetime import datetime

# Import main_bp from the main package
from app.main import main_bp

# ... rest of your main routes code ...

# Add to imports at top
from app.models import Notification


# Add these routes after existing ones
@main_bp.route('/notifications')
@login_required
def notifications():
    """View all notifications"""
    page = request.args.get('page', 1, type=int)
    per_page = 20

    notifications = Notification.query.filter_by(user_id=current_user.id) \
        .order_by(Notification.created_at.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    # Mark as read when viewing
    unread_notifications = Notification.query.filter_by(
        user_id=current_user.id, is_read=False
    ).all()

    for notification in unread_notifications:
        notification.is_read = True

    db.session.commit()

    return render_template('main/notifications.html',
                           notifications=notifications,
                           user=current_user)


@main_bp.route('/notifications/count')
@login_required
def notifications_count():
    """Get unread notifications count (for AJAX)"""
    count = Notification.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).count()

    return jsonify({'count': count})


@main_bp.route('/notifications/clear', methods=['POST'])
@login_required
def clear_notifications():
    """Clear all notifications"""
    Notification.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()

    return jsonify({'success': True})


@main_bp.route('/notifications/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    """Mark a notification as read"""
    notification = Notification.query.get_or_404(notification_id)

    # Check ownership
    if notification.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Not authorized'}), 403

    notification.is_read = True
    db.session.commit()

    return jsonify({'success': True})


@main_bp.route('/')
@main_bp.route('/home')
def home():
    from app.models import Post, User, Event, Comment

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    # Get stats for sidebar
    post_count = Post.query.count()
    user_count = User.query.count()
    event_count = Event.query.filter_by(status='approved').count()
    comment_count = Comment.query.count()

    # Get upcoming events for sidebar
    from datetime import datetime
    upcoming_events = Event.query.filter_by(status='approved') \
        .filter(Event.start_date >= datetime.utcnow()) \
        .order_by(Event.start_date.asc()) \
        .limit(5).all()

    return render_template('main/home.html',
                           posts=posts,
                           events=upcoming_events,
                           post_count=post_count,
                           user_count=user_count,
                           event_count=event_count,
                           comment_count=comment_count,
                           user=current_user)


@main_bp.route('/notifications/preview')
@login_required
def notifications_preview():
    """Get preview of recent notifications (for dropdown)"""
    notifications = Notification.query.filter_by(user_id=current_user.id) \
        .order_by(Notification.created_at.desc()) \
        .limit(5) \
        .all()

    notifications_data = []
    for notification in notifications:
        # Calculate time ago
        time_diff = datetime.utcnow() - notification.created_at
        if time_diff.days > 0:
            time_ago = f"{time_diff.days}d ago"
        elif time_diff.seconds > 3600:
            time_ago = f"{time_diff.seconds // 3600}h ago"
        elif time_diff.seconds > 60:
            time_ago = f"{time_diff.seconds // 60}m ago"
        else:
            time_ago = "Just now"

        notifications_data.append({
            'id': notification.id,
            'title': notification.title,
            'message': notification.message,
            'type': notification.notification_type,
            'is_read': notification.is_read,
            'time': time_ago
        })

    return jsonify({'notifications': notifications_data})


@main_bp.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', '').strip()

        if not title:
            flash('Title is required', 'danger')
        elif not content:
            flash('Content is required', 'danger')
        elif not category:
            flash('Category is required', 'danger')
        else:
            post = Post(
                title=title,
                content=content,
                category=category,
                user_id=current_user.id
            )

            db.session.add(post)
            db.session.commit()

            flash('Post created successfully!', 'success')
            return redirect(url_for('main.home'))

    return render_template('main/create_post.html')


@main_bp.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('main/view_post.html',
                           post=post,
                           user=current_user)


@main_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Check if user owns the post or is admin
    if post.user_id != current_user.id and not current_user.is_admin():
        return jsonify({'success': False, 'error': 'Not authorized'}), 403

    db.session.delete(post)
    db.session.commit()

    flash('Post deleted successfully!', 'success')
    return jsonify({'success': True})


@main_bp.route('/post/<int:post_id>/react/<reaction_type>', methods=['POST'])
@login_required
def react_to_post(post_id, reaction_type):
    """Handle post reactions with proper error handling"""
    try:
        # Check authentication
        if not current_user.is_authenticated:
            return jsonify({'success': False, 'error': 'Not authenticated'}), 401

        post = Post.query.get_or_404(post_id)
        user_id = current_user.id

        # Valid medical reactions
        valid_reactions = ['stethoscope', 'heartbeat', 'pill', 'syringe', 'tooth', 'dna', 'remove']

        if reaction_type not in valid_reactions:
            return jsonify({'success': False, 'error': 'Invalid reaction type'}), 400

        # Check if user already reacted to this post
        existing_reaction = PostReaction.query.filter_by(
            post_id=post_id,
            user_id=user_id
        ).first()

        if reaction_type == 'remove':
            # Remove reaction if exists
            if existing_reaction:
                db.session.delete(existing_reaction)
                db.session.commit()

                # Get updated reaction counts
                reaction_counts = post.get_reaction_counts()

                return jsonify({
                    'success': True,
                    'action': 'removed',
                    'reaction_counts': reaction_counts,
                    'user_reaction': None
                })
            else:
                return jsonify({'success': False, 'error': 'No reaction to remove'}), 400
        else:
            # Add or update reaction
            if existing_reaction:
                # Update existing reaction
                if existing_reaction.reaction_type == reaction_type:
                    # Same reaction clicked again - remove it
                    db.session.delete(existing_reaction)
                    action = 'removed'
                    user_reaction = None
                else:
                    # Different reaction - update it
                    existing_reaction.reaction_type = reaction_type
                    action = 'updated'
                    user_reaction = reaction_type
            else:
                # Create new reaction
                new_reaction = PostReaction(
                    user_id=user_id,
                    post_id=post_id,
                    reaction_type=reaction_type
                )
                db.session.add(new_reaction)
                action = 'added'
                user_reaction = reaction_type

            db.session.commit()

            # CREATE NOTIFICATION for post owner (if not reacting to own post)
            if post.user_id != current_user.id:
                reaction_names = {
                    'stethoscope': 'stethoscope',
                    'heartbeat': 'heartbeat',
                    'pill': 'pill',
                    'syringe': 'syringe',
                    'tooth': 'tooth',
                    'dna': 'DNA'
                }

                # Use direct creation instead of static method to avoid issues
                notification = Notification(
                    user_id=post.user_id,
                    title='New Reaction',
                    message=f'{current_user.username} reacted with {reaction_names.get(reaction_type, reaction_type)} to your post "{post.title[:50]}..."',
                    notification_type='post_reaction',
                    related_id=post_id
                )
                db.session.add(notification)
                db.session.commit()

            # Get updated reaction counts
            reaction_counts = post.get_reaction_counts()

            return jsonify({
                'success': True,
                'action': action,
                'reaction_counts': reaction_counts,
                'user_reaction': user_reaction
            })

    except Exception as e:
        db.session.rollback()
        print(f"Error in react_to_post: {str(e)}")  # For debugging
        return jsonify({
            'success': False,
            'error': 'An internal error occurred'
        }), 500


@main_bp.route('/post/<int:post_id>/reactions')
@login_required
def get_post_reactions(post_id):
    """Get all reactions for a post"""
    post = Post.query.get_or_404(post_id)

    # Get reaction counts
    reaction_counts = post.get_reaction_counts()

    # Get user's reaction
    user_reaction = post.get_user_reaction(current_user.id)

    return jsonify({
        'success': True,
        'reaction_counts': reaction_counts,
        'user_reaction': user_reaction,
        'total_reactions': sum(reaction_counts.values())
    })


@main_bp.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    content = request.form.get('content', '').strip()

    if not content:
        return jsonify({'success': False, 'error': 'Comment cannot be empty'}), 400

    post = Post.query.get_or_404(post_id)

    comment = Comment(
        content=content,
        user_id=current_user.id,
        post_id=post_id
    )

    db.session.add(comment)
    db.session.commit()

    # Get the comment with author info
    comment_with_author = Comment.query.get(comment.id)

    return jsonify({
        'success': True,
        'comment': {
            'id': comment.id,
            'content': comment.content,
            'author_name': comment_with_author.author.username,
            'author_full_name': comment_with_author.author.get_full_name(),
            'created_at': comment.created_at.strftime('%b %d, %Y at %I:%M %p')
        }
    })


@main_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    # Check if user owns the comment or the post or is admin
    if comment.user_id != current_user.id and comment.post.user_id != current_user.id and not current_user.is_admin():
        return jsonify({'success': False, 'error': 'Not authorized'}), 403

    db.session.delete(comment)
    db.session.commit()

    return jsonify({'success': True})


@main_bp.route('/news')
def news():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    posts = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False)

    return render_template('main/news.html',
                           posts=posts,
                           user=current_user)


@main_bp.route('/profile')
@login_required
def profile():
    user_posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.created_at.desc()).all()

    return render_template('main/profile.html',
                           user=current_user,
                           posts=user_posts)


@main_bp.route('/profile/<username>')
def view_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    user_posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at.desc()).limit(10).all()

    return render_template('main/view_profile.html',
                           profile_user=user,
                           posts=user_posts,
                           user=current_user)