#!/usr/bin/env python3
"""
Roadmap.sh Data Extractor

This script extracts role-based roadmap information from the roadmap.sh GitHub repository.
It demonstrates the easiest method: direct HTTP access to GitHub raw files.

Usage:
    python roadmap_extractor.py
"""

import requests
import yaml
import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class RoadmapMetadata:
    """Structured roadmap metadata"""
    name: str
    title: str
    description: str
    brief_title: str
    brief_description: str
    has_topics: bool
    order: Optional[int] = None
    json_url: Optional[str] = None
    pdf_url: Optional[str] = None


@dataclass
class Topic:
    """Individual topic in a roadmap"""
    id: str
    label: str
    position_x: float
    position_y: float
    content_file: Optional[str] = None


@dataclass
class Roadmap:
    """Complete roadmap data"""
    metadata: RoadmapMetadata
    topics: List[Topic]
    edges: List[Dict[str, Any]]
    topic_count: int


class RoadmapExtractor:
    """Extract roadmap data from roadmap.sh GitHub repository"""
    
    BASE_URL = "https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master"
    API_URL = "https://api.github.com/repos/kamranahmedse/developer-roadmap"
    
    def __init__(self):
        """
        Initialize the RoadmapExtractor by creating an HTTP session configured with a custom User-Agent header.
        
        This prepares a persistent requests.Session used for all outbound GitHub/raw HTTP requests.
        """
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'RoadmapExtractor/1.0'
        })
    
    def get_all_roadmaps(self) -> List[str]:
        """
        Retrieve the names of roadmap directories from the repository's contents API.
        
        Returns:
            A list of roadmap directory names (e.g., ['backend', 'frontend', 'devops']).
        """
        url = f"{self.API_URL}/contents/src/data/roadmaps"
        response = self.session.get(url)
        response.raise_for_status()
        
        items = response.json()
        return [item['name'] for item in items if item['type'] == 'dir']
    
    def get_roadmap_metadata(self, roadmap_name: str) -> RoadmapMetadata:
        """
        Parse a roadmap's markdown file and return its YAML frontmatter as structured metadata.
        
        Parameters:
            roadmap_name (str): Roadmap directory/name (e.g., "backend") used to locate the markdown file.
        
        Returns:
            RoadmapMetadata: Metadata populated from the file's YAML frontmatter. If frontmatter is missing or keys are absent, text fields default to empty strings, `has_topics` defaults to `False`, and optional fields remain `None`.
        
        Raises:
            requests.HTTPError: If fetching the roadmap markdown fails (non-2xx HTTP response).
        """
        url = f"{self.BASE_URL}/src/data/roadmaps/{roadmap_name}/{roadmap_name}.md"
        response = self.session.get(url)
        response.raise_for_status()
        
        content = response.text
        metadata_dict = {}
        
        # Parse YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 2:
                metadata_dict = yaml.safe_load(parts[1]) or {}
        
        # Create structured metadata
        return RoadmapMetadata(
            name=roadmap_name,
            title=metadata_dict.get('title', ''),
            description=metadata_dict.get('description', ''),
            brief_title=metadata_dict.get('briefTitle', ''),
            brief_description=metadata_dict.get('briefDescription', ''),
            has_topics=metadata_dict.get('hasTopics', False),
            order=metadata_dict.get('order'),
            json_url=metadata_dict.get('jsonUrl'),
            pdf_url=metadata_dict.get('pdfUrl'),
        )
    
    def get_roadmap_structure(self, roadmap_name: str) -> Dict[str, Any]:
        """
        Extract nodes and edges from roadmap's JSON file.
        
        Args:
            roadmap_name: Name of the roadmap
            
        Returns:
            Dictionary with 'nodes' and 'edges' arrays
        """
        url = f"{self.BASE_URL}/src/data/roadmaps/{roadmap_name}/{roadmap_name}.json"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_content_files(self, roadmap_name: str) -> List[str]:
        """
        Return the list of markdown content filenames for the given roadmap.
        
        If the roadmap has no content directory or the directory is inaccessible, an empty list is returned.
        
        Parameters:
            roadmap_name (str): Identifier of the roadmap directory to query.
        
        Returns:
            List[str]: Filenames of `.md` files found in the roadmap's content directory.
        """
        url = f"{self.API_URL}/contents/src/data/roadmaps/{roadmap_name}/content"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            items = response.json()
            return [item['name'] for item in items if item['type'] == 'file' and item['name'].endswith('.md')]
        except requests.exceptions.HTTPError:
            # Content directory might not exist
            return []
    
    def get_topic_content(self, roadmap_name: str, content_file: str) -> str:
        """
        Retrieve the raw markdown content for a specific topic file in a roadmap.
        
        Parameters:
            roadmap_name (str): Roadmap directory name (e.g., "frontend").
            content_file (str): Content filename within the roadmap's content directory (e.g., "internet@abc123.md").
        
        Returns:
            The raw markdown text of the specified content file.
        
        Raises:
            requests.HTTPError: If the HTTP request for the content file fails.
        """
        url = f"{self.BASE_URL}/src/data/roadmaps/{roadmap_name}/content/{content_file}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.text
    
    def extract_topics(self, structure: Dict[str, Any]) -> List[Topic]:
        """
        Extract all topics from roadmap structure.
        
        Args:
            structure: Parsed JSON structure with nodes and edges
            
        Returns:
            List of Topic objects
        """
        topics = []
        for node in structure.get('nodes', []):
            if node.get('type') == 'topic':
                position = node.get('position', {})
                label = node.get('data', {}).get('label', '')
                
                topics.append(Topic(
                    id=node['id'],
                    label=label,
                    position_x=position.get('x', 0),
                    position_y=position.get('y', 0),
                ))
        return topics
    
    def extract_roadmap(self, roadmap_name: str, include_content: bool = False) -> Roadmap:
        """
        Assemble a Roadmap object for the given roadmap name.
        
        Fetches the roadmap's metadata and structure, extracts topic nodes, and, if requested, retrieves content file names and associates them to topics by matching filenames of the form `name@ID.md`.
        
        Parameters:
            roadmap_name (str): The roadmap identifier to extract.
            include_content (bool): If True, fetch content file listings and attach matching content filenames to topics.
        
        Returns:
            Roadmap: A Roadmap populated with metadata, topics (with optional content_file), edges, and topic_count.
        """
        print(f"Extracting roadmap: {roadmap_name}")
        
        # Get metadata
        metadata = self.get_roadmap_metadata(roadmap_name)
        print(f"  - Title: {metadata.title}")
        
        # Get structure
        structure = self.get_roadmap_structure(roadmap_name)
        topics = self.extract_topics(structure)
        print(f"  - Topics: {len(topics)}")
        
        # Optionally fetch content files
        if include_content:
            content_files = self.get_content_files(roadmap_name)
            print(f"  - Content files: {len(content_files)}")
            
            # Map content files to topics by ID
            content_map = {}
            for file in content_files:
                # Extract ID from filename (format: name@ID.md)
                match = re.search(r'@([^.]+)\.md$', file)
                if match:
                    content_map[match.group(1)] = file
            
            # Assign content files to topics
            for topic in topics:
                if topic.id in content_map:
                    topic.content_file = content_map[topic.id]
        
        return Roadmap(
            metadata=metadata,
            topics=topics,
            edges=structure.get('edges', []),
            topic_count=len(topics),
        )
    
    def export_to_json(self, roadmap: Roadmap, output_file: str):
        """
        Export roadmap to JSON file.
        
        Args:
            roadmap: Roadmap object to export
            output_file: Path to output JSON file
        """
        data = {
            'metadata': asdict(roadmap.metadata),
            'topics': [asdict(topic) for topic in roadmap.topics],
            'edges': roadmap.edges,
            'topic_count': roadmap.topic_count,
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Exported to {output_file}")


def main():
    """
    Run a demonstration that fetches roadmaps from roadmap.sh and exports selected ones to JSON.
    
    This function:
    - Prints progress and informational messages to stdout.
    - Retrieves the list of available roadmaps, prints a short sample, and attempts to extract a set of popular roadmaps ('backend', 'frontend', 'devops', 'full-stack') if present.
    - When extraction succeeds, writes each roadmap to a file named "<roadmap_name>_roadmap.json" using the extractor's export_to_json method.
    - Continues past individual extraction errors and prints a final summary of available and exported roadmaps.
    """
    print("=== Roadmap.sh Data Extractor ===\n")
    
    extractor = RoadmapExtractor()
    
    # 1. Get all roadmaps
    print("Step 1: Fetching list of all roadmaps...")
    all_roadmaps = extractor.get_all_roadmaps()
    print(f"Found {len(all_roadmaps)} roadmaps\n")
    
    # 2. Show sample of available roadmaps
    print("Sample roadmaps:")
    for i, name in enumerate(all_roadmaps[:10], 1):
        print(f"  {i}. {name}")
    print(f"  ... and {len(all_roadmaps) - 10} more\n")
    
    # 3. Extract a few popular roadmaps
    popular_roadmaps = ['backend', 'frontend', 'devops', 'full-stack']
    
    print("Step 2: Extracting popular roadmaps...\n")
    for roadmap_name in popular_roadmaps:
        if roadmap_name in all_roadmaps:
            try:
                roadmap = extractor.extract_roadmap(roadmap_name, include_content=True)
                
                # Export to JSON
                output_file = f"{roadmap_name}_roadmap.json"
                extractor.export_to_json(roadmap, output_file)
                print()
                
            except Exception as e:
                print(f"  Error extracting {roadmap_name}: {e}\n")
    
    # 4. Summary statistics
    print("\n=== Summary ===")
    print(f"Total roadmaps available: {len(all_roadmaps)}")
    print(f"Successfully extracted: {len(popular_roadmaps)}")
    print("\nExtracted roadmaps saved as JSON files:")
    for name in popular_roadmaps:
        if name in all_roadmaps:
            print(f"  - {name}_roadmap.json")


if __name__ == "__main__":
    main()