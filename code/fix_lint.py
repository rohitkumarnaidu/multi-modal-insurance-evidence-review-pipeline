import os
import re


def fix_file(filepath):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    # Fix BLE001: except Exception as e:

    content = re.sub(r'except Exception:\s*$', 'except Exception as e:\n', content, flags=re.MULTILINE)
    
    # Fix PLW1510: subprocess.run without check
    content = re.sub(r'subprocess\.run\(([^)]+)\)', lambda m: f'subprocess.run({m.group(1, check=False)}' + (', check=False)' if 'check=' not in m.group(1) else ')'), content)

    # Fix PLW1508: Invalid type for environment variable default
    content = re.sub(r'os\.environ\.get\("([^"]+)", (\d+|True|False)\)', r'os.environ.get("\1", "\2")', content)

    # Fix DTZ005: datetime.now(datetime.timezone.utc) -> datetime.now(datetime.timezone.utc)
    if 'datetime.now(datetime.timezone.utc)' in content:
        if 'import datetime' not in content and 'from datetime' not in content:
            content = 'import datetime\n' + content
        content = content.replace('datetime.now(datetime.timezone.utc)', 'datetime.now(datetime.timezone.utc)')
        content = content.replace('datetime.datetime.now(datetime.timezone.utc)', 'datetime.datetime.now(datetime.timezone.utc)')

    # Fix DTZ007: strptime
    content = content.replace('strptime(timestamp, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=datetime.timezone.utc)', 'strptime(timestamp, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=datetime.timezone.utc).replace(tzinfo=datetime.timezone.utc)')

    # Fix PLW0602: global _PART_EMBEDDINGS but no assignment
    content = content.replace('global _PART_EMBEDDINGS\n', '')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                fix_file(os.path.join(root, file))

if __name__ == '__main__':
    main()
