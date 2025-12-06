# Roadmap.sh Analysis - Linear Issue AHS-82

## Executive Summary

This analysis identifies the **easiest way to extract role-based roadmap information** from [roadmap.sh](https://roadmap.sh).

**Answer: Direct HTTP access to GitHub repository files**

- ✅ No authentication required
- ✅ Simple HTTP GET requests  
- ✅ Works with any programming language
- ✅ 71 roadmaps available
- ✅ Structured data (JSON + Markdown)

## Quick Start

### Method 1: Use the Python Script (Recommended)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the extractor
python roadmap_extractor.py
```

This will extract 4 popular roadmaps (backend, frontend, devops, full-stack) and save them as JSON files.

### Method 2: Manual Extraction

```bash
# Get list of all roadmaps
curl https://api.github.com/repos/kamranahmedse/developer-roadmap/contents/src/data/roadmaps

# Get backend roadmap metadata
curl https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master/src/data/roadmaps/backend/backend.md

# Get backend roadmap structure
curl https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master/src/data/roadmaps/backend/backend.json
```

## Files in This Analysis

1. **roadmap-sh-analysis.md** - Comprehensive technical analysis
   - Data structure documentation
   - All extraction methods compared
   - Implementation examples
   - Sample code snippets

2. **roadmap_extractor.py** - Working Python implementation
   - Fetches all 71 roadmaps
   - Extracts metadata, topics, and content
   - Exports to JSON format
   - Well-documented and extensible

3. **requirements.txt** - Python dependencies
   - requests (HTTP client)
   - PyYAML (YAML parser)

4. **Generated JSON files** (after running script):
   - backend_roadmap.json
   - frontend_roadmap.json
   - devops_roadmap.json
   - full-stack_roadmap.json

## Data Structure Overview

### Available Roadmaps (71 total)

Role-based roadmaps include:
- **Development**: backend, frontend, full-stack, mobile (android, ios), game-developer
- **Languages**: python, javascript, golang, java, rust, cpp, php, etc.
- **DevOps**: devops, docker, kubernetes, terraform, aws
- **Data**: data-analyst, data-engineer, ai-data-scientist, machine-learning, mlops
- **Specialized**: security, blockchain, system-design, api-design, ux-design
- **Management**: product-manager, engineering-manager, technical-writer
- And many more...

### File Structure per Roadmap

```
src/data/roadmaps/{roadmap-name}/
├── {name}.md              # Metadata (title, description, SEO)
├── {name}.json            # Visual roadmap (nodes & edges)
├── content/               # Topic descriptions
│   ├── topic1@id.md
│   ├── topic2@id.md
│   └── ...
└── faqs.astro            # FAQ component
```

### JSON Data Format

```json
{
  "metadata": {
    "name": "backend",
    "title": "Backend Developer",
    "description": "Step by step guide...",
    "topic_count": 21
  },
  "topics": [
    {
      "id": "unique-id",
      "label": "Internet",
      "position_x": 100,
      "position_y": 200,
      "content_file": "internet@unique-id.md"
    }
  ],
  "edges": [
    {
      "source": "topic-1-id",
      "target": "topic-2-id"
    }
  ]
}
```

## Why This Method is Easiest

### Comparison of Methods

| Method | Complexity | Auth Required | Rate Limits | Offline |
|--------|-----------|---------------|-------------|---------|
| **Direct GitHub Raw** | ⭐ Low | ❌ No | Generous | ❌ No |
| Clone Repository | ⭐⭐ Medium | ❌ No | None | ✅ Yes |
| GitHub GraphQL API | ⭐⭐⭐ High | ✅ Yes | Strict | ❌ No |
| Web Scraping | ⭐⭐⭐⭐ Very High | ❌ No | Very Strict | ❌ No |

### Why Direct GitHub Access Wins

1. **Simple HTTP**: Just use `requests.get()` or `curl`
2. **No Setup**: No API keys, no git installation, no browser automation
3. **Standard Formats**: JSON and Markdown are easy to parse
4. **Well Structured**: Consistent format across all 71 roadmaps
5. **Active Maintenance**: Repository is updated regularly
6. **Free & Open**: No costs, no rate limit concerns for reasonable use

## Example Output

Running the extractor produces:

```
=== Roadmap.sh Data Extractor ===

Step 1: Fetching list of all roadmaps...
Found 71 roadmaps

Sample roadmaps:
  1. ai-agents
  2. backend
  3. frontend
  ...

Step 2: Extracting popular roadmaps...

Extracting roadmap: backend
  - Title: Backend Developer
  - Topics: 21
  - Content files: 154
Exported to backend_roadmap.json
```

## Use Cases

This extraction method enables:

1. **Learning Platform Integration**: Import roadmaps into your LMS
2. **Career Planning Tools**: Build career path visualizers
3. **Content Aggregation**: Create learning resource compilations
4. **Progress Tracking**: Build skill assessment applications
5. **Analytics**: Analyze skill trends and requirements
6. **Custom Visualizations**: Create interactive roadmap views

## Technical Details

### API Endpoints

```python
# List all roadmaps
GET https://api.github.com/repos/kamranahmedse/developer-roadmap/contents/src/data/roadmaps

# Get metadata
GET https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master/src/data/roadmaps/{name}/{name}.md

# Get structure
GET https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master/src/data/roadmaps/{name}/{name}.json

# Get topic content
GET https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master/src/data/roadmaps/{name}/content/{filename}
```

### Data Parsing

**Metadata (YAML)**:
```python
import yaml
content = response.text
if content.startswith('---'):
    parts = content.split('---', 2)
    metadata = yaml.safe_load(parts[1])
```

**Structure (JSON)**:
```python
import json
data = response.json()
topics = [node for node in data['nodes'] if node['type'] == 'topic']
```

## Customization

### Extract Specific Roadmaps

```python
extractor = RoadmapExtractor()
roadmap = extractor.extract_roadmap('python')
extractor.export_to_json(roadmap, 'python_roadmap.json')
```

### Get All Roadmaps

```python
extractor = RoadmapExtractor()
all_roadmaps = extractor.get_all_roadmaps()

for name in all_roadmaps:
    roadmap = extractor.extract_roadmap(name)
    extractor.export_to_json(roadmap, f'{name}_roadmap.json')
```

### Extract Topic Content

```python
extractor = RoadmapExtractor()
content = extractor.get_topic_content('backend', 'internet@SiYUdtYMDImRPmV2_XPkH.md')
print(content)
```

## Performance

- **Single roadmap**: ~2-3 seconds
- **All 71 roadmaps** (without content): ~2-3 minutes
- **All roadmaps with content**: ~5-10 minutes

*Note: Times may vary based on network speed*

## Limitations

1. **No Real-time API**: Must fetch from GitHub (slight delay for updates)
2. **No Search/Filter**: Must implement your own filtering
3. **Network Required**: Can't work offline (unless using git clone method)
4. **Rate Limits**: GitHub has rate limits (60 req/hour unauthenticated, 5000 with token)

## Next Steps

1. **For Production**: Implement caching to avoid repeated requests
2. **For Scale**: Clone repository and process locally
3. **For Updates**: Set up periodic pulls (daily/weekly)
4. **For API**: Build your own API wrapper around this data

## License & Attribution

- **Source**: https://github.com/kamranahmedse/developer-roadmap
- **License**: Check repository for current license
- **Attribution**: Always credit roadmap.sh and the contributors

## Conclusion

✅ **Question Answered**: The easiest way to extract role-based roadmap information from roadmap.sh is **direct HTTP access to GitHub repository files**.

✅ **Working Implementation**: Provided in `roadmap_extractor.py`

✅ **Comprehensive Documentation**: See `roadmap-sh-analysis.md` for technical details

## Questions?

For detailed technical information, see:
- **Full Analysis**: `roadmap-sh-analysis.md`
- **Source Code**: `roadmap_extractor.py`
- **Original Repository**: https://github.com/kamranahmedse/developer-roadmap
