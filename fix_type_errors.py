#!/usr/bin/env python3
"""
Script to automatically fix common Pylance type checking errors
"""

import os
import re
from pathlib import Path

# Files to process
FILES_TO_FIX = [
    "src/ss_ai_server/domain/entities/*.py",
    "src/ss_ai_server/domain/value_objects/*.py",
    "src/ss_ai_server/domain/interfaces/*.py",
    "src/ss_ai_server/domain/services/*.py",
    "src/ss_ai_server/application/dto/**/*.py",
    "src/ss_ai_server/application/use_cases/*.py",
    "src/ss_ai_server/infrastructure/**/*.py",
    "src/ss_ai_server/presentation/api/v1/*.py",
    "src/ss_ai_server/exceptions/*.py",
    "src/ss_ai_server/container.py",
]

def fix_unused_imports(content: str) -> str:
    """Remove unused imports"""
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        # Check for unused imports
        if line.strip().startswith('from typing import'):
            # Extract imported names
            imports = line.replace('from typing import', '').strip()
            import_names = [name.strip() for name in imports.split(',')]
            
            # Check which imports are actually used in the file
            used_imports = []
            for imp in import_names:
                if imp in content and imp != 'Any' and imp != 'Dict':
                    used_imports.append(imp)
            
            # Rebuild import line
            if used_imports:
                new_line = f"from typing import {', '.join(used_imports)}"
                new_lines.append(new_line)
            # If no imports used, skip the line
        elif line.strip().startswith('import ') and 'typing' not in line:
            # Keep other imports
            new_lines.append(line)
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)

def fix_dict_type_annotations(content: str) -> str:
    """Fix dict type annotations to use proper typing"""
    # Replace dict[str, Any] with Dict[str, Any]
    content = re.sub(r'\bdict\[', 'Dict[', content)
    return content

def add_missing_imports(content: str) -> str:
    """Add missing imports for Dict, List if needed"""
    if 'Dict[' in content and 'from typing import' in content:
        # Check if Dict is imported
        if 'Dict' not in content.split('from typing import')[1].split('\n')[0]:
            content = content.replace('from typing import', 'from typing import Dict, ', 1)
    
    if 'List[' in content and 'from typing import' in content:
        if 'List' not in content.split('from typing import')[1].split('\n')[0]:
            content = content.replace('from typing import', 'from typing import List, ', 1)
    
    return content

def process_file(filepath: Path):
    """Process a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply fixes
        content = fix_unused_imports(content)
        content = fix_dict_type_annotations(content)
        content = add_missing_imports(content)
        
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
    
    print("🔧 Fixing Pylance type checking errors...\n")
    
    # Process each file pattern
    for pattern in FILES_TO_FIX:
        if '**' in pattern:
            # Recursive glob
            for filepath in base_path.glob(pattern):
                if filepath.is_file() and filepath.suffix == '.py':
                    process_file(filepath)
        else:
            # Simple glob
            for filepath in base_path.glob(pattern):
                if filepath.is_file() and filepath.suffix == '.py':
                    process_file(filepath)
    
    print("\n✅ Type error fixing complete!")
    print("\nNote: Some Pylance warnings may remain for:")
    print("  - Unimplemented interfaces (expected, will be resolved in Phase 2)")
    print("  - Missing return type hints (cosmetic, don't affect runtime)")
    print("  - Import resolution for dynamic dependencies (by design)")

if __name__ == '__main__':
    main()