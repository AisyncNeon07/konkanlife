---
name: skill-catalog
description: Search, reference, and import new skills from the awesome-agent-skills catalog into this workspace
---

# Awesome Agent Skills Catalog & Import Guide

## Overview

This workspace is paired with the `awesome-agent-skills` curated repository (located at `../awesome-agent-skills/README.md`), containing over 1,400+ curated agent skills across official teams (Anthropic, Google, VoltAgent, TestMu AI, Supabase, Neon, Microsoft, OpenAI, etc.) and the community.

## How to Add a New Skill from the Catalog

1. **Browse Catalog**: Check `awesome-agent-skills/README.md` for existing skills in your domain (e.g. testing, auth, devops, database).
2. **Create Skill Folder**: Inside `konkan/.agent/skills/<skill-name>/`
3. **Add `SKILL.md`**: Create `SKILL.md` with:
   ```markdown
   ---
   name: <skill-name>
   description: <When and what the skill does (third-person)>
   ---

   # Skill Title

   ## Step-by-step instructions and patterns...
   ```
4. **Antigravity Automatic Discovery**: Antigravity automatically detects any new skill directory inside `.agent/skills/` on your next query.
