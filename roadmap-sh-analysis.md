# Analysis of roadmap.sh for Role-Based Roadmap Extraction

## Overview

**Repository**: https://github.com/kamranahmedse/developer-roadmap  
**Website**: https://roadmap.sh  
**Tech Stack**: Astro (TypeScript-based static site generator)  
**Total Roadmaps**: 71+ role-based roadmaps

## Data Structure

### 1. File Organization

Each roadmap is stored in: `/src/data/roadmaps/{roadmap-name}/`

Example structure for `backend` roadmap:
```
src/data/roadmaps/backend/
├── backend.md              # Metadata (frontmatter + SEO)
├── backend.json            # Visual roadmap data (nodes/edges)
├── backend-beginner.json   # Beginner variant (if available)
├── content/                # Individual topic descriptions
│   ├── topic-1@{id}.md
│   ├── topic-2@{id}.md
│   └── ...
├── faqs.astro             # FAQ component
└── migration-mapping.json  # Migration data
```

### 2. Metadata File (.md)

**File**: `{roadmap-name}.md`

Contains YAML frontmatter with:
- `title`: Roadmap title
- `description`: Full description
- `briefTitle`: Short title
- `briefDescription`: Short description
- `hasTopics`: Boolean indicating if roadmap has topics
- `jsonUrl`: Path to JSON (e.g., `/jsons/roadmaps/backend.json`)
- `pdfUrl`: Path to PDF version
- `order`: Display order
- `dimensions`: Width/height for rendering
- `seo`: SEO metadata (keywords, descriptions)
- `schema`: Schema.org metadata
- `courses`: Related courses (optional)
- `partner`: Partner information (optional)

**Example**:
```yaml
---
renderer: 'editor'
jsonUrl: '/jsons/roadmaps/backend.json'
pdfUrl: '/pdfs/roadmaps/backend.pdf'
order: 2
briefTitle: 'Backend'
briefDescription: 'Step by step guide to becoming a backend developer in 2025'
title: 'Backend Developer'
description: 'Step by step guide to becoming a modern backend developer in 2025'
hasTopics: true
---
```

### 3. Roadmap Data (.json)

**File**: `{roadmap-name}.json`

JSON structure with two main arrays:

```json
{
  "nodes": [
    {
      "id": "unique-node-id",
      "type": "topic" | "section" | "button",
      "position": { "x": 100, "y": 200 },
      "data": {
        "label": "Topic Name",
        "style": { "width": 150, "height": 100, ... }
      },
      "width": 150,
      "height": 100
    }
  ],
  "edges": [
    {
      "id": "edge-id",
      "source": "source-node-id",
      "target": "target-node-id"
    }
  ]
}
```

**Node Types**:
- `topic`: Clickable topics with content
- `section`: Visual grouping boxes
- `button`: Navigation buttons

### 4. Topic Content

**Location**: `content/{topic-name}@{unique-id}.md`

Markdown files with:
- Topic description
- Learning resources (links, videos, articles)
- Resource links prefixed with type: `@article@`, `@video@`, `@feed@`, `@official@`

**Example**:
```markdown
# Basic authentication

Basic Authentication sends base64-encoded username:password in HTTP headers...

Visit the following resources to learn more:

- [@article@HTTP Basic Authentication](https://roadmap.sh/guides/http-basic-authentication)
- [@video@Basic Authentication in 5 minutes](https://www.youtube.com/watch?v=rhi1eIjSbvk)
- [@feed@Explore top posts about Authentication](https://app.daily.dev/tags/authentication)
```

## Available Roadmaps (Sample)

```
ai-agents              frontend               nodejs
ai-data-scientist      full-stack             php
ai-engineer            game-developer         postgresql-dba
android                git-github             product-manager
angular                golang                 python
api-design             graphql                qa
aspnet-core            html                   react
aws                    ios                    react-native
backend                java                   rust
blockchain             javascript             security
cpp                    kubernetes             software-architect
css                    laravel                spring-boot
cyber-security         linux                  sql
data-analyst           machine-learning       system-design
data-engineer          mlops                  terraform
datastructures-and-algorithms  mongodb        typescript
design-system          nextjs                 ux-design
devops                 ...and more (71 total)
```

## Extraction Methods (Easiest to Hardest)

### Method 1: Direct GitHub Raw Files (EASIEST ⭐)

**Best for**: Simple, quick extraction without dependencies

