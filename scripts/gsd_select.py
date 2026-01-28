#!/usr/bin/env python3
import os
import re
import json
import sys
import xml.etree.ElementTree as ET

# --- Configuration ---
SKILLS_INVENTORY = ".gsd/SKILLS.md"
MCPS_INVENTORY = ".gsd/MCPS.md"

def extract_registry(path):
    if not os.path.exists(path):
        return []
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Locate the registry tag - ensure it's the block and not a text mention
    tag_match = re.search(r'\n(<gsd_registry.*?>.*?</gsd_registry>)', content, re.DOTALL)
    if not tag_match:
        # Fallback to start of string or search without leading newline if it's the only content
        tag_match = re.search(r'(<gsd_registry.*?>.*?</gsd_registry>)', content, re.DOTALL)
    
    if not tag_match:
        return []
    
    registry_xml = tag_match.group(1).strip()
    
    try:
        root = ET.fromstring(registry_xml)
        items = []
        for item in root.findall('item'):
            items.append({
                "id": item.get('id'),
                "confidence": float(item.get('confidence', 0)),
                "name": item.find('name').text if item.find('name') is not None else "",
                "path": item.find('path').text if item.find('path') is not None else "",
                "description": item.find('description').text if item.find('description') is not None else ""
            })
        return items
    except Exception as e:
        print(f"Error parsing registry in {path}: {e}")
        return []

def get_full_extraction(item_id, inventory_path):
    """Extracts the full human-readable section for a specific item from the MD file."""
    if not os.path.exists(inventory_path):
        return ""
        
    with open(inventory_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Split by separators
    sections = re.split(r'\n---', content)
    for section in sections:
        section = section.strip()
        if f"- **ID**: `{item_id}`" in section:
            # Only return from the first header onwards to avoid header/meta leaks
            if "## " in section:
                skill_part = "## " + section.split("## ", 1)[1]
                return skill_part
            return section
    
    return ""

def score_item(item, context):
    context = context.lower()
    score = 0
    
    # Weights
    W_NAME = 10
    W_DESC = 5
    W_ID = 3
    
    # Exact name match
    if item['name'].lower() in context:
        score += W_NAME
        
    # Description keywords
    desc_words = re.findall(r'\w+', item['description'].lower())
    for word in desc_words:
        if len(word) > 3 and word in context:
            score += W_DESC / len(desc_words)
            
    # ID match
    if item['id'].lower() in context:
        score += W_ID
        
    # Heuristic: if context contains "debug" and id contains "debug"
    if "debug" in context and "debug" in item['id'].lower():
        score += 5

    if "map" in context and "mapper" in item['id'].lower():
        score += 5
        
    return score

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No context provided", "usage": "gsd_select.py <context>"}, indent=2))
        sys.exit(1)
        
    context = " ".join(sys.argv[1:])
    
    # 1. Load Registry
    skills = extract_registry(SKILLS_INVENTORY)
    mcps = extract_registry(MCPS_INVENTORY)
    
    all_items = skills + mcps
    
    # 2. Score Items
    scored_items = []
    for item in all_items:
        score = score_item(item, context)
        if score > 0:
            scored_items.append((score, item))
            
    # 3. Sort and Filter
    scored_items.sort(key=lambda x: x[0], reverse=True)
    top_items = scored_items[:3]
    
    # 4. Prepare Output
    results = []
    prompt_fragment = []
    
    for score, item in top_items:
        # Get full extraction for prompt injection
        inventory_path = SKILLS_INVENTORY if item in skills else MCPS_INVENTORY
        full_text = get_full_extraction(item['id'], inventory_path)
        
        results.append({
            "id": item['id'],
            "name": item['name'],
            "score": round(score, 2),
            "confidence": item['confidence']
        })
        
        if full_text:
            prompt_fragment.append(full_text)
            
    output = {
        "results": results,
        "prompt_injection": "\n\n".join(prompt_fragment) if prompt_fragment else "No relevant skills found."
    }
    
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
