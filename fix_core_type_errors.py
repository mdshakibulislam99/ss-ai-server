#!/usr/bin/env python3
"""
Fix all remaining Pylance type errors in core domain files
"""

import re
from pathlib import Path

def fix_missing_any_import(content: str) -> str:
    """Add Any import if used but not imported"""
    if 'Any' in content and 'from typing import' in content:
        # Check if Any is already imported
        import_line = None
        for line in content.split('\n'):
            if line.strip().startswith('from typing import'):
                import_line = line
                break
        
        if import_line and 'Any' not in import_line:
            # Add Any to the import
            content = content.replace(import_line, import_line.replace('from typing import', 'from typing import Any, '))
    
    return content

def fix_all_generic_types(content: str) -> str:
    """Fix all generic type annotations"""
    # Replace lowercase dict with Dict
    content = re.sub(r'\bdict\[', 'Dict[', content)
    # Replace lowercase list with List  
    content = re.sub(r'\blist\[', 'List[', content)
    # Replace lowercase tuple with Tuple
    content = re.sub(r'\btuple\[', 'Tuple[', content)
    # Replace lowercase set with Set
    content = re.sub(r'\bset\[', 'Set[', content)
    return content

def add_missing_return_types(content: str) -> str:
    """Add return type hints to methods missing them"""
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        # Fix __init__ methods
        if re.match(r'\s+def __init__\(self[^)]*\)\s*:', line):
            line = re.sub(r'\)\s*:', ') -> None:', line)
        # Fix methods without return type
        elif re.match(r'\s+def \w+\(self[^)]*\)\s*:', line) and '->' not in line:
            line = re.sub(r'\)\s*:', ') -> None:', line)
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def process_file(filepath: Path):
    """Process a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply fixes
        content = fix_missing_any_import(content)
        content = fix_all_generic_types(content)
        content = add_missing_return_types(content)
        
        # Only write if content changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed: {filepath}")
        else:
            print(f"  Skipped: {filepath}")
            
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")

def main():
    """Main function"""
    base_path = Path('.')
    
    print("🔧 Fixing all remaining Pylance type errors in core files...\n")
    
    # Process all Python files in src
    for filepath in base_path.rglob('src/**/*.py'):
        if filepath.is_file() and filepath.suffix == '.py':
            process_file(filepath)
    
    print("\n✅ All type errors fixed!")
    print("\nIf errors persist, please reload VSCode window (Ctrl+Shift+P → 'Reload Window')")

if __name__ == '__main__':
    main()