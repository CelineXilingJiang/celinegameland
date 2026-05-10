# 🎮 Celine's Game Land

A local game hub built for Celine and family — two fun, browser-based games served from a single Python server.

## Games

### 🍜 Food Bowl Rush
A multiplayer racing game where 1–6 players pick a food fighter and race to the bowl. Supports Chinese characters (中文 OK). Scores are saved server-side.

### ⭐ Number Bond Star
A solo math game where players answer number bond questions to collect stars and climb the leaderboard. Four difficulty levels: Baby → Lion → Rocket → Diamond.

## How to Run

**Double-click** `start.command` (macOS) — it starts the server and opens the hub in your browser automatically.

Or run manually:
```bash
python3 server.py
```

Then open [http://localhost:8765](http://localhost:8765).

## Players / Profiles

Six built-in profiles: Celine 👧, Eileen 👩, Tao 👨, Kunyan 🧑, 爷爷 👴, 奶奶 👵. Custom profiles can be added in-game.

## Structure

```
celinegameland/
├── index.html       # Game hub (landing page with leaderboard)
├── server.py        # Combined HTTP server (port 8765)
├── start.command    # One-click launcher for macOS
└── PUSH_LOG.md      # Auto-generated push history
```

The server also routes to sibling game directories:
- `../food-bowl-rush/` — Food Bowl Rush game files + `scores.json`
- `../math-bond-star/` — Number Bond Star game files

## Tech

- Pure HTML/CSS/JS frontend — no frameworks
- Python 3 stdlib HTTP server — no dependencies
- Scores stored in `scores.json` (Food Bowl Rush) and `localStorage` (Math Bond Star)

---

*Made with ♥ by Tao & Celine · Powered by Claude Code*
