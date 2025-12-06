#!/usr/bin/env python3
"""
Minimal example: Extract roadmap data from roadmap.sh

This is the simplest possible implementation to get started.
Run: python quick_example.py
"""

import requests
import json

def main():
    # Step 1: Get a roadmap's JSON data
    roadmap_name = "backend"
    url = f"https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master/src/data/roadmaps/{roadmap_name}/{roadmap_name}.json"
    
    print(f"Fetching {roadmap_name} roadmap...")
    response = requests.get(url)
    data = response.json()
    
    # Step 2: Extract topics
    topics = [
        node['data']['label'] 
        for node in data['nodes'] 
        if node.get('type') == 'topic'
    ]
    
    # Step 3: Show results
    print(f"\nFound {len(topics)} topics in {roadmap_name} roadmap:")
    for i, topic in enumerate(topics, 1):
        print(f"  {i}. {topic}")
    
    # Step 4: Save to file
    output = {
        "roadmap": roadmap_name,
        "topic_count": len(topics),
        "topics": topics,
        "edges_count": len(data.get('edges', []))
    }
    
    with open(f"{roadmap_name}_simple.json", 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Saved to {roadmap_name}_simple.json")

if __name__ == "__main__":
    main()
