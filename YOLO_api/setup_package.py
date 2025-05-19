"""
This module initializes the package structure.
"""

# Create empty __init__.py files to make directories into Python packages

import os
import pathlib

# List of directories to initialize as packages
package_dirs = [
    "app",
    "app/api",
    "app/api/routes",
    "app/models",
    "app/utils"
]

# Create __init__.py files
for directory in package_dirs:
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
    init_file = os.path.join(directory, "__init__.py")
    
    # Only create if it doesn't exist
    if not os.path.exists(init_file):
        with open(init_file, "w") as f:
            if directory == "app/api/routes":
                # For routes, add code to include the router
                f.write("""
from fastapi import APIRouter

# Import all routes
from app.api.routes.config import router as config_router

# Create main router
api_router = APIRouter()

# Include all route modules
api_router.include_router(config_router)
""")
            else:
                # Empty __init__.py for other directories
                f.write('"""Package initialization."""\n')

# Update main.py to include routers
main_file = os.path.join("app/api/main.py")
if os.path.exists(main_file):
    with open(main_file, "r") as f:
        content = f.read()
    
    # Check if router import is missing
    if "from app.api.routes import api_router" not in content:
        # Add import and router inclusion
        import_line = "from app.api.routes import api_router\n"
        app_line = "app.include_router(api_router)\n"
        
        # Find where to insert
        lines = content.split("\n")
        import_added = False
        app_added = False
        
        for i, line in enumerate(lines):
            if "from fastapi import" in line and not import_added:
                lines.insert(i + 1, import_line)
                import_added = True
            
            if "add_middleware" in line and not app_added:
                # Find the end of the middleware block
                for j in range(i + 1, len(lines)):
                    if ")" in lines[j]:
                        lines.insert(j + 2, app_line)
                        app_added = True
                        break
        
        # Write the updated content
        with open(main_file, "w") as f:
            f.write("\n".join(lines))

print("Package structure initialized successfully.")