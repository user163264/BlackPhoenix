import subprocess
import os
import sys

def setup_environment():
    project_dir = "/Users/admin/Documents/redteam-tools"
    venv_dir = os.path.join(project_dir, "venv")
    
    # Check if venv exists
    if not os.path.exists(venv_dir):
        print("VENV directory not found. Please ensure it exists at:", venv_dir)
        return
    
    # Determine pip path
    pip_path = os.path.join(venv_dir, "bin", "pip")
    
    # Install requirements
    print("Installing dependencies to existing VENV...")
    requirements = [
        "flask",
        "openai",
        "requests",
        "python-dotenv",
        "flask-wtf",
        "nltk",
        "langdetect",
        "transformers",
        "tiktoken"
    ]
    
    subprocess.check_call([pip_path, "install"] + requirements)
    
    # Create requirements.txt
    with open(os.path.join(project_dir, "requirements.txt"), "w") as f:
        f.write("\n".join(requirements))
    
    print("Dependencies installed successfully!")

if __name__ == "__main__":
    setup_environment()