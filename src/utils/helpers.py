"""Helper functions"""

import uuid
from datetime import datetime

def generate_id():
    """Generate unique ID"""
    return str(uuid.uuid4())

def get_timestamp():
    """Get current timestamp"""
    return datetime.now().isoformat()

def format_duration(seconds):
    """Format duration in seconds to readable format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def dict_to_json(data):
    """Convert dict to JSON string"""
    import json
    return json.dumps(data, indent=2)