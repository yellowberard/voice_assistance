"""
Simple deployment script for Voice Interview Bot
Demonstrates automation and deployment practices
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a shell command with error handling"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking deployment requirements...")
    
    # Check if .env file exists
    if not Path('.env').exists():
        print("❌ .env file not found. Please copy .env.example to .env and configure it.")
        return False
    
    # Check if OpenAI API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OPENAI_API_KEY not set in .env file")
        return False
    
    print("✅ All requirements met")
    return True

def run_tests():
    """Run the test suite"""
    print("🧪 Running tests...")
    result = run_command("python test_app.py", "Running test suite")
    return result is not None

def install_dependencies():
    """Install Python dependencies"""
    return run_command("pip install -r requirements.txt", "Installing dependencies")

def start_local_server():
    """Start the local development server"""
    print("🚀 Starting local development server...")
    print("Visit: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    try:
        subprocess.run("python app.py", shell=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")

def deploy_to_vercel():
    """Deploy to Vercel"""
    print("🌐 Deploying to Vercel...")
    
    # Check if Vercel CLI is installed
    vercel_check = run_command("vercel --version", "Checking Vercel CLI")
    if not vercel_check:
        print("Installing Vercel CLI...")
        run_command("npm install -g vercel", "Installing Vercel CLI")
    
    # Deploy
    result = run_command("vercel --prod", "Deploying to Vercel")
    if result:
        print("🎉 Deployment successful!")
        print("Your voice bot is now live!")

def main():
    """Main deployment function"""
    print("🎤 Voice Interview Bot Deployment Script")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python deploy.py check     - Check requirements")
        print("  python deploy.py test      - Run tests")
        print("  python deploy.py install   - Install dependencies")
        print("  python deploy.py dev       - Start local development server")
        print("  python deploy.py deploy    - Deploy to Vercel")
        print("  python deploy.py full      - Full deployment (check + test + deploy)")
        return
    
    command = sys.argv[1].lower()
    
    if command == "check":
        check_requirements()
    
    elif command == "test":
        if check_requirements():
            run_tests()
    
    elif command == "install":
        install_dependencies()
    
    elif command == "dev":
        if check_requirements():
            install_dependencies()
            start_local_server()
    
    elif command == "deploy":
        if check_requirements():
            deploy_to_vercel()
    
    elif command == "full":
        if check_requirements():
            if install_dependencies():
                if run_tests():
                    deploy_to_vercel()
                else:
                    print("❌ Tests failed. Deployment cancelled.")
            else:
                print("❌ Dependency installation failed.")
    
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()