**Approach**:
1. List all roadmaps: `https://api.github.com/repos/kamranahmedse/developer-roadmap/contents/src/data/roadmaps`
2. For each roadmap, fetch:
   - Metadata: `https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master/src/data/roadmaps/{name}/{name}.md`
   - JSON data: `https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master/src/data/roadmaps/{name}/{name}.json`
   - Content files: `https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master/src/data/roadmaps/{name}/content/*.md`

**Pros**:
- No API keys needed
- No rate limiting (for reasonable use)
- Direct access to latest data
- Simple HTTP GET requests
- Works with any programming language

**Cons**:
- Requires multiple requests per roadmap
- No built-in filtering or querying
- Need to parse YAML frontmatter and JSON yourself

**Example Python Code**:
```python
import requests
import yaml
import json

def get_roadmap_list():
    url = "https://api.github.com/repos/kamranahmedse/developer-roadmap/contents/src/data/roadmaps"
    response = requests.get(url)
    return [item['name'] for item in response.json() if item['type'] == 'dir']

def get_roadmap_metadata(roadmap_name):
    url = f"https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master/src/data/roadmaps/{roadmap_name}/{roadmap_name}.md"
    response = requests.get(url)
    # Parse YAML frontmatter
    content = response.text
    if content.startswith('---'):
        parts = content.split('---', 2)
        metadata = yaml.safe_load(parts[1])
        return metadata
    return None

def get_roadmap_data(roadmap_name):
    url = f"https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master/src/data/roadmaps/{roadmap_name}/{roadmap_name}.json"
    response = requests.get(url)
    return response.json()

# Usage
roadmaps = get_roadmap_list()
for roadmap in roadmaps:
    metadata = get_roadmap_metadata(roadmap)
    data = get_roadmap_data(roadmap)
    print(f"{roadmap}: {metadata.get('title')} - {len(data.get('nodes', []))} nodes")
```

### Method 2: Clone Repository Locally

**Best for**: Offline access, bulk processing, custom analysis

**Approach**:
```bash
# Clone the repository
git clone https://github.com/kamranahmedse/developer-roadmap.git
cd developer-roadmap

# Navigate to roadmaps
cd src/data/roadmaps

# List all roadmaps
ls -d */

# Process each roadmap
for dir in */; do
    name=${dir%/}
    echo "Processing: $name"
    # Read metadata
    cat "$name/$name.md"
    # Read JSON data
    cat "$name/$name.json"
    # Read content files
    ls "$name/content/"
done
```

**Pros**:
- Full offline access
- Fast bulk operations
- Can track changes with git
- No network dependencies after cloning
- Easy to integrate with build tools

**Cons**:
- Requires disk space (~360MB)
- Need to pull updates manually
- Requires git installed

### Method 3: GitHub API with GraphQL

**Best for**: Advanced filtering, specific data queries

**Approach**: Use GitHub GraphQL API to query specific files

**Pros**:
- Efficient for targeted queries
- Can fetch multiple files in one request
- Better for production applications

**Cons**:
- Requires GitHub token for higher rate limits
- More complex to implement
- Need to learn GraphQL syntax

### Method 4: Web Scraping the Website

**Best for**: NOT RECOMMENDED

**Why avoid**:
- No public API endpoints on roadmap.sh
- Data is rendered client-side
- More complex than direct GitHub access
- Risk of rate limiting
- Against best practices

## Recommended Approach

### For Quick Analysis/Prototyping:
**Use Method 1 (Direct GitHub Raw Files)**
- Simple HTTP requests
- No authentication needed
- Direct access to structured data
- Easy to implement in any language

### For Production Application:
**Use Method 2 (Clone Repository)**
- Set up automated git pulls (hourly/daily)
- Process files locally
- Store processed data in your database
- Fast and reliable

## Data Processing Pipeline

### Step 1: Fetch Roadmap List
```
GET https://api.github.com/repos/kamranahmedse/developer-roadmap/contents/src/data/roadmaps
→ Returns array of roadmap directories
```

### Step 2: For Each Roadmap, Extract:

1. **Metadata** from `{name}.md`:
   - Title, description
   - Categories, tags
   - Order, dimensions
   
2. **Visual Structure** from `{name}.json`:
   - Topics (nodes with type="topic")
   - Relationships (edges)
   - Layout positions

3. **Content** from `content/*.md`:
   - Topic descriptions
   - Learning resources
   - External links

### Step 3: Transform Data

Extract useful information:

**From metadata**:
```json
{
  "id": "backend",
  "title": "Backend Developer",
  "description": "Step by step guide...",
  "category": "role-based",
  "topics_count": 21,
  "last_updated": "2023-09-16"
}
```

