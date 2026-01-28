#!/usr/bin/env python3
import os
import re
import json
import datetime
import sys
import xml.etree.ElementTree as ET

# --- Configuration ---
SKILLS_DIR = ".agent/skills"
SKILLS_INVENTORY = ".gsd/SKILLS.md"
MCPS_INVENTORY = ".gsd/MCPS.md"

# Standard macOS paths for MCP configs
PATHS = {
    "claude": [
        os.path.expanduser("~/Library/Application Support/Claude/claude_desktop_config.json"),
        os.path.expanduser("~/Library/Application Support/Claude Desktop/claude_desktop_config.json")
    ],
    "cursor": [
        os.path.expanduser("~/Library/Application Support/Cursor/User/globalStorage/cursor-mcp/mcp-servers.json"),
        os.path.expanduser("~/.cursor/mcp-servers.json") # Alternate/future
    ],
    "gemini": [
        os.path.expanduser("~/.gemini/config.json") # Custom projection
    ]
}

def scan_skills():
    skills = []
    if not os.path.exists(SKILLS_DIR):
        print(f"Warning: {SKILLS_DIR} not found.")
        return skills
    
    for skill_name in sorted(os.listdir(SKILLS_DIR)):
        skill_dir = os.path.join(SKILLS_DIR, skill_name)
        if not os.path.isdir(skill_dir):
            continue
            
        skill_path = os.path.join(skill_dir, "SKILL.md")
        if os.path.exists(skill_path):
            with open(skill_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Metadata extraction
            meta_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
            name = skill_name
            description = ""
            if meta_match:
                meta = meta_match.group(1)
                name_line = re.search(r'^name:\s*(.*)', meta, re.MULTILINE)
                desc_line = re.search(r'^description:\s*(.*)', meta, re.MULTILINE)
                if name_line: name = name_line.group(1).strip()
                if desc_line: description = desc_line.group(1).strip()
            
            # Extraction logic (Full extraction as requested)
            usage = ""
            constraints = ""
            
            # Extract sections
            sections = re.split(r'\n##\s+', content)
            for section in sections:
                if section.lower().startswith("purpose"):
                    usage += "### Purpose\n" + section[len("purpose"):].strip() + "\n\n"
                elif "activate" in section.lower() or "when to use" in section.lower():
                    title = "Activation" if "activate" in section.lower() else "When to Use"
                    # Find first line and content
                    lines = section.split('\n')
                    usage += f"### {title}\n" + "\n".join(lines[1:]).strip() + "\n\n"
                elif "behavior rules" in section.lower() or "constraints" in section.lower():
                    lines = section.split('\n')
                    constraints += "\n".join(lines[1:]).strip() + "\n\n"

            # Fallback description
            if not description and usage:
                first_para = re.search(r'^(.*?)\n\n', usage, re.DOTALL)
                description = first_para.group(1).strip()[:150] if first_para else usage[:150]

            # Confidence scoring
            score = 0.0
            has_meta = bool(meta_match)
            has_details = len(usage) > 50 or len(constraints) > 50
            if has_meta and has_details:
                score = 1.0
            elif has_meta or has_details:
                score = 0.5
            
            skills.append({
                "id": skill_name,
                "name": name,
                "path": skill_path,
                "description": description or "No description provided.",
                "usage": usage.strip(),
                "constraints": constraints.strip(),
                "confidence": score
            })
        else:
            # Directory exists but no SKILL.md
            skills.append({
                "id": skill_name,
                "name": skill_name,
                "path": skill_dir,
                "description": "[MISSING SKILL.MD]",
                "usage": "",
                "constraints": "",
                "confidence": 0.0
            })
            
    return skills

def scan_mcps():
    mcp_servers = []
    
    # Scan known paths
    for source, paths in PATHS.items():
        for path in paths:
            if os.path.exists(path):
                print(f"Found {source} config at {path}")
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                    # Handle Claude/Cursor formats (they differ slightly)
                    # Claude: {"mcpServers": {"name": {"command": ...}}}
                    # Cursor: {"mcpServers": {"name": {"type": ...}}}
                    servers = data.get("mcpServers", {}) or data.get("servers", {})
                    if not servers and isinstance(data, dict):
                        # Some formats just have the server map
                        servers = data
                        
                    for s_name, s_conf in servers.items():
                        if not isinstance(s_conf, dict): continue
                        
                        mcp_servers.append({
                            "id": f"{source}:{s_name}",
                            "name": s_name,
                            "source": source.capitalize(),
                            "path": path,
                            "description": f"MCP Server ({source}): {s_name}",
                            "confidence": 1.0
                        })
                except Exception as e:
                    print(f"Error parsing {path}: {e}")
    
    return mcp_servers

def update_inventory(path, category, items):
    if not os.path.exists(path):
        print(f"Error: Inventory file {path} not found.")
        return
        
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Generate human section
    human_blocks = []
    for item in items:
        block = f"## {item['name']}\n"
        block += f"- **ID**: `{item['id']}`\n"
        block += f"- **Confidence**: `{item['confidence']}`\n"
        if item.get('source'):
            block += f"- **Source**: {item['source']} ({item['path']})\n"
        
        block += f"\n### Description\n{item['description']}\n"
        
        if item.get('usage'):
            block += f"\n{item['usage']}\n"
            
        if item.get('constraints'):
            block += f"\n### Behavior & Constraints\n{item['constraints']}\n"
            
        block += "\n---\n"
        human_blocks.append(block)
    
    human_content = "\n".join(human_blocks)
    if not items:
        human_content = "## [NO ITEMS DISCOVERED]\n_Run discovery again or check configuration paths._\n"
    
    # 2. Generate XML block
    root = ET.Element("gsd_registry", type=category)
    root.append(ET.Comment(" MACHINE-READABLE REGISTRY "))
    for item in items:
        item_el = ET.SubElement(root, "item", id=item["id"], confidence=str(item["confidence"]))
        ET.SubElement(item_el, "name").text = item["name"]
        ET.SubElement(item_el, "path").text = item["path"]
        ET.SubElement(item_el, "description").text = item["description"]
    
    # Pretty print XML
    xml_registry = ET.tostring(root, encoding='utf-8').decode('utf-8')
    # Simple indent for readability
    xml_registry = xml_registry.replace('<item', '\n    <item').replace('</item>', '\n    </item>').replace('</gsd_registry>', '\n</gsd_registry>').replace('<name', '\n        <name').replace('<path', '\n        <path').replace('<description', '\n        <description')
    
    # 3. Perform Reflective Swap
    # Replace content between first --- and <gsd_registry> tag
    # or just replace everything after the header.
    
    # Locate the registry tag
    tag_match = re.search(r'<gsd_registry.*?>.*?</gsd_registry>', content, re.DOTALL)
    if not tag_match:
        print(f"Error: Registry tag not found in {path}")
        return
    
    # Locate the "header" - everything before the first "---" (excluding frontmatter)
    header_parts = re.split(r'\n---\n', content)
    if len(header_parts) > 1:
        header = header_parts[0].strip()
    else:
        header = content.split('##')[0].strip()
    
    new_content = f"""{header}

---

## Technical Details
This file is both a human-readable inventory and a machine-readable registry. GSD uses the `<gsd_registry>` block below for automated tool selection and prompt injection.

---

{human_content}

{xml_registry}
"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {path} with {len(items)} items.")

def hydrate_personas(skills):
    """Injects discovered skills into persona files."""
    PERSONAS_DIR = ".agent/personas"
    if not os.path.exists(PERSONAS_DIR):
        return

    # Prepare skill summary for hydration
    skill_summary = "\n".join([f"- **{s['name']}**: {s['description']}" for s in skills if s['confidence'] >= 0.5])
    if not skill_summary:
        skill_summary = "_No specialized skills discovered._"

    for persona_file in os.listdir(PERSONAS_DIR):
        if not persona_file.endswith(".md"): continue
        path = os.path.join(PERSONAS_DIR, persona_file)
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        if "<!-- SKILLS_START -->" in content and "<!-- SKILLS_END -->" in content:
            new_content = re.sub(
                r"<!-- SKILLS_START -->.*?<!-- SKILLS_END -->",
                f"<!-- SKILLS_START -->\n{skill_summary}\n<!-- SKILLS_END -->",
                content,
                flags=re.DOTALL
            )
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Hydrated persona: {persona_file}")

def main():
    print(f"GSD Discovery Engine v1.1.0 | {datetime.datetime.now().isoformat()}")
    print("-" * 50)
    
    skills = scan_skills()
    mcps = scan_mcps()
    
    update_inventory(SKILLS_INVENTORY, "skills", skills)
    update_inventory(MCPS_INVENTORY, "mcp_servers", mcps)
    
    # Hydration Wave
    print("Initiating Hydration Wave...")
    hydrate_personas(skills)
    
    print("-" * 50)
    print("Sync complete.")

if __name__ == "__main__":
    main()
