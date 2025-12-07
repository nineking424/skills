#!/usr/bin/env python3
"""
Skill validation script for marketplace distribution.
Validates skill structure, frontmatter, and content requirements.
"""

import sys
import os
import re
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


def parse_frontmatter(content: str) -> tuple[dict | None, str, str | None]:
    """
    Parse YAML frontmatter from SKILL.md content.
    Returns (frontmatter_dict, body, error_message)
    """
    if not content.startswith('---'):
        return None, content, "No YAML frontmatter found (must start with ---)"

    match = re.match(r'^---\n(.*?)\n---\n?(.*)', content, re.DOTALL)
    if not match:
        return None, content, "Invalid frontmatter format (missing closing ---)"

    frontmatter_text = match.group(1)
    body = match.group(2)

    if yaml:
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            if not isinstance(frontmatter, dict):
                return None, body, "Frontmatter must be a YAML dictionary"
        except yaml.YAMLError as e:
            return None, body, f"Invalid YAML in frontmatter: {e}"
    else:
        # Fallback: simple YAML parsing without yaml library
        frontmatter = {}
        current_key = None
        current_list = None

        for line in frontmatter_text.split('\n'):
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith('#'):
                continue

            # Check if this is a list item (starts with -)
            if stripped.startswith('- '):
                if current_key and current_list is not None:
                    current_list.append(stripped[2:].strip())
                continue

            # Check if this is a key-value pair (not indented, has colon)
            if ':' in line and not line.startswith(' ') and not line.startswith('\t'):
                # Save previous list if exists
                if current_key and current_list is not None:
                    frontmatter[current_key] = current_list

                key, _, value = line.partition(':')
                current_key = key.strip()
                value = value.strip()

                if value:
                    # Simple value
                    frontmatter[current_key] = value
                    current_list = None
                else:
                    # Might be a list or multi-line value
                    current_list = []

        # Save final list if exists
        if current_key and current_list is not None:
            frontmatter[current_key] = current_list if current_list else ''

    return frontmatter, body, None


def validate_skill(skill_path: str, output_json: bool = False) -> dict:
    """
    Validate a skill for marketplace distribution.

    Returns dict with:
        - valid: bool
        - errors: list of error messages
        - warnings: list of warning messages
        - skill_name: str or None
        - skill_path: str
    """
    result = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "skill_name": None,
        "skill_path": str(skill_path)
    }

    skill_path = Path(skill_path)

    # Check skill directory exists
    if not skill_path.exists():
        result["valid"] = False
        result["errors"].append(f"Path does not exist: {skill_path}")
        return result

    if not skill_path.is_dir():
        result["valid"] = False
        result["errors"].append(f"Path is not a directory: {skill_path}")
        return result

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        result["valid"] = False
        result["errors"].append("SKILL.md not found in skill directory")
        return result

    # Read and parse content
    content = skill_md.read_text(encoding='utf-8')
    frontmatter, body, parse_error = parse_frontmatter(content)

    if parse_error:
        result["valid"] = False
        result["errors"].append(parse_error)
        return result

    # Validate allowed frontmatter properties
    ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata'}
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        result["valid"] = False
        result["errors"].append(
            f"Unexpected key(s) in frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required fields
    if 'name' not in frontmatter:
        result["valid"] = False
        result["errors"].append("Missing required 'name' field in frontmatter")

    if 'description' not in frontmatter:
        result["valid"] = False
        result["errors"].append("Missing required 'description' field in frontmatter")

    # Validate name field
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        result["valid"] = False
        result["errors"].append(f"'name' must be a string, got {type(name).__name__}")
        name = ''
    else:
        name = name.strip()
        result["skill_name"] = name

        if name:
            # Check naming convention (hyphen-case)
            if not re.match(r'^[a-z0-9-]+$', name):
                result["valid"] = False
                result["errors"].append(
                    f"Name '{name}' must be hyphen-case (lowercase letters, digits, hyphens only)"
                )

            if name.startswith('-') or name.endswith('-') or '--' in name:
                result["valid"] = False
                result["errors"].append(
                    f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
                )

            # Check name length
            if len(name) > 64:
                result["valid"] = False
                result["errors"].append(
                    f"Name too long ({len(name)} chars). Maximum is 64 characters."
                )

            # Check directory name matches skill name
            dir_name = skill_path.name
            if dir_name != name:
                result["valid"] = False
                result["errors"].append(
                    f"Directory name '{dir_name}' must match skill name '{name}'"
                )
        else:
            result["valid"] = False
            result["errors"].append("'name' field cannot be empty")

    # Validate description field
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        result["valid"] = False
        result["errors"].append(f"'description' must be a string, got {type(description).__name__}")
        description = ''
    else:
        description = description.strip()

        if description:
            # Check for angle brackets
            if '<' in description or '>' in description:
                result["valid"] = False
                result["errors"].append("Description cannot contain angle brackets (< or >)")

            # Check description length
            if len(description) > 1024:
                result["valid"] = False
                result["errors"].append(
                    f"Description too long ({len(description)} chars). Maximum is 1024 characters."
                )

            # Warning for very short descriptions
            if len(description) < 50:
                result["warnings"].append(
                    f"Description is short ({len(description)} chars). Consider adding more detail."
                )
        else:
            result["valid"] = False
            result["errors"].append("'description' field cannot be empty")

    # Check for TODO placeholders in body (exclude code blocks)
    # Remove code blocks before checking
    body_no_code = re.sub(r'```.*?```', '', body, flags=re.DOTALL)
    body_no_code = re.sub(r'`[^`]+`', '', body_no_code)

    todo_patterns = [r'\[TODO\]', r'\[PLACEHOLDER\]']
    for pattern in todo_patterns:
        if re.search(pattern, body_no_code, re.IGNORECASE):
            result["warnings"].append(
                f"Found TODO/placeholder in SKILL.md body. Remove before distribution."
            )
            break

    # Check body has content
    body_stripped = body.strip()
    if not body_stripped:
        result["warnings"].append("SKILL.md body is empty. Consider adding instructions.")
    elif len(body_stripped) < 100:
        result["warnings"].append("SKILL.md body is very short. Consider adding more content.")

    # Check for extraneous files
    extraneous_files = ['README.md', 'CHANGELOG.md', 'INSTALLATION_GUIDE.md']
    for fname in extraneous_files:
        if (skill_path / fname).exists():
            result["warnings"].append(
                f"Found extraneous file '{fname}'. Skills should not include auxiliary documentation."
            )

    return result


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Validate a skill for marketplace distribution'
    )
    parser.add_argument('skill_path', help='Path to the skill directory')
    parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='Output result as JSON'
    )

    args = parser.parse_args()

    result = validate_skill(args.skill_path)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        # Human-readable output
        if result["valid"]:
            print(f"✓ Skill '{result['skill_name']}' is valid!")
        else:
            print(f"✗ Skill validation failed")

        if result["errors"]:
            print("\nErrors:")
            for error in result["errors"]:
                print(f"  • {error}")

        if result["warnings"]:
            print("\nWarnings:")
            for warning in result["warnings"]:
                print(f"  ⚠ {warning}")

    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
