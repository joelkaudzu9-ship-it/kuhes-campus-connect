# update_reactions_db.py
import os
import sys
from app import create_app, db
from app.models import User, Post, PostReaction, Comment

print("🔄 Updating database with new reactions system...")

# Remove old database
db_files = ['kuhes.db', 'instance/kuhes.db']
for db_file in db_files:
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"✅ Deleted: {db_file}")

app = create_app()

with app.app_context():
    # Create all tables with new schema
    db.create_all()
    print("✅ Created new database tables")

    # Create test user
    test_user = User(
        username='test',
        email='test@kuhes.edu',
        first_name='Test',
        last_name='User',
        faculty='Medicine',
        program='MBBS',
        year='3'
    )
    test_user.set_password('password123')
    db.session.add(test_user)

    # Create sample posts
    sample_posts = [
        {
            'title': 'Welcome to KUHES Campus Connect!',
            'content': 'Welcome to our new platform with Facebook-style reactions!',
            'category': 'announcement'
        },
        {
            'title': 'Try the new medical reactions system',
            'content': 'Press and hold the React button to choose from medical reactions!',
            'category': 'news'
        }
    ]

    for post_data in sample_posts:
        post = Post(
            title=post_data['title'],
            content=post_data['content'],
            category=post_data['category'],
            user_id=1
        )
        db.session.add(post)

    db.session.commit()

    print("✅ Sample data created")
    print("\n🚀 Start the app with: python run.py")
    print("👤 Login with: test / password123")
    print("✨ Try the new Facebook-style reactions!")