import logging
from pathlib import Path
from PIL import Image
import imagehash

logger = logging.getLogger(__name__)

def _resolve_path(image_path: str) -> Path | None:
    path = Path(image_path)
    if path.exists():
        return path
    
    # Try resolving relative to project root if executed from code/
    code_dir = Path(__file__).resolve().parent.parent
    project_root = code_dir.parent
    
    # Strip leading dots or slashes and try appending to project root
    clean_path = image_path.lstrip("./\\")
    if clean_path.startswith("dataset"):
        resolved = project_root / clean_path
        if resolved.exists():
            return resolved
            
    # Try just appending to dataset directly
    resolved = project_root / "dataset" / "images" / Path(image_path).name
    if resolved.exists():
        return resolved
        
    return None

def compute_phash(image_path: str) -> str | None:
    resolved_path = _resolve_path(image_path)
    if not resolved_path:
        logger.warning(f"Could not resolve image path for hashing: {image_path}")
        return None
    try:
        with Image.open(resolved_path) as img:
            return str(imagehash.phash(img))
    except Exception as e:
        logger.warning(f"Error computing phash for {image_path}: {e}")
        return None

def are_images_similar(hash1: str, hash2: str, threshold: int = 10) -> bool:
    try:
        h1 = imagehash.hex_to_hash(hash1)
        h2 = imagehash.hex_to_hash(hash2)
        return (h1 - h2) < threshold
    except Exception:
        return False

def find_duplicates(image_paths: list[str]) -> list[tuple[int, int, int]]:
    hashes = []
    for p in image_paths:
        h = compute_phash(p)
        hashes.append(h)
    
    duplicates = []
    for i in range(len(hashes)):
        if not hashes[i]:
            continue
        for j in range(i + 1, len(hashes)):
            if not hashes[j]:
                continue
            h1_str = hashes[i]
            h2_str = hashes[j]
            if not h1_str or not h2_str:
                continue
            h1 = imagehash.hex_to_hash(h1_str)
            h2 = imagehash.hex_to_hash(h2_str)
            diff = h1 - h2
            if diff < 10:  # Threshold for near-duplicates
                duplicates.append((i, j, diff))
                
    return duplicates

def max_phash_distance(image_paths: list[str]) -> int | None:
    hashes = []
    for p in image_paths:
        h = compute_phash(p)
        if h:
            hashes.append(imagehash.hex_to_hash(h))
            
    if len(hashes) < 2:
        return None
        
    max_diff = 0
    for i in range(len(hashes)):
        for j in range(i + 1, len(hashes)):
            diff = hashes[i] - hashes[j]
            if diff > max_diff:
                max_diff = diff
                
    return max_diff
