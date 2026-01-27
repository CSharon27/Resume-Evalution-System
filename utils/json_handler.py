"""
HireLens JSON Handler
Utilities for JSON file operations
"""

import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path


def load_json(path: str | Path) -> Dict | List:
    """
    Load JSON data from file
    
    Args:
        path: Path to JSON file
        
    Returns:
        Parsed JSON data (dict or list)
    """
    path = Path(path)
    
    if not path.exists():
        # Return empty dict for new files
        return {}
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON in {path}, returning empty dict")
        return {}
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return {}


def save_json(data: Dict | List, path: str | Path, indent: int = 2) -> bool:
    """
    Save data to JSON file
    
    Args:
        data: Data to save (dict or list)
        path: Path to JSON file
        indent: JSON indentation (default: 2)
        
    Returns:
        True if successful, False otherwise
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False, default=str)
        return True
    except Exception as e:
        print(f"Error saving to {path}: {e}")
        return False


def append_to_json(data: Dict, path: str | Path, key: Optional[str] = None) -> bool:
    """
    Append data to existing JSON file
    
    Args:
        data: Data to append
        path: Path to JSON file
        key: Optional key to store data under (for dict-based storage)
        
    Returns:
        True if successful, False otherwise
    """
    existing_data = load_json(path)
    
    if isinstance(existing_data, list):
        existing_data.append(data)
    elif isinstance(existing_data, dict):
        if key:
            existing_data[key] = data
        else:
            existing_data.update(data)
    else:
        # Initialize as list if empty
        existing_data = [data]
    
    return save_json(existing_data, path)


def get_by_id(item_id: str, path: str | Path, id_field: str = "id") -> Optional[Dict]:
    """
    Retrieve item by ID from JSON file
    
    Args:
        item_id: ID to search for
        path: Path to JSON file
        id_field: Name of the ID field (default: "id")
        
    Returns:
        Item dict if found, None otherwise
    """
    data = load_json(path)
    
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and item.get(id_field) == item_id:
                return item
    elif isinstance(data, dict):
        # Try direct key access first
        if item_id in data:
            return data[item_id]
        # Search through values
        for  key, item in data.items():
            if isinstance(item, dict) and item.get(id_field) == item_id:
                return item
    
    return None


def get_all(path: str | Path) -> List[Dict]:
    """
    Get all items from JSON file as a list
    
    Args:
        path: Path to JSON file
        
    Returns:
        List of items
    """
    data = load_json(path)
    
    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        return list(data.values())
    else:
        return []


def delete_by_id(item_id: str, path: str | Path, id_field: str = "id") -> bool:
    """
    Delete item by ID from JSON file
    
    Args:
        item_id: ID to delete
        path: Path to JSON file
        id_field: Name of the ID field
        
    Returns:
        True if deleted, False if not found
    """
    data = load_json(path)
    deleted = False
    
    if isinstance(data, list):
        original_len = len(data)
        data = [item for item in data if not (isinstance(item, dict) and item.get(id_field) == item_id)]
        deleted = len(data) < original_len
    elif isinstance(data, dict):
        if item_id in data:
            del data[item_id]
            deleted = True
    
    if deleted:
        save_json(data, path)
    
    return deleted


def update_by_id(item_id: str, updates: Dict, path: str | Path, id_field: str = "id") -> bool:
    """
    Update item by ID in JSON file
    
    Args:
        item_id: ID to update
        updates: Dict of updates to apply
        path: Path to JSON file
        id_field: Name of the ID field
        
    Returns:
        True if updated, False if not found
    """
    data = load_json(path)
    updated = False
    
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and item.get(id_field) == item_id:
                item.update(updates)
                updated = True
                break
    elif isinstance(data, dict):
        if item_id in data and isinstance(data[item_id], dict):
            data[item_id].update(updates)
            updated = True
    
    if updated:
        save_json(data, path)
    
    return updated


def initialize_json_file(path: str | Path, initial_data: Dict | List = None):
    """
    Initialize JSON file with default structure if it doesn't exist
    
    Args:
        path: Path to JSON file
        initial_data: Initial data structure (default: empty dict)
    """
    path = Path(path)
    
    if not path.exists():
        if initial_data is None:
            initial_data = {}
        save_json(initial_data, path)
