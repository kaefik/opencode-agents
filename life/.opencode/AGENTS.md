# Singularity Task Management

When working with tasks, projects, habits, and notebooks, use the `singularity` MCP tools.

## Time Zone Configuration

⚠️ **ВАЖНО:** Замените GMT+3 на ваш часовой пояс!

- Use GMT+3 time zone for all task dates and times
- If time is specified in chat, consider it to be in GMT+3

## Working with Projects

1. When adding tasks to a project, always place the task in the project's base task group, unless explicitly specified which other group to add the task to.

2. Project emoji must be specified as hexadecimal Unicode code without prefix:
   - Format: `"1f49e"` (hexadecimal string)
   - NOT Unicode format: `"U+1F49E"`
   - NOT the emoji itself: `"💞"`
   - Examples:
     - 💞 = `"1f49e"`
     - 🎯 = `"1f3af"`
     - 🚀 = `"1f680"`
     - ⭐️ = `"2b50"`

3. Do not set the `showInBasket` field unless specifically asked.

4. Note content must be in Delta format - pass the operations array directly `[{},...]`, NOT `{"ops":[{},...]}`
   - The last insert inside a Delta must always end with a line break

## Working with Tasks

1. For task date and time, use GMT+3 time zone. If time is specified in chat, consider it GMT+3.

2. Notifications format:
   - `notifies: [60, 15]` - array in minutes, highest to lowest (1 hour and 15 minutes in advance)
   - `notify: 1` - main notification enabled
   - `alarmNotify: true` - alarm enabled (false by default, enable only if explicitly specified)

3. Default task priority is `1`.

4. Time handling:
   - `useTime: false` - start time is just a date without specific hour
   - `useTime: true` - start time is real time in GMT+3

5. Date interpretation:
   - Large difference between `modifiedDate` and `createdDate` indicates task was rescheduled
   - `modifiedDate` is technical field of last change, NOT completion time

## Notebooks and Note-like Entries

1. When asked to create a notebook → create a project with `notebook` attribute
2. When adding items to notebook → create task with `isNote` attribute by default
3. If asked to create a task → create the task
4. To add note to non-notebook project → create task with `isNote` attribute

## Working with Habits

1. Pass habit color as string from acceptable values, NOT color code:
   - Acceptable: `"red"`, `"pink"`, `"purple"`, `"deepPurple"`, `"indigo"`, `"lightBlue"`, `"cyan"`, `"teal"`, `"green"`, `"lightGreen"`, `"lime"`, `"yellow"`, `"amber"`, `"orange"`, `"deepOrange"`, `"brown"`, `"grey"`, `"blueGrey"`

2. Active habits have status `0`. Always create habits with status `0`.
