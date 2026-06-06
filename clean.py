import os
import re

cjk_pattern = re.compile(r'[\u4e00-\u9fff\uac00-\ud7af\u3040-\u309f\u30a0-\u30ff]')

def clean_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return

    original_content = content

    # 1. Remove line comments containing CJK
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if '//' in line:
            comment_idx = line.find('//')
            comment_part = line[comment_idx:]
            if cjk_pattern.search(comment_part):
                line = line[:comment_idx].rstrip()
                if not line.strip():
                    continue
        new_lines.append(line)
    
    content = '\n'.join(new_lines)
    
    # 2. Remove ko: { ... } and ja: { ... } blocks (no nested braces inside them)
    content = re.sub(r'\s*ko:\s*\{[^{}]*\},?', '', content)
    content = re.sub(r'\s*ja:\s*\{[^{}]*\},?', '', content)
    
    # 3. Remove ko: "...", ja: "..." etc in single line objects like labels: { en: "Head", ko: "머리", ja: "頭" }
    content = re.sub(r',\s*ko:\s*".*?"', '', content)
    content = re.sub(r',\s*ja:\s*".*?"', '', content)
    content = re.sub(r',\s*ko:\s*`.*?`', '', content)
    content = re.sub(r',\s*ja:\s*`.*?`', '', content)
    # Also if they are the first key (unlikely but possible)
    content = re.sub(r'\bko:\s*".*?",\s*', '', content)
    content = re.sub(r'\bja:\s*".*?",\s*', '', content)
    
    # 4. Same for arrays of objects with ko: "..."
    # e.g. label: { en: "Black cat", ko: "검은냥이" }
    
    # 5. Remove any other CJK HTML text (simple heuristic: if a line has CJK and is in HTML, remove or clear it)
    if filepath.endswith('.html'):
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if cjk_pattern.search(line) and ('<!--' in line or '-->' in line):
                # It's an HTML comment with CJK
                line = re.sub(r'<!--.*?-->', '', line)
            new_lines.append(line)
        content = '\n'.join(new_lines)
        
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned {filepath}")

for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or 'dist' in root or '.git' in root or '.claude' in root:
        continue
    for file in files:
        if file.endswith(('.js', '.html', '.css', '.json', '.md')):
            clean_file(os.path.join(root, file))
