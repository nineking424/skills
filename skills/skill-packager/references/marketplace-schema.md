# Marketplace Schema Reference

Complete schema documentation for Claude Code marketplace.json files.

## Full Schema Structure

```json
{
  "name": "<marketplace-identifier>",
  "owner": {
    "name": "<owner display name>",
    "email": "<contact email>"
  },
  "metadata": {
    "description": "<marketplace description>",
    "version": "<semantic version>"
  },
  "plugins": [
    {
      "name": "<plugin-identifier>",
      "description": "<plugin description>",
      "source": "<source path or URL>",
      "strict": <boolean>,
      "skills": [
        "<relative path to skill>"
      ]
    }
  ]
}
```

## Field Reference

### Root Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Marketplace identifier. Use hyphen-case (e.g., `my-skills`). Must be unique. |
| `owner` | Yes | object | Owner information with `name` and `email` fields. |
| `metadata` | No | object | Optional metadata including `description` and `version`. |
| `plugins` | Yes | array | Array of plugin configurations. |

### Owner Object

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Owner display name. |
| `email` | Yes | string | Contact email address. |

### Metadata Object

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `description` | No | string | Brief description of the marketplace. |
| `version` | No | string | Semantic version (e.g., `1.0.0`). |

### Plugin Object

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Plugin group identifier. |
| `description` | No | string | What capabilities this plugin provides. |
| `source` | Yes | string/object | Where to find the skills (see Source Types below). |
| `strict` | No | boolean | If `true`, all skills must load successfully. Default: `false`. |
| `skills` | Yes | array | Array of relative paths to skill directories. |

## Source Types

### Local Source (Same Repository)

Use relative paths for skills in the same repository:

```json
{
  "source": "./",
  "skills": [
    "./skills/my-skill",
    "./skills/another-skill"
  ]
}
```

### GitHub Repository Source

Reference skills from a GitHub repository:

```json
{
  "source": {
    "source": "github",
    "repo": "owner/repository"
  },
  "skills": [
    "skills/skill-name"
  ]
}
```

### Git URL Source

Reference skills from any Git repository:

```json
{
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/skills.git"
  },
  "skills": [
    "skills/skill-name"
  ]
}
```

## Common Patterns

### Single Skill Repository

One repository containing one skill:

```json
{
  "name": "my-skill",
  "owner": {
    "name": "Developer Name",
    "email": "dev@example.com"
  },
  "metadata": {
    "description": "A single skill marketplace",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "my-skill",
      "description": "My awesome skill",
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/my-skill"
      ]
    }
  ]
}
```

### Multi-Skill Collection

Repository with multiple skills grouped by category:

```json
{
  "name": "skill-collection",
  "owner": {
    "name": "Team Name",
    "email": "team@example.com"
  },
  "metadata": {
    "description": "Collection of productivity skills",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "document-skills",
      "description": "Document processing capabilities",
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/pdf-processor",
        "./skills/docx-editor"
      ]
    },
    {
      "name": "dev-skills",
      "description": "Development workflow tools",
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/git-helper",
        "./skills/code-reviewer"
      ]
    }
  ]
}
```

### External Skills Reference

Aggregate skills from multiple external repositories:

```json
{
  "name": "aggregated-skills",
  "owner": {
    "name": "Aggregator",
    "email": "admin@example.com"
  },
  "plugins": [
    {
      "name": "external-tools",
      "description": "Skills from external repos",
      "source": {
        "source": "github",
        "repo": "org/skill-repo"
      },
      "skills": [
        "skills/tool-a",
        "skills/tool-b"
      ]
    }
  ]
}
```

## Validation Rules

1. **name**: Must be hyphen-case (lowercase letters, digits, hyphens)
2. **owner.email**: Must be a valid email format
3. **plugins**: Must contain at least one plugin
4. **skills**: Paths must be valid relative paths
5. **version**: Should follow semantic versioning (MAJOR.MINOR.PATCH)

## User Commands

Users interact with marketplaces using these commands:

```bash
# Add a marketplace
/plugin marketplace add <source>

# List configured marketplaces
/plugin marketplace list

# Update marketplace metadata
/plugin marketplace update

# Remove a marketplace
/plugin marketplace remove <name>

# Install skill from marketplace
/plugin install <skill-name>@<marketplace-name>
```