**From nodes**:
```json
{
  "topics": [
    {
      "id": "SiYUdtYMDImRPmV2_XPkH",
      "name": "Internet",
      "content_file": "internet@SiYUdtYMDImRPmV2_XPkH.md",
      "position": { "x": 100, "y": 200 }
    }
  ]
}
```

**From edges**:
```json
{
  "relationships": [
    {
      "from": "Internet",
      "to": "Pick a Language",
      "type": "prerequisite"
    }
  ]
}
```

## Key Insights

1. **Consistent Structure**: All 71 roadmaps follow the same format
2. **No Public API**: Website doesn't expose a public API
3. **GitHub is Source of Truth**: All data lives in the repository
4. **Simple Parsing**: Files use standard formats (JSON, Markdown, YAML)
5. **Regular Updates**: Repository is actively maintained
6. **Content Mapping**: Topic IDs in JSON map to content files via `@{id}.md` suffix

## Sample Implementation (Python)

```python
import requests
import yaml
import json
import re
from typing import Dict, List, Any

class RoadmapExtractor:
    BASE_URL = "https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master"
    API_URL = "https://api.github.com/repos/kamranahmedse/developer-roadmap"
    
    def get_all_roadmaps(self) -> List[str]:
        """Get list of all available roadmaps"""
        url = f"{self.API_URL}/contents/src/data/roadmaps"
        response = requests.get(url)
        response.raise_for_status()
        return [item['name'] for item in response.json() if item['type'] == 'dir']
    
    def get_roadmap_metadata(self, roadmap_name: str) -> Dict[str, Any]:
        """Extract metadata from .md file"""
        url = f"{self.BASE_URL}/src/data/roadmaps/{roadmap_name}/{roadmap_name}.md"
        response = requests.get(url)
        response.raise_for_status()
        
        content = response.text
        if content.startswith('---'):
            parts = content.split('---', 2)
            metadata = yaml.safe_load(parts[1])
            return metadata
        return {}
    
    def get_roadmap_structure(self, roadmap_name: str) -> Dict[str, Any]:
        """Extract nodes and edges from JSON"""
        url = f"{self.BASE_URL}/src/data/roadmaps/{roadmap_name}/{roadmap_name}.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_topic_content(self, roadmap_name: str, content_file: str) -> str:
        """Get content for a specific topic"""
        url = f"{self.BASE_URL}/src/data/roadmaps/{roadmap_name}/content/{content_file}"
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    
    def extract_topics(self, structure: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract all topics from roadmap structure"""
        topics = []
        for node in structure.get('nodes', []):
            if node.get('type') == 'topic':
                topics.append({
                    'id': node['id'],
                    'label': node.get('data', {}).get('label', ''),
                    'position': node.get('position', {}),
                })
        return topics
    
    def extract_full_roadmap(self, roadmap_name: str) -> Dict[str, Any]:
        """Extract complete roadmap data"""
        metadata = self.get_roadmap_metadata(roadmap_name)
        structure = self.get_roadmap_structure(roadmap_name)
        topics = self.extract_topics(structure)
        
        return {
            'name': roadmap_name,
            'metadata': metadata,
            'topics': topics,
            'edges': structure.get('edges', []),
            'topic_count': len(topics),
        }

# Usage
extractor = RoadmapExtractor()

# Get all roadmaps
all_roadmaps = extractor.get_all_roadmaps()
print(f"Found {len(all_roadmaps)} roadmaps")

# Extract specific roadmap
backend = extractor.extract_full_roadmap('backend')
print(f"Backend roadmap: {backend['topic_count']} topics")
print(f"Title: {backend['metadata'].get('title')}")

# Extract all roadmaps
for roadmap_name in all_roadmaps[:5]:  # First 5 for demo
    data = extractor.extract_full_roadmap(roadmap_name)
    print(f"{roadmap_name}: {data['topic_count']} topics")
```

## Conclusion

**Easiest Method**: Direct GitHub raw file access via HTTP requests

**Why it's easiest**:
1. No authentication required
2. Simple HTTP GET requests
3. Standard data formats (JSON, YAML, Markdown)
4. Works in any programming language
5. No installation or setup needed
6. Direct access to source of truth

**Next Steps**:
1. Decide on your use case (analysis, app integration, etc.)
2. Choose implementation language
3. Implement the extractor using Method 1
4. Parse and store the data in your preferred format
5. Set up periodic updates if needed

## Additional Resources

- **Repository**: https://github.com/kamranahmedse/developer-roadmap
- **Contributing Guide**: https://github.com/kamranahmedse/developer-roadmap/blob/master/contributing.md
- **License**: Custom (check repository license file)
- **Tech Stack**: Astro, React, TypeScript
