#!/usr/bin/env python3
"""
Generate marketplace.json for Claude Code skill distribution.
Auto-discovers skills and creates marketplace configuration.
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    yaml = None


def parse_frontmatter(content: str) -> tuple[dict | None, str | None]:
    """
    Parse YAML frontmatter from SKILL.md content.
    Returns (frontmatter_dict, error_message)
    """
    if not content.startswith('---'):
        return None, "No YAML frontmatter found"

    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    if yaml:
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            if not isinstance(frontmatter, dict):
                return None, "Frontmatter must be a YAML dictionary"
            return frontmatter, None
        except yaml.YAMLError as e:
            return None, f"Invalid YAML: {e}"
    else:
        # Fallback: simple key-value parsing
        frontmatter = {}
        current_key = None
        current_value = []

        for line in frontmatter_text.split('\n'):
            if ':' in line and not line.startswith(' ') and not line.startswith('\t'):
                # Save previous key if exists
                if current_key:
                    frontmatter[current_key] = ' '.join(current_value).strip()

                key, _, value = line.partition(':')
                current_key = key.strip()
                current_value = [value.strip()] if value.strip() else []
            elif current_key and line.strip():
                current_value.append(line.strip())

        if current_key:
            frontmatter[current_key] = ' '.join(current_value).strip()

        return frontmatter, None


def discover_skills(marketplace_path: Path) -> list[dict]:
    """
    Discover all skills in the marketplace directory.
    Returns list of skill info dicts.
    """
    skills = []
    skills_dir = marketplace_path / 'skills'

    if not skills_dir.exists():
        return skills

    for item in sorted(skills_dir.iterdir()):
        if item.is_dir():
            skill_md = item / 'SKILL.md'
            if skill_md.exists():
                content = skill_md.read_text(encoding='utf-8')
                frontmatter, error = parse_frontmatter(content)

                if frontmatter and not error:
                    skill_info = {
                        'name': frontmatter.get('name', item.name),
                        'description': frontmatter.get('description', ''),
                        'path': f"./skills/{item.name}",
                        'dir_name': item.name
                    }
                    skills.append(skill_info)
                else:
                    print(f"Warning: Could not parse {skill_md}: {error}", file=sys.stderr)

    return skills


def generate_marketplace_json(
    marketplace_path: Path,
    name: str,
    owner_name: str,
    owner_email: str,
    description: Optional[str] = None,
    version: str = "1.0.0",
    plugin_name: Optional[str] = None,
    plugin_description: Optional[str] = None
) -> dict:
    """
    Generate marketplace.json structure.
    """
    skills = discover_skills(marketplace_path)

    if not skills:
        print("Warning: No skills found in skills/ directory", file=sys.stderr)

    # Build skills paths list
    skill_paths = [s['path'] for s in skills]

    # Build skill descriptions for plugin description
    if not plugin_description and skills:
        skill_names = [s['name'] for s in skills]
        plugin_description = f"Skills: {', '.join(skill_names)}"

    marketplace = {
        "name": name,
        "owner": {
            "name": owner_name,
            "email": owner_email
        },
        "metadata": {
            "description": description or f"Claude Code skills marketplace: {name}",
            "version": version
        },
        "plugins": [
            {
                "name": plugin_name or name,
                "description": plugin_description or "Skill collection",
                "source": "./",
                "strict": False,
                "skills": skill_paths
            }
        ]
    }

    return marketplace


def main():
    parser = argparse.ArgumentParser(
        description='Generate marketplace.json for Claude Code skill distribution',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s . --name my-skills --owner-name "John Doe" --owner-email "john@example.com"
  %(prog)s /path/to/marketplace --name team-tools --owner-name "Team" --owner-email "team@company.com"
        """
    )

    parser.add_argument(
        'marketplace_path',
        help='Path to the marketplace root directory'
    )
    parser.add_argument(
        '--name', '-n',
        required=True,
        help='Marketplace name (hyphen-case recommended)'
    )
    parser.add_argument(
        '--owner-name',
        required=True,
        help='Owner display name'
    )
    parser.add_argument(
        '--owner-email',
        required=True,
        help='Owner contact email'
    )
    parser.add_argument(
        '--description', '-d',
        help='Marketplace description'
    )
    parser.add_argument(
        '--version', '-v',
        default='1.0.0',
        help='Marketplace version (default: 1.0.0)'
    )
    parser.add_argument(
        '--plugin-name',
        help='Plugin group name (default: same as marketplace name)'
    )
    parser.add_argument(
        '--plugin-description',
        help='Plugin group description'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file path (default: <marketplace>/.claude-plugin/marketplace.json)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Print JSON to stdout without writing file'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output only JSON (for scripting)'
    )

    args = parser.parse_args()

    marketplace_path = Path(args.marketplace_path).resolve()

    if not marketplace_path.exists():
        print(f"Error: Marketplace path does not exist: {marketplace_path}", file=sys.stderr)
        sys.exit(1)

    # Generate marketplace.json
    marketplace = generate_marketplace_json(
        marketplace_path=marketplace_path,
        name=args.name,
        owner_name=args.owner_name,
        owner_email=args.owner_email,
        description=args.description,
        version=args.version,
        plugin_name=args.plugin_name,
        plugin_description=args.plugin_description
    )

    json_output = json.dumps(marketplace, indent=2)

    if args.dry_run or args.json:
        print(json_output)
        if not args.json:
            print(f"\n(Dry run - no file written)", file=sys.stderr)
        sys.exit(0)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = marketplace_path / '.claude-plugin' / 'marketplace.json'

    # Create directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write file
    output_path.write_text(json_output + '\n', encoding='utf-8')

    print(f"Generated marketplace.json at: {output_path}")
    print(f"  - Name: {marketplace['name']}")
    print(f"  - Owner: {marketplace['owner']['name']} <{marketplace['owner']['email']}>")
    print(f"  - Skills found: {len(marketplace['plugins'][0]['skills'])}")

    for skill_path in marketplace['plugins'][0]['skills']:
        print(f"    • {skill_path}")


if __name__ == "__main__":
    main()
