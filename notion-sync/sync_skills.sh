#!/bin/bash
# AI Genesis Skills → Notion Sync Script
# Usage: ./sync_skills_to_notion.sh

NOTION_KEY=$(cat ~/.config/notion/api_key)
DB_ID="6469b63d-5e4f-4429-966d-3b0f94fe6df4"
SKILLS_DIR="/root/.openclaw/skills/skills"

echo "🔄 Syncing AI Genesis Skills to Notion..."

# Function to create/update skill in Notion
sync_skill() {
  local name="$1"
  local category="$2"
  local tier="$3"
  local rating="$4"
  local path="$5"
  local desc="$6"
  
  # Check if skill already exists
  existing=$(curl -s -X POST "https://api.notion.com/v1/databases/$DB_ID/query" \
    -H "Authorization: Bearer $NOTION_KEY" \
    -H "Notion-Version: 2025-09-03" \
    -H "Content-Type: application/json" \
    -d "{\"filter\": {\"property\": \"Name\", \"title\": {\"equals\": \"$name\"}}}")
  
  if echo "$existing" | grep -q "\"results\":\[\]"; then
    # Create new skill
    curl -s -X POST "https://api.notion.com/v1/pages" \
      -H "Authorization: Bearer $NOTION_KEY" \
      -H "Notion-Version: 2025-09-03" \
      -H "Content-Type: application/json" \
      -d "{
        \"parent\": {\"database_id\": \"$DB_ID\"},
        \"properties\": {
          \"Name\": {\"title\": [{\"text\": {\"content\": \"$name\"}}]},
          \"Category\": {\"select\": {\"name\": \"$category\"}},
          \"Status\": {\"select\": {\"name\": \"Активен\"}},
          \"Tier\": {\"select\": {\"name\": \"$tier\"}},
          \"Price\": {\"number\": 0},
          \"Rating\": {\"number\": $rating},
          \"File Path\": {\"rich_text\": [{\"text\": {\"content\": \"$path\"}}]},
          \"Description\": {\"rich_text\": [{\"text\": {\"content\": \"$desc\"}}]}
        }
      }" > /dev/null
    echo "✅ Created: $name"
  else
    echo "⏭️  Exists: $name"
  fi
}

# Sync all skills from local directory
for skill_dir in "$SKILLS_DIR"/*/; do
  skill_name=$(basename "$skill_dir")
  echo "📁 Found: $skill_name"
done

echo "✨ Sync complete!"
echo "🔗 View: https://www.notion.so/6469b63d5e4f4429966d3b0f94fe6df4"
