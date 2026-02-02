# init_database.py - COMPLETE DATABASE INITIALIZATION
import os
import sys
import time
from datetime import datetime, timedelta

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def initialize_database():
    print("🚀 Initializing KUHES Campus Connect Database...")
    print("=" * 60)

    # Remove old database files
    db_files = ['kuhes.db', 'instance/kuhes.db']
    for db_file in db_files:
        if os.path.exists(db_file):
            try:
                os.remove(db_file)
                print(f"✅ Deleted old database: {db_file}")
                time.sleep(0.5)
            except Exception as e:
                print(f"⚠️  Could not delete {db_file}: {e}")
                print("   Please stop any running Flask servers and try again.")
                return

    # Create app instance
    from app import create_app, db
    from app.models import User, Post, Comment, Event, PostReaction

    app = create_app()

    with app.app_context():
        print("\n🔄 Creating database tables...")
        db.create_all()
        print("✅ Database schema created successfully")

        # Create sample users
        print("\n👥 Creating sample users...")

        users_data = [
            {
                'username': 'test_student',
                'email': 'student@kuhes.edu',
                'first_name': 'John',
                'last_name': 'Student',
                'faculty': 'Medicine',
                'program': 'MBBS',
                'year': '3',
                'password': 'password123',
                'role': 'student'
            },
            {
                'username': 'admin',
                'email': 'admin@kuhes.edu',
                'first_name': 'Campus',
                'last_name': 'Admin',
                'faculty': 'Administration',
                'program': 'Management',
                'year': 'Staff',
                'password': 'admin123',
                'role': 'admin'
            },
            {
                'username': 'dr_smith',
                'email': 'smith@kuhes.edu',
                'first_name': 'John',
                'last_name': 'Smith',
                'faculty': 'Medicine',
                'program': 'Cardiology',
                'year': 'Faculty',
                'password': 'faculty123',
                'role': 'faculty'
            },
            {
                'username': 'nursing_leader',
                'email': 'nursing@kuhes.edu',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'faculty': 'Nursing',
                'program': 'Nursing Science',
                'year': 'Faculty',
                'password': 'nursing123',
                'role': 'leader'
            }
        ]

        created_users = {}
        for user_data in users_data:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                faculty=user_data['faculty'],
                program=user_data['program'],
                year=user_data['year'],
                role=user_data['role']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
            db.session.flush()  # Get the ID
            created_users[user_data['username']] = user.id
            print(f"   ✅ Created {user_data['role']}: {user_data['username']}")

        db.session.commit()

        # Create sample posts
        print("\n📝 Creating sample posts...")

        posts_data = [
            {
                'title': 'Welcome to KUHES Campus Connect!',
                'content': """Welcome everyone to our new campus platform!

This platform is designed to help students, faculty, and staff connect, share information, and collaborate more effectively.

Features include:
• Campus news and announcements
• Event calendar and registration
• Discussion forums by faculty
• Resource sharing
• Study groups
• And much more!

Please take a moment to explore and let us know your feedback.""",
                'category': 'announcement',
                'user_id': created_users['admin']
            },
            {
                'title': 'Health Sciences Symposium 2024 - Call for Abstracts',
                'content': """The annual Health Sciences Symposium will be held on March 15th, 2024.

We are now accepting abstract submissions for:
1. Original research
2. Case studies
3. Literature reviews
4. Quality improvement projects

Important Dates:
• Abstract submission deadline: February 15, 2024
• Notification of acceptance: February 28, 2024
• Symposium date: March 15, 2024

Venue: Main Auditorium
Time: 9:00 AM - 5:00 PM

Submit your abstracts to: symposium@kuhes.edu""",
                'category': 'academic',
                'user_id': created_users['dr_smith']
            },
            {
                'title': 'Library Extended Hours During Examination Period',
                'content': """ATTENTION ALL STUDENTS

The main library will operate on extended hours during the upcoming examination period:

Extended Hours (March 1 - April 15):
• Monday to Friday: 7:00 AM - 11:00 PM
• Saturdays: 8:00 AM - 10:00 PM
• Sundays: 9:00 AM - 9:00 PM

Additional study spaces available:
1. Block B, Rooms 101-105
2. Medical Library (24/7 access for final year students)
3. Nursing Resource Center

Please maintain silence in all study areas.""",
                'category': 'announcement',
                'user_id': created_users['admin']
            },
            {
                'title': 'CPR and Basic Life Support Workshop - Free Certification',
                'content': """The Emergency Medicine Department is organizing a FREE CPR and Basic Life Support workshop.

Details:
• Date: March 10, 2024
• Time: 8:00 AM - 4:00 PM
• Venue: Medical Simulation Lab
• Instructor: Dr. James Wilson (Emergency Medicine Consultant)

What you'll learn:
✓ Adult and pediatric CPR
✓ AED operation
✓ Choking management
✓ Basic first aid

Limited to 30 participants. Register at: ems.workshop@kuhes.edu

Certificates will be provided to all participants who complete the training.""",
                'category': 'workshop',
                'user_id': created_users['dr_smith']
            },
            {
                'title': 'Looking for Biochemistry Study Group Partners',
                'content': """Hi everyone!

I'm a Year 2 MBBS student looking to form a study group for Biochemistry. The exams are coming up and I find group study very effective.

I'm available:
• Mondays & Wednesdays: 4-6 PM
• Saturdays: 10 AM - 1 PM

Preferred location: Medical Library study rooms

If interested, please comment below or message me directly.

Let's ace Biochemistry together! 💪""",
                'category': 'study_group',
                'user_id': created_users['test_student']
            }
        ]

        created_posts = {}
        for i, post_data in enumerate(posts_data, 1):
            post = Post(
                title=post_data['title'],
                content=post_data['content'],
                category=post_data['category'],
                user_id=post_data['user_id']
            )
            db.session.add(post)
            db.session.flush()
            created_posts[i] = post.id
            print(f"   ✅ Created post: {post_data['title'][:40]}...")

        db.session.commit()

        # Create sample events
        print("\n📅 Creating sample events...")

        events_data = [
            {
                'title': 'Health Sciences Symposium 2024',
                'description': 'Annual symposium for all health sciences students to present research and network with professionals from various medical fields.',
                'event_type': 'academic',
                'category': 'conference',
                'venue': 'Main Auditorium',
                'organizer_name': 'Dean of Medicine',
                'contact_email': 'symposium@kuhes.edu',
                'start_date': datetime.utcnow() + timedelta(days=30),
                'end_date': datetime.utcnow() + timedelta(days=30, hours=8),
                'user_id': created_users['admin'],
                'status': 'approved'
            },
            {
                'title': 'Inter-Faculty Sports Tournament',
                'description': 'Annual sports competition between Medicine, Nursing, Pharmacy, and Public Health faculties. Events: Football, Basketball, Volleyball, Athletics.',
                'event_type': 'sports',
                'category': 'competition',
                'venue': 'University Sports Complex',
                'organizer_name': 'Sports Committee',
                'start_date': datetime.utcnow() + timedelta(days=15),
                'end_date': datetime.utcnow() + timedelta(days=15, hours=6),
                'user_id': created_users['test_student'],
                'status': 'approved'
            },
            {
                'title': 'Medical Career Fair 2024',
                'description': 'Meet representatives from leading hospitals, research centers, and healthcare organizations. Bring your CV!',
                'event_type': 'career',
                'category': 'seminar',
                'venue': 'Student Union Building',
                'organizer_name': 'Career Services Office',
                'contact_email': 'careers@kuhes.edu',
                'start_date': datetime.utcnow() + timedelta(days=45),
                'end_date': datetime.utcnow() + timedelta(days=45, hours=7),
                'user_id': created_users['admin'],
                'status': 'approved'
            },
            {
                'title': 'Cultural Diversity Night',
                'description': 'Celebrating the diverse cultures of KUHES students with traditional food, music, dance, and fashion show.',
                'event_type': 'cultural',
                'category': 'celebration',
                'venue': 'Main Quadrangle',
                'organizer_name': 'Student Council',
                'start_date': datetime.utcnow() + timedelta(days=25),
                'end_date': datetime.utcnow() + timedelta(days=25, hours=5),
                'user_id': created_users['test_student'],
                'status': 'pending'
            },
            {
                'title': 'Research Methodology Workshop',
                'description': 'Hands-on workshop on research design, data analysis, and academic writing for health sciences students.',
                'event_type': 'workshop',
                'category': 'workshop',
                'venue': 'Computer Lab 3',
                'organizer_name': 'Research Department',
                'contact_email': 'research@kuhes.edu',
                'start_date': datetime.utcnow() + timedelta(days=10),
                'end_date': datetime.utcnow() + timedelta(days=10, hours=4),
                'user_id': created_users['dr_smith'],
                'status': 'approved'
            }
        ]

        for event_data in events_data:
            event = Event(
                title=event_data['title'],
                description=event_data['description'],
                event_type=event_data['event_type'],
                category=event_data['category'],
                venue=event_data['venue'],
                organizer_name=event_data.get('organizer_name', ''),
                contact_email=event_data.get('contact_email', ''),
                start_date=event_data['start_date'],
                end_date=event_data['end_date'],
                user_id=event_data['user_id'],
                status=event_data['status'],
                approved_by=created_users['admin'] if event_data['status'] == 'approved' else None,
                approved_at=datetime.utcnow() if event_data['status'] == 'approved' else None
            )
            db.session.add(event)
            print(f"   ✅ Created event: {event_data['title'][:40]}... ({event_data['status']})")

        db.session.commit()

        # Create sample comments
        print("\n💬 Creating sample comments...")

        comments_data = [
            {'post_id': created_posts[1],
             'content': 'This platform looks amazing! Finally, a centralized place for all campus activities.',
             'user_id': created_users['test_student']},
            {'post_id': created_posts[1], 'content': 'Great initiative! Looking forward to using this platform.',
             'user_id': created_users['dr_smith']},
            {'post_id': created_posts[2], 'content': 'Will there be prizes for best presentations?',
             'user_id': created_users['test_student']},
            {'post_id': created_posts[2],
             'content': 'Yes, there will be cash prizes for the top 3 presentations in each category.',
             'user_id': created_users['dr_smith']},
            {'post_id': created_posts[3],
             'content': 'Thank you for extending the library hours! This helps a lot during exams.',
             'user_id': created_users['test_student']},
            {'post_id': created_posts[4], 'content': 'Is this workshop open to nursing students as well?',
             'user_id': created_users['nursing_leader']},
            {'post_id': created_posts[4], 'content': 'Yes, it\'s open to all health sciences students!',
             'user_id': created_users['dr_smith']},
            {'post_id': created_posts[5],
             'content': 'I\'m interested in joining the study group! Year 2 Pharmacy here.',
             'user_id': created_users['nursing_leader']},
        ]

        for comment_data in comments_data:
            comment = Comment(
                content=comment_data['content'],
                user_id=comment_data['user_id'],
                post_id=comment_data['post_id']
            )
            db.session.add(comment)

        db.session.commit()

        # Create sample reactions
        print("\n❤️ Creating sample reactions...")

        reactions_data = [
            {'post_id': created_posts[1], 'reaction_type': 'stethoscope', 'user_id': created_users['test_student']},
            {'post_id': created_posts[1], 'reaction_type': 'heartbeat', 'user_id': created_users['dr_smith']},
            {'post_id': created_posts[2], 'reaction_type': 'pill', 'user_id': created_users['test_student']},
            {'post_id': created_posts[2], 'reaction_type': 'syringe', 'user_id': created_users['nursing_leader']},
            {'post_id': created_posts[3], 'reaction_type': 'stethoscope', 'user_id': created_users['test_student']},
            {'post_id': created_posts[4], 'reaction_type': 'heartbeat', 'user_id': created_users['test_student']},
            {'post_id': created_posts[5], 'reaction_type': 'dna', 'user_id': created_users['nursing_leader']},
        ]

        for reaction_data in reactions_data:
            reaction = PostReaction(
                user_id=reaction_data['user_id'],
                post_id=reaction_data['post_id'],
                reaction_type=reaction_data['reaction_type']
            )
            db.session.add(reaction)

        db.session.commit()

        print("\n" + "=" * 60)
        print("✅ DATABASE INITIALIZATION COMPLETE!")
        print("=" * 60)

        # Summary
        print("\n📊 DATABASE SUMMARY:")
        print(f"   👥 Users: {User.query.count()}")
        print(f"   📝 Posts: {Post.query.count()}")
        print(f"   📅 Events: {Event.query.count()} (4 approved, 1 pending)")
        print(f"   💬 Comments: {Comment.query.count()}")
        print(f"   ❤️ Reactions: {PostReaction.query.count()}")

        print("\n🔐 LOGIN CREDENTIALS:")
        print("   " + "-" * 40)
        print("   1. Student Account:")
        print("      👤 Username: test_student")
        print("      🔐 Password: password123")
        print("      🎯 Role: Student")
        print("   " + "-" * 40)
        print("   2. Admin Account:")
        print("      👤 Username: admin")
        print("      🔐 Password: admin123")
        print("      🎯 Role: Admin (can approve events)")
        print("   " + "-" * 40)
        print("   3. Faculty Account:")
        print("      👤 Username: dr_smith")
        print("      🔐 Password: faculty123")
        print("      🎯 Role: Faculty (can approve events)")
        print("   " + "-" * 40)
        print("   4. Nursing Leader:")
        print("      👤 Username: nursing_leader")
        print("      🔐 Password: nursing123")
        print("      🎯 Role: Leader (can approve events)")

        print("\n🚀 STARTING THE APPLICATION:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Run the app: python run.py")
        print("   3. Open browser: http://localhost:5000")
        print("\n✨ Enjoy KUHES Campus Connect!")


if __name__ == '__main__':
    try:
        initialize_database()
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        import traceback

        traceback.print_exc()
        print("\n💡 TROUBLESHOOTING:")
        print("   1. Make sure all dependencies are installed")
        print("   2. Stop any running Flask servers")
        print("   3. Check file permissions")