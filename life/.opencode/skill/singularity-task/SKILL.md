---
name: singularity-task
description: Manage tasks, projects, habits, and notebooks using the Singularity MCP tools. Use this skill when working with task management, creating or updating projects, managing habits, creating notebooks, or any operations involving tasks, to-do items, reminders, and project organization. Trigger when user mentions tasks, projects, habits, notebooks, to-do lists, reminders, or scheduling activities.
---

# Singularity Task Management

## Overview

This skill enables task management, project organization, habit tracking, and notebook creation using Singularity MCP tools. It provides comprehensive guidelines for working with time zones, projects, tasks, notebooks, and habits.

## Time Zone Configuration

**CRITICAL:** All dates and times use GMT+3 timezone unless user specifies otherwise.

- Default timezone: GMT+3
- When time is specified in conversation, interpret it as GMT+3
- Replace GMT+3 with user's actual timezone if needed

## Working with Projects

### Creating Projects

When creating projects, follow these requirements:

**Project Emoji Format:**
- Must be hexadecimal Unicode code **without prefix**
- Format: `"1f49e"` (hexadecimal string only)
- NOT Unicode format: `"U+1F49E"`
- NOT the emoji itself: `"💞"`

Examples:
- 💞 = `"1f49e"`
- 🎯 = `"1f3af"`
- 🚀 = `"1f680"`
- ⭐️ = `"2b50"`

### Adding Tasks to Projects

**Default behavior:** Always place new tasks in the project's base task group unless explicitly specified otherwise.

### Project Settings

**`showInBasket` field:** Do not set this field unless specifically requested by user.

### Project Notes

**Note content format:** Must be in Delta format
- Pass operations array directly: `[{},...]`
- NOT wrapped format: `{"ops":[{},...]}`
- **Critical:** Last insert in Delta must always end with line break

Example:
```json
[
  {"insert": "First line\n"},
  {"insert": "Second line\n"}
]
```

## Working with Tasks

### Date and Time Handling

**Timezone:** Use GMT+3 for all task dates and times.

**Time precision:**
- `useTime: false` - Start time is date-only (no specific hour)
- `useTime: true` - Start time includes specific time in GMT+3

### Notifications

**Format:**
```json
{
  "notifies": [60, 15],      // Array in minutes, highest to lowest
  "notify": 1,               // Main notification enabled
  "alarmNotify": true        // Alarm (false by default)
}
```

**Rules:**
- `notifies` array: Minutes before event, ordered highest to lowest
- Example: `[60, 15]` = notifications at 1 hour and 15 minutes before
- `notify: 1` enables main notification
- `alarmNotify: true` only when explicitly requested (default: false)

### Task Priority

**Default priority:** `1`

### Date Interpretation

**Technical fields:**
- `modifiedDate` - Last change timestamp (NOT completion time)
- `createdDate` - Original creation timestamp
- Large difference between `modifiedDate` and `createdDate` indicates task was rescheduled

## Notebooks and Note-like Entries

### Creating Notebooks

**When user asks for notebook:** Create project with `notebook` attribute set to true.

### Adding Items to Notebooks

**Default behavior:** Create task with `isNote` attribute when adding items to notebook.

### Tasks vs Notes

**Decision tree:**
1. User explicitly asks for task → Create task (without `isNote`)
2. User adds item to notebook → Create task with `isNote` attribute
3. User wants note in non-notebook project → Create task with `isNote` attribute

## Working with Habits

### Habit Colors

**Format:** Pass color as string from acceptable values, NOT color code.

**Acceptable values:**
- `"red"`
- `"pink"`
- `"purple"`
- `"deepPurple"`
- `"indigo"`
- `"lightBlue"`
- `"cyan"`
- `"teal"`
- `"green"`
- `"lightGreen"`
- `"lime"`
- `"yellow"`
- `"amber"`
- `"orange"`
- `"deepOrange"`
- `"brown"`
- `"grey"`
- `"blueGrey"`

### Habit Status

**Active habits:** Status `0`

**Always create habits with:** `status: 0`

## Common Workflows

### Example: Creating a Project with Tasks

```
User: "Create a project called 'Website Redesign' with tasks for design, development, and testing"

Steps:
1. Create project with name "Website Redesign"
2. Set appropriate emoji (e.g., "1f4bb" for 💻)
3. Add tasks to base task group:
   - Design task
   - Development task
   - Testing task
4. Set priority 1 for all tasks (default)
5. Use GMT+3 for any date/time specifications
```

### Example: Creating a Notebook

```
User: "Create a research notebook for my AI project"

Steps:
1. Create project with name "AI Research"
2. Set notebook: true
3. Set appropriate emoji (e.g., "1f4d3" for 📓)
4. When adding entries, create tasks with isNote: true
```

### Example: Creating a Habit

```
User: "Create a daily reading habit"

Steps:
1. Create habit with appropriate name
2. Set color from acceptable list (e.g., "blue")
3. Set status: 0 (active)
```