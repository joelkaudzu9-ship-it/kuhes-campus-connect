
# app/forum/routes.py - FIXED
from flask import render_template, request
from flask_login import current_user
from app.models import Post, Comment
from app import db

# Import forum_bp from the forum package
from app.forum import forum_bp

# ... rest of your forum routes code ...


@forum_bp.route('/')
def forum_home():
    category = request.args.get('category', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    query = Post.query

    if category != 'all':
        query = query.filter_by(category=category)

    posts = query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False)

    return render_template('forum/home.html',
                           posts=posts,
                           category=category,
                           user=current_user)


@forum_bp.route('/categories')
def categories():
    # Get all unique categories from posts
    categories = db.session.query(Post.category).distinct().all()
    category_list = [cat[0] for cat in categories if cat[0]]

    # Get post count per category
    category_counts = {}
    for category in category_list:
        count = Post.query.filter_by(category=category).count()
        category_counts[category] = count

    return render_template('forum/categories.html',
                           categories=category_list,
                           category_counts=category_counts,
                           user=current_user)


@forum_bp.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    if query:
        posts = Post.query.filter(
            (Post.title.ilike(f'%{query}%')) |
            (Post.content.ilike(f'%{query}%'))
        ).order_by(Post.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False)
    else:
        posts = Post.query.order_by(Post.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False)

    return render_template('forum/search.html',
                           posts=posts,
                           query=query,
                           user=current_user)