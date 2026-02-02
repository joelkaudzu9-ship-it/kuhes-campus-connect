# run.py - UPDATED VERSION
from app import create_app

app = create_app()

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 KUHES Campus Connect - Starting Server")
    print("=" * 60)
    print("\n📡 Server running at: http://localhost:5000")
    print("🛑 Press CTRL+C to stop the server")
    print("\n✨ Features Available:")
    print("   • User Authentication & Registration")
    print("   • Campus News & Announcements")
    print("   • Facebook-style Medical Reactions")
    print("   • Event Management System")
    print("   • Discussion Forums")
    print("   • Comments & Interactions")
    print("=" * 60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)