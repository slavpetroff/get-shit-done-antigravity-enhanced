#!/usr/bin/env python3
import os
import re
import xml.etree.ElementTree as ET
from urllib.parse import quote

# Configuration
SKILLS_DIR = ".agent/skills"
OUTPUT_FILE = ".gsd/SKILLS.md"

# Categorization Keywords (Heuristics)
CATEGORIES = {
    "Core/Workflow": ["plan", "execute", "verify", "debug", "checklist", "kaizen", "task", "memory", "context", "roadmap", "gsd"],
    "Frontend": ["react", "css", "tailwind", "ui", "ux", "frontend", "design", "component", "animation", "three.js", "webgl", "canvas", "visual"],
    "Backend": ["api", "database", "sql", "node", "python", "fastapi", "django", "server", "backend", "docker", "aws", "cloud", "deployment", "firebase", "supabase", "auth"],
    "Security": ["security", "pentest", "vulnerability", "hack", "exploit", "audit", "auth", "xss", "injection", "scanner"],
    "AI/Agents": ["ai", "agent", "llm", "prompt", "rag", "mcp", "tool", "braistorm", "research", "bot"],
    "Product/Business": ["marketing", "seo", "copywriting", "product", "growth", "analytics", "email", "launch", "business", "saas"],
}

def get_skill_metadata(skill_path):
    """
    Extracts name, description, and confidence from SKILL.md.
    """
    try:
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Basic YAML frontmatter extraction (simple regex for robustness without pyyaml)
        name_match = re.search(r"name:\s*(.+)", content)
        desc_match = re.search(r"description:\s*(.+)", content)
        
        name = name_match.group(1).strip() if name_match else os.path.basename(os.path.dirname(skill_path))
        description = desc_match.group(1).strip() if desc_match else "No description provided."
        
        return {
            "name": name,
            "description": description,
            "path": os.path.abspath(skill_path),
            "content": content
        }
    except Exception as e:
        print(f"Error reading {skill_path}: {e}")
        return None

def determine_category(metadata):
    """
    Assigns a category based on keywords in name and description.
    """
    text = (metadata["name"] + " " + metadata["description"]).lower()
    
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in text:
                return category
    
    return "Uncategorized"

def generate_registry_xml(skills):
    """
    Generates the <gsd_registry> XML block.
    """
    root = ET.Element("gsd_registry")
    
    for skill in skills:
        item = ET.SubElement(root, "item", id=skill["name"], confidence="1.0")
        
        name = ET.SubElement(item, "name")
        name.text = skill["name"]
        
        desc = ET.SubElement(item, "description")
        desc.text = skill["description"]
        
        path = ET.SubElement(item, "path")
        path.text = skill["path"]
        
    # Convert to string (python 3.8+ handles unicode well)
    xml_str = ET.tostring(root, encoding="unicode")
    return xml_str

def main():
    print(" scanning skills...")
    
    discovered_skills = []
    
    # Walk through .agent/skills
    for root, dirs, files in os.walk(SKILLS_DIR):
        if "SKILL.md" in files:
            skill_path = os.path.join(root, "SKILL.md")
            meta = get_skill_metadata(skill_path)
            if meta:
                meta["category"] = determine_category(meta)
                discovered_skills.append(meta)

    # Sort skills by name
    discovered_skills.sort(key=lambda x: x["name"])
    
    # Group by category
    skills_by_category = {cat: [] for cat in CATEGORIES.keys()}
    skills_by_category["Uncategorized"] = []
    
    for skill in discovered_skills:
        skills_by_category[skill["category"]].append(skill)
        
    # Generate Output
    output_lines = [
        "# SKILLS.md — Local Agent Intelligence",
        "",
        "> **Status**: `OPTIMIZED`",
        "> **Discovery Mode**: `AUTO`",
        "",
        "This registry contains specialized skills discovered in `.agent/skills/`. Each skill provides domain-specific knowledge.",
        "",
        "---",
        ""
    ]
    
    # Human Readable Index
    output_lines.append("## Skill Index\n")
    
    for category, skills in skills_by_category.items():
        if not skills:
            continue
            
        output_lines.append(f"### {category}")
        for skill in skills:
            # Use file:// link for clickable absolute path support in most editors
            link = f"file://{skill['path']}"
            output_lines.append(f"- [{skill['name']}]({link}) - {skill['description']}")
        output_lines.append("")

    # Machine Registry
    output_lines.append("---")
    output_lines.append("\n## Registry\n")
    output_lines.append(generate_registry_xml(discovered_skills))
    
    # Write File
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
        
    print(f"Successfully generated {OUTPUT_FILE} with {len(discovered_skills)} skills.")

if __name__ == "__main__":
    main()
