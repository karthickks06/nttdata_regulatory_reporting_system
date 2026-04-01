"""Helper utility functions"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import re
import json


def generate_unique_id(prefix: str = "") -> str:
    """Generate unique ID with optional prefix"""
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    return f"{prefix}{timestamp}" if prefix else timestamp


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime to string"""
    return dt.strftime(format_str)


def parse_datetime(dt_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
    """Parse datetime from string"""
    try:
        return datetime.strptime(dt_str, format_str)
    except Exception:
        return None


def is_valid_email(email: str) -> bool:
    """Validate email address"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing invalid characters"""
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')
    return sanitized


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate string to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split list into chunks"""
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


def flatten_dict(d: Dict, parent_key: str = '', separator: str = '.') -> Dict:
    """Flatten nested dictionary"""
    items = []
    for key, value in d.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key

        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key, separator).items())
        else:
            items.append((new_key, value))

    return dict(items)


def deep_merge(dict1: Dict, dict2: Dict) -> Dict:
    """Deep merge two dictionaries"""
    result = dict1.copy()

    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value

    return result


def calculate_percentage(part: float, total: float, decimals: int = 2) -> float:
    """Calculate percentage"""
    if total == 0:
        return 0.0
    return round((part / total) * 100, decimals)


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def extract_numbers(text: str) -> List[float]:
    """Extract all numbers from text"""
    pattern = r'-?\d+\.?\d*'
    matches = re.findall(pattern, text)
    return [float(m) for m in matches]


def remove_duplicates(items: List[Any], key: Optional[str] = None) -> List[Any]:
    """Remove duplicates from list"""
    if key:
        seen = set()
        result = []
        for item in items:
            item_key = item.get(key) if isinstance(item, dict) else getattr(item, key, None)
            if item_key not in seen:
                seen.add(item_key)
                result.append(item)
        return result
    else:
        return list(dict.fromkeys(items))


def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """Safely load JSON string"""
    try:
        return json.loads(json_str)
    except Exception:
        return default


def safe_json_dumps(obj: Any, default: str = "{}") -> str:
    """Safely dump object to JSON string"""
    try:
        return json.dumps(obj, default=str)
    except Exception:
        return default


def create_date_range(
    start_date: datetime,
    end_date: datetime,
    interval_days: int = 1
) -> List[datetime]:
    """Create list of dates between start and end"""
    dates = []
    current = start_date

    while current <= end_date:
        dates.append(current)
        current += timedelta(days=interval_days)

    return dates


def mask_sensitive_data(text: str, pattern: str = r'\b\d{3}-\d{2}-\d{4}\b') -> str:
    """Mask sensitive data in text using pattern"""
    return re.sub(pattern, '***-**-****', text)


def convert_snake_to_camel(snake_str: str) -> str:
    """Convert snake_case to camelCase"""
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def convert_camel_to_snake(camel_str: str) -> str:
    """Convert camelCase to snake_case"""
    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()


def batch_process(
    items: List[Any],
    batch_size: int,
    process_func: callable
) -> List[Any]:
    """Process items in batches"""
    results = []
    chunks = chunk_list(items, batch_size)

    for chunk in chunks:
        chunk_results = process_func(chunk)
        results.extend(chunk_results)

    return results


def retry_on_exception(
    func: callable,
    max_retries: int = 3,
    delay: float = 1.0,
    exceptions: tuple = (Exception,)
):
    """Decorator to retry function on exception"""
    import time
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                if attempt == max_retries - 1:
                    raise
                time.sleep(delay * (attempt + 1))

        return None

    return wrapper
