#!/usr/bin/env python3
"""
Release script for simplejsonspider
"""
import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a shell command and return the result"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result.stdout.strip()

def main():
    """Main release process"""
    # Get the current directory
    repo_dir = Path(__file__).parent
    
    # Clean previous builds
    print("Cleaning previous builds...")
    for path in ["build", "dist", "*.egg-info"]:
        full_path = repo_dir / path
        if full_path.exists():
            run_command(f"rmdir /s /q {full_path}" if os.name == 'nt' else f"rm -rf {full_path}", cwd=repo_dir)
    
    # Install build dependencies
    print("Installing build dependencies...")
    run_command("pip install -U build setuptools setuptools_scm wheel twine")
    
    # Run tests
    print("Running tests...")
    run_command("python -m pytest tests/ -v", cwd=repo_dir)
    
    # Build the package
    print("Building package...")
    run_command("python -m build", cwd=repo_dir)
    
    # Test the built package
    print("Testing built package...")
    import glob
    whl_files = glob.glob(str(repo_dir / "dist" / "*.whl"))
    if whl_files:
        run_command(f"pip install \"{whl_files[0]}\" --force-reinstall", cwd=repo_dir)
        run_command("python -c \"import simplejsonspider; print(f'Package version: {simplejsonspider.__version__}')\"")
    else:
        print("No wheel file found!")
    # Get version from git
    try:
        version = run_command("git describe --tags --abbrev=0")
        if not version:
            version = "v0.3.0"
    except:
        version = "v0.3.0"
    
    print(f"Package built successfully! Version: {version}")
    print(f"Files created:")
    dist_dir = repo_dir / "dist"
    for file in dist_dir.glob("*"):
        print(f"  - {file}")
    
    print("\nTo create a release:")
    print("1. Commit your changes:")
    print("   git add .")
    print("   git commit -m 'Prepare release'")
    print("   git push")
    print("")
    print("2. Create and push a tag:")
    print(f"   git tag {version}")
    print(f"   git push origin {version}")
    print("")
    print("3. The GitHub Actions will automatically:")
    print("   - Run tests")
    print("   - Build the package")
    print("   - Create a GitHub release")
    print("   - Upload to PyPI (if PYPI_TOKEN is set)")

if __name__ == "__main__":
    main()
