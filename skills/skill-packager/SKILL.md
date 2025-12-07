---
name: skill-packager
description: Package and prepare skills for Claude Code marketplace distribution. Use when generating marketplace.json files, validating skill structure for distribution, preparing skills for public sharing, or setting up a new Claude Code marketplace. Triggers on requests to package skills, create marketplace configs, validate skills for distribution, or configure skill repositories for sharing.
allowed-tools:
  - Bash(python3:*)
  - Read
  - Write
  - Glob
---

# Skill Packager

Prepare and package skills for Claude Code marketplace distribution.

## Overview

This skill helps you:
- Validate skills meet marketplace requirements
- Generate marketplace.json configuration files
- Set up repositories for skill distribution

## Workflow

1. **Validate a skill** → Run `scripts/validate_skill.py`
2. **Generate marketplace.json** → Run `scripts/generate_marketplace.py`
3. **Set up new marketplace** → Follow setup workflow below

## Validate a Skill

Before distributing, validate skill structure:

```bash
python3 scripts/validate_skill.py <skill-path>
```

JSON output for scripting:

```bash
python3 scripts/validate_skill.py <skill-path> --json
```

### Validation Checks

- SKILL.md exists with valid YAML frontmatter
- Required fields: `name`, `description`
- Name follows hyphen-case convention (max 64 chars)
- Description constraints (no angle brackets, max 1024 chars)
- Directory name matches skill name
- No TODO placeholders in body
- No extraneous files (README.md, CHANGELOG.md)

## Generate marketplace.json

Create marketplace configuration:

```bash
python3 scripts/generate_marketplace.py <marketplace-path> \
  --name "marketplace-name" \
  --owner-name "Your Name" \
  --owner-email "email@example.com"
```

### Options

| Option | Description |
|--------|-------------|
| `--name`, `-n` | Marketplace name (required) |
| `--owner-name` | Owner display name (required) |
| `--owner-email` | Contact email (required) |
| `--description`, `-d` | Marketplace description |
| `--version`, `-v` | Version (default: 1.0.0) |
| `--output`, `-o` | Output file path |
| `--dry-run` | Preview without writing |

### Example

```bash
python3 scripts/generate_marketplace.py /path/to/repo \
  --name "my-skills" \
  --owner-name "Developer" \
  --owner-email "dev@example.com" \
  --description "My Claude Code skills collection"
```

## Set Up New Marketplace

### Step 1: Create Directory Structure

```
my-marketplace/
├── .claude-plugin/
│   └── marketplace.json
├── skills/
│   └── my-skill/
│       └── SKILL.md
└── README.md (optional)
```

### Step 2: Create Skills

Each skill needs a `SKILL.md` with frontmatter:

```yaml
---
name: my-skill
description: What this skill does and when to use it.
---
```

### Step 3: Generate marketplace.json

```bash
python3 scripts/generate_marketplace.py . \
  --name "my-marketplace" \
  --owner-name "Your Name" \
  --owner-email "you@example.com"
```

### Step 4: Validate

```bash
python3 scripts/validate_skill.py skills/my-skill
```

### Step 5: Distribute

Push to GitHub. Users add via:

```
/plugin marketplace add owner/repo
```

## marketplace.json Structure

Quick reference (see [references/marketplace-schema.md](references/marketplace-schema.md) for full schema):

```json
{
  "name": "marketplace-name",
  "owner": {
    "name": "Owner Name",
    "email": "email@example.com"
  },
  "metadata": {
    "description": "Marketplace description",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "description": "Plugin description",
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/skill-name"
      ]
    }
  ]
}
```

## Common Patterns

### Single Skill Repository

```
my-skill-repo/
├── .claude-plugin/
│   └── marketplace.json
└── skills/
    └── my-skill/
        └── SKILL.md
```

### Multi-Skill Collection

```
skills-collection/
├── .claude-plugin/
│   └── marketplace.json
└── skills/
    ├── skill-a/
    │   └── SKILL.md
    ├── skill-b/
    │   └── SKILL.md
    └── skill-c/
        └── SKILL.md
```

Group related skills in a single plugin, or create multiple plugins for categories:

```json
{
  "plugins": [
    {
      "name": "document-skills",
      "skills": ["./skills/pdf", "./skills/docx"]
    },
    {
      "name": "dev-skills",
      "skills": ["./skills/git-helper"]
    }
  ]
}
```
