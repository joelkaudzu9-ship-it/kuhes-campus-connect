# run.py - FIXED VERSION
import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get port FIRST

    print("\n" + "=" * 60)
    print("🚀 KUHES Campus Connect - Starting Server")
    print("=" * 60)
    print(f"\n📡 Server running at: http://localhost:{port}")  # FIXED: Use f-string
    print("🛑 Press CTRL+C to stop the server")
    print("\n✨ Features Available:")
    print("   • User Authentication & Registration")
    print("   • Campus News & Announcements")
    print("   • Facebook-style Medical Reactions")
    print("   • Event Management System")
    print("   • Discussion Forums")
    print("   • Comments & Interactions")
    print("=" * 60 + "\n")

    app.run(host="0.0.0.0", port=port)  # Use the port variable