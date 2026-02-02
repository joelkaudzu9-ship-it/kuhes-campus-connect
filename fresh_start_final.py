# fresh_start_final.py - UPDATED
import os
import sys
import time
from app import create_app, db
from datetime import datetime, timedelta


def fresh_start_final():
    print("🚀 Starting fresh KUHES Campus Connect setup...")

    # Remove old database files
    db_files = ['kuhes.db', 'instance/kuhes.db', 'app/instance/kuhes.db']
    for db_file in db_files:
        if os.path.exists(db_file):
            try:
                os.remove(db_file)
                print(f"✅ Deleted: {db_file}")
            except PermissionError:
                print(f"⚠️  Could not delete {db_file} (file in use)")
                print("   Please stop any running Flask servers (Ctrl+C in the terminal)")
                return

    # Wait a moment
    time.sleep(1)

    # Create app
    app = create_app()

    with app.app_context():
        print("🔄 Creating new database tables...")

        # IMPORTANT: Create tables BEFORE importing models
        db.create_all()
        print("✅ Database tables created")

        # Now import models
        from app.models import User, Post, Comment, Event

        # Create a test user
        print("👤 Creating test user...")
        test_user = User(
            username='test',
            email='test@kuhes.edu',
            first_name='Test',
            last_name='User',
            faculty='Medicine',
            program='MBBS',
            year='3',
            role='student'
        )
        test_user.set_password('password123')
        db.session.add(test_user)

        # Create admin user
        print("👑 Creating admin user...")
        admin_user = User(
            username='admin',
            email='admin@kuhes.edu',
            first_name='Campus',
            last_name='Admin',
            faculty='Administration',
            program='Management',
            year='Staff',
            role='admin'
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)

        # Create faculty user
        print("👨‍🏫 Creating faculty user...")
        faculty_user = User(
            username='dr_smith',
            email='smith@kuhes.edu',
            first_name='John',
            last_name='Smith',
            faculty='Medicine',
            program='Cardiology',
            year='Faculty',
            role='faculty'
        )
        faculty_user.set_password('faculty123')
        db.session.add(faculty_user)

        # Commit users first to get their IDs
        db.session.commit()
        print(f"✅ Created users with IDs: test=1, admin=2, dr_smith=3")

        # Create sample posts
        print("📝 Creating sample posts...")

        # Post 1
        post1 = Post(
            title='Welcome to KUHES Campus Connect!',
            content='Welcome to our new platform for connecting students, faculty, and staff. Share news, events, and resources here!\n\nThis platform is designed specifically for health sciences students to collaborate and support each other.',
            user_id=1
        )
        db.session.add(post1)

        # Post 2
        post2 = Post(
            title='Health Sciences Symposium 2024',
            content='Join us for the annual Health Sciences Symposium on March 15th. All students are encouraged to participate and present their research.\n\nVenue: Main Auditorium\nTime: 10:00 AM - 4:00 PM\nRegistration required.',
            user_id=1
        )
        db.session.add(post2)

        # Post 3
        post3 = Post(
            title='Sports Day Announcement',
            content='University Sports Day will be held on March 20th. Register your teams at the sports office.\n\nEvents include: Football, Basketball, Athletics, and Medical Relay Race!',
            user_id=1
        )
        db.session.add(post3)

        # Post 4
        post4 = Post(
            title='Library Extended Hours During Exams',
            content='The main library will have extended hours during the exam period:\n\n- Monday to Friday: 7:00 AM - 11:00 PM\n- Weekends: 8:00 AM - 10:00 PM\n\nAdditional study spaces are also available in Block B.',
            user_id=1
        )
        db.session.add(post4)

        # Post 5
        post5 = Post(
            title='Research Paper Writing Workshop',
            content='The Research Department is organizing a workshop on academic writing and research paper formatting.\n\nDate: March 18th\nTime: 2:00 PM - 5:00 PM\nLocation: Room 302, Academic Block',
            user_id=1
        )
        db.session.add(post5)

        # Create sample events
        print("📅 Creating sample events...")
        sample_events = [
            {
                'title': 'Health Sciences Symposium 2024',
                'description': 'Annual symposium for all health sciences students to present research and network with professionals.',
                'event_type': 'academic',
                'category': 'conference',
                'venue': 'Main Auditorium',
                'organizer_name': 'Dean of Medicine',
                'contact_email': 'symposium@kuhes.edu',
                'start_date': datetime.utcnow() + timedelta(days=30),
                'end_date': datetime.utcnow() + timedelta(days=30, hours=6),
                'user_id': 1,
                'status': 'approved'
            },
            {
                'title': 'Medical Career Fair',
                'description': 'Meet representatives from hospitals, research centers, and healthcare organizations.',
                'event_type': 'academic',
                'category': 'seminar',
                'venue': 'Student Union Building',
                'organizer_name': 'Career Services',
                'contact_email': 'careers@kuhes.edu',
                'start_date': datetime.utcnow() + timedelta(days=15),
                'end_date': datetime.utcnow() + timedelta(days=15, hours=8),
                'user_id': 2,
                'status': 'approved'
            },
            {
                'title': 'Inter-faculty Sports Tournament',
                'description': 'Annual sports competition between Medicine, Nursing, Pharmacy, and Public Health faculties.',
                'event_type': 'sports',
                'category': 'competition',
                'venue': 'University Sports Complex',
                'organizer_name': 'Sports Committee',
                'start_date': datetime.utcnow() + timedelta(days=10),
                'end_date': datetime.utcnow() + timedelta(days=10, hours=5),
                'user_id': 1,
                'status': 'approved'
            },
            {
                'title': 'Cultural Night',
                'description': 'Celebrating the diverse cultures of KUHES students with food, music, and performances.',
                'event_type': 'cultural',
                'category': 'celebration',
                'venue': 'Main Quadrangle',
                'organizer_name': 'Student Council',
                'start_date': datetime.utcnow() + timedelta(days=20),
                'end_date': datetime.utcnow() + timedelta(days=20, hours=4),
                'user_id': 1,
                'status': 'pending'
            },
            {
                'title': 'CPR and First Aid Workshop',
                'description': 'Free workshop on basic life support and emergency response techniques.',
                'event_type': 'workshop',
                'category': 'workshop',
                'venue': 'Medical Simulation Lab',
                'organizer_name': 'Emergency Medicine Dept',
                'contact_email': 'ems@kuhes.edu',
                'start_date': datetime.utcnow() + timedelta(days=5),
                'end_date': datetime.utcnow() + timedelta(days=5, hours=3),
                'user_id': 3,
                'status': 'approved'
            }
        ]

        for event_data in sample_events:
            event = Event(
                title=event_data['title'],
                description=event_data['description'],
                event_type=event_data['event_type'],
                category=event_data['category'],
                venue=event_data['venue'],
                organizer_name=event_data['organizer_name'],
                contact_email=event_data.get('contact_email', ''),
                contact_phone=event_data.get('contact_phone', ''),
                start_date=event_data['start_date'],
                end_date=event_data['end_date'],
                user_id=event_data['user_id'],
                status=event_data['status'],
                approved_by=2 if event_data['status'] == 'approved' else None,
                approved_at=datetime.utcnow() if event_data['status'] == 'approved' else None
            )
            db.session.add(event)

        # Create some sample comments
        print("💬 Creating sample comments...")
        sample_comments = [
            {'post_id': 1, 'content': 'This platform looks amazing! Can\'t wait to connect with other med students.'},
            {'post_id': 1, 'content': 'Great initiative! This will really help us stay connected.'},
            {'post_id': 2, 'content': 'I\'m presenting my research on cardiovascular diseases. Looking forward to it!'},
            {'post_id': 2, 'content': 'Will there be certificates for participants?'},
            {'post_id': 3, 'content': 'Our pharmacy team is ready for the relay race! 💊'},
            {'post_id': 4, 'content': 'Thank you for extending library hours. This helps a lot during exams.'},
            {'post_id': 5, 'content': 'This workshop is much needed. I always struggle with formatting.'}
        ]

        for comment_data in sample_comments:
            comment = Comment(
                content=comment_data['content'],
                user_id=1,
                post_id=comment_data['post_id']
            )
            db.session.add(comment)

        # Commit everything
        db.session.commit()

        print("\n✅ Setup complete!")
        print("\n📋 Test Credentials:")
        print("   1. Student Account:")
        print("      👤 Username: test")
        print("      🔐 Password: password123")
        print("      🎯 Role: Student")
        print("\n   2. Admin Account:")
        print("      👤 Username: admin")
        print("      🔐 Password: admin123")
        print("      🎯 Role: Admin (can approve events)")
        print("\n   3. Faculty Account:")
        print("      👤 Username: dr_smith")
        print("      🔐 Password: faculty123")
        print("      🎯 Role: Faculty (can approve events)")
        print("\n📊 Sample data created:")
        print(f"   👥 {User.query.count()} users")
        print(f"   📝 {Post.query.count()} posts")
        print(f"   📅 {Event.query.count()} events (4 approved, 1 pending)")
        print(f"   💬 {Comment.query.count()} comments")
        print("\n🚀 Start the app with: python run.py")
        print("🌐 Then visit: http://localhost:5000")


if __name__ == '__main__':
    try:
        fresh_start_final()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()