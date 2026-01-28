import json
import os
import sys

try:
    import tomllib
except ImportError:
    try:
        import toml as tomllib
    except ImportError:
        print("Warning: neither 'tomllib' nor 'toml' installed. pyproject.toml scanning will fail.", file=sys.stderr)
        tomllib = None

# High Value Interest List
# We only want to fetch intelligence for major frameworks, not every utility lib.
INTEREST_LIST = {
    "frontend": [
        "react", "next", "vue", "nuxt", "svelte", "tailwindcss", 
        "framer-motion", "redux", "zustand", "tanstack", "bootstrap", "material-ui"
    ],
    "backend": [
        "fastapi", "flask", "django", "express", "nestjs", "socket.io",
        "sqlalchemy", "prisma", "mongoose", "typeorm", "redis", "celery", "bullmq"
    ],
    "ai": [
        "langchain", "openai", "anthropic", "transformers", "pytorch", 
        "tensorflow", "huggingface", "pinecone", "chromadb", "crewai"
    ],
    "testing": [
        "jest", "vitest", "pytest", "cypress", "playwright", "selenium"
    ],
    "devops": [
        "docker", "kubernetes", "terraform", "aws-cdk", "pulumi"
    ]
}

def scan_package_json():
    """Scans package.json for dependencies."""
    found = set()
    if os.path.exists("package.json"):
        try:
            with open("package.json", "r") as f:
                data = json.load(f)
                deps = data.get("dependencies", {})
                dev_deps = data.get("devDependencies", {})
                all_deps = {**deps, **dev_deps}
                found.update(all_deps.keys())
        except Exception as e:
            print(f"Error parsing package.json: {e}", file=sys.stderr)
    return found

def scan_pyproject_toml():
    """Scans pyproject.toml for dependencies (Poetry/PDM/Standard)."""
    found = set()
    if os.path.exists("pyproject.toml") and tomllib:
        try:
            with open("pyproject.toml", "rb") as f:
                data = tomllib.load(f)
            # Poetry
            if "tool" in data and "poetry" in data["tool"]:
                deps = data["tool"]["poetry"].get("dependencies", {})
                dev_deps = data["tool"]["poetry"].get("dev-dependencies", {})
                found.update(deps.keys())
                found.update(dev_deps.keys())
            # Standard project.dependencies
            if "project" in data:
                found.update(data["project"].get("dependencies", []))
        except Exception as e:
            print(f"Error parsing pyproject.toml: {e}", file=sys.stderr)
    return found

def identify_libraries():
    """Identifies and categorizes high-value libraries from found dependencies."""
    npm_deps = scan_package_json()
    pypi_deps = scan_pyproject_toml()
    
    # Normalize PyPI specific names (e.g. 'fastapi' is same, but 'python-dotenv' -> 'dotenv')
    # For now, strict matching against interest list is enough for MVP.
    
    all_found_deps = npm_deps.union(pypi_deps)
    
    results = []
    
    for category, keywords in INTEREST_LIST.items():
        for lib in keywords:
            # Check for exact match or typical variations
            # e.g. 'next' matches 'next' package
            # 'react' matches 'react'
            
            # Simple substring check is risky (e.g. 'os' matches 'postcss'), so we do:
            # 1. Exact match
            # 2. "starts with lib-" or "ends with -lib"? No, keep it simple for now.
            
            if lib in all_found_deps:
                results.append({"name": lib, "category": category})
            else:
                # Handle scoped packages or variations if critical
                # e.g. @nestjs/core -> nestjs
                pass

    return results

if __name__ == "__main__":
    libs = identify_libraries()
    print(json.dumps(libs, indent=2))
