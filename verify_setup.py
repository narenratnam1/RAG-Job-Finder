#!/usr/bin/env python3
"""
Comprehensive setup verification script
"""

import sys
import os

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} (need 3.8+)")
        return False

def check_venv():
    """Check if running in virtual environment"""
    print("\n📦 Checking virtual environment...")
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("   ✅ Virtual environment active")
        return True
    else:
        print("   ⚠️  Not in virtual environment (recommended to activate venv)")
        return True  # Non-critical

def check_imports():
    """Check all required imports"""
    print("\n📚 Checking dependencies...")
    
    checks = [
        ("FastAPI", "fastapi"),
        ("Uvicorn", "uvicorn"),
        ("MCP", "mcp.server.fastmcp"),
        ("ChromaDB", "chromadb"),
        ("LangChain", "langchain"),
        ("LangChain Community", "langchain_community"),
        ("LangChain HuggingFace", "langchain_huggingface"),
        ("LangChain Text Splitters", "langchain_text_splitters"),
        ("PyPDF", "pypdf"),
        ("Sentence Transformers", "sentence_transformers"),
        ("Python Multipart", "python_multipart"),
    ]
    
    all_passed = True
    for name, module in checks:
        try:
            __import__(module)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name} - Missing!")
            all_passed = False
    
    return all_passed

def check_app_structure():
    """Check application file structure"""
    print("\n📁 Checking project structure...")
    
    required_files = [
        "app/__init__.py",
        "app/main.py",
        "app/services/__init__.py",
        "app/services/vector_store.py",
        "app/services/ingestor.py",
        "requirements.txt",
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - Missing!")
            all_exist = False
    
    return all_exist

def check_app_imports():
    """Check if app modules can be imported"""
    print("\n🔍 Checking app modules...")
    
    try:
        from app.services.vector_store import VectorService
        print("   ✅ VectorService")
    except Exception as e:
        print(f"   ❌ VectorService - {e}")
        return False
    
    try:
        from app.services.ingestor import process_pdf
        print("   ✅ process_pdf")
    except Exception as e:
        print(f"   ❌ process_pdf - {e}")
        return False
    
    return True

def main():
    """Run all checks"""
    print("=" * 60)
    print("🔧 Agentic RAG API - Setup Verification")
    print("=" * 60)
    
    results = []
    
    # Run all checks
    results.append(("Python Version", check_python_version()))
    results.append(("Virtual Environment", check_venv()))
    results.append(("Dependencies", check_imports()))
    results.append(("Project Structure", check_app_structure()))
    results.append(("App Modules", check_app_imports()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:12} {name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All checks passed! You're ready to run the application!")
        print("\n💡 To start the server, run:")
        print("   python app/main.py")
        print("   or")
        print("   ./run.sh")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\n💡 To install dependencies:")
        print("   pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
