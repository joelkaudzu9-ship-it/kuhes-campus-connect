# update_notifications.py
import os
import sys
from app import create_app, db
from app.models import Notification

print("🔄 Adding notifications system to database...")

app = create_app()

with app.app_context():
    # Create notifications table
    db.create_all()

    print("✅ Notifications table created successfully!")
    print(f"📊 Total notifications in database: {Notification.query.count()}")

    # Update the database version
    print("\n🎉 Database update complete!")
    print("\n🚀 Restart the application with: python run.py")
    print("🔔 Notifications system is now active!")