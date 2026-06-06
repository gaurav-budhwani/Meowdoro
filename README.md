# Meowdoro

![Meowdoro](assets/screenshot.png)

**Meowdoro** is an interactive desktop companion designed specifically for developers. It lives quietly on your screen, reacting to your keystrokes and keeping you on track. With built-in Pomodoro timers, customizable reminders, and deep integration with AI agents like Claude Code and Cursor, it transforms your workspace into a more engaging and productive environment.

## Features

- **Desktop Pet** that follows your cursor, reacts to your typing, and stretches on a schedule.
- **Pomodoro Timer** with focus and break intervals to help you manage your productivity.
- **Customizable Reminders** that trigger pings or speech bubbles exactly when you need them.
- **AI Agent Integration** — Hooks directly into Claude Code, Antigravity (Gemini), and Cursor to let the pet know when your agents are working or waiting for approval.
- **Pattern Editor** for customizing your pet's colors, spots, and odd eyes.
- **Video Sharing** to easily record and show off your productivity sessions.

## Quick Start

To run the project locally in development mode:

```bash
npm install
npm start
```

### Build Scripts

| Command | Description |
| --- | --- |
| `npm start` | Run the app in development mode. |
| `npm run smoke` | Run a smoke test to ensure the app boots successfully. |
| `npm run dist:mac` | Build an installable `.dmg` for macOS. |
| `npm run dist:win` | Build an installable `.exe` for Windows. |
| `npm run dist:linux` | Build an `AppImage` for Linux. |

## AI-Agent Hook Integration

Meowdoro seamlessly tracks agent states. The app integrates with the following agent workflows:

| Agent | Settings file |
| --- | --- |
| **Claude Code** | `~/.claude/settings.json` |
| **Antigravity (Gemini)** | `~/.gemini/config/hooks.json` |
| **Cursor** | `~/.cursor/hooks.json` |

## Permissions

- **macOS:** You will need to grant **Accessibility** permissions (and sometimes **Input Monitoring**) in `System Settings → Privacy & Security` for the pet to react to your global typing.
- **Windows:** Security software may block the global keyboard hook. Allow the application if prompted.
