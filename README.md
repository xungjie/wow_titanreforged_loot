# WoW Loot Database - Setup Guide

This project displays WoW loot drops from Altasloot with item details fetched from TitanReforged database (wlk.scarlet5.com).

## Project Structure

```
wow_Loot/
├── index.html                 # Main web interface
├── Altasloot/                # Local Altasloot addon files
│   └── AtlasLootMY_Data/
│       ├── source.lua         # Classic/Vanilla items
│       ├── source-tbc.lua     # Burning Crusade items
│       └── source-wrath.lua   # Wrath of the Lich King items
├── data/                     # Generated data files
│   └── items-cache.json      # Cached item data from TitanReforged
└── scripts/                  # Utility scripts
    ├── fetch-items-from-wclbox.js  # Fetch script (name kept for compatibility)
    └── parse-altasloot.js
```

## Setup Instructions

### 1. Install Node.js

Download and install Node.js from https://nodejs.org/

### 2. Generate Item Database

**Option A: Click the batch file (Windows)**
```
Double-click: update-items.bat
```

**Option B: Run from command line**
```bash
cd scripts
node fetch-items-from-wclbox.js
```

This will:
- Parse all Altasloot Lua files to extract item IDs
- Fetch item details from TitanReforged API (wlk.scarlet5.com)
- Cache the data locally in `data/items-cache.json`
- Display statistics about the fetched data

**Note:** First run may take 10-15 minutes (200k+ items). Subsequent runs only fetch new items.

### 3. View the Loot Table

Open `index.html` in your browser:
- See all WoW loot drops organized by instance/boss
- Search by item name
- Filter by class
- Filter by instance/raid
- Click item names to view details on TitanReforged

## Features

✅ **Offline Item Database** - Uses local TitanReforged cache (fast loading)  
✅ **Full Altasloot Coverage** - 200k+ items across all expansions  
✅ **Fast Search & Filter** - Instant search and multi-filter support  
✅ **Chinese UI** - Complete Chinese localization  
✅ **Quality Levels** - Color-coded item rarity (poor/common/uncommon/rare/epic/legendary)  
✅ **TitanReforged Integration** - Direct links to item details  

## Data Sources

- **Loot Data**: Altasloot addon (local Lua files)
- **Item Details**: TitanReforged API (wlk.scarlet5.com)
- **Game Versions**: Classic, Burning Crusade, Wrath of the Lich King

## Usage

### Update Item Data

To refresh the item cache from TitanReforged:

**Windows:**
```bash
double-click update-items.bat
```

**Command line:**
```bash
cd scripts
node fetch-items-from-wclbox.js
```

### Parse Only (No Fetching)

To just parse Altasloot and generate item ID list:

```bash
cd scripts
node parse-altasloot.js
```

## Troubleshooting

### "Cannot find module" error

This shouldn't happen - the scripts only use Node.js built-in modules. 
Check that Node.js is installed correctly by running:
```bash
node --version
```

### Slow fetch speed

The script intentionally rate-limits requests to TitanReforged API to avoid overloading the server. This is normal behavior.

Items showing "物品ID XXX"

Some items may not be found in TitanReforged database. The script will retry failed items in subsequent runs.

## API Integration

The HTML fetches item names on-demand when needed:
- Caches results in browser memory
- Falls back to item ID if name not available
- Uses TitanReforged links for item lookups
- Prioritizes local cache file for instant loading

## Performance

- **Initial Load**: ~1-2 seconds (parsing Altasloot files + loading cache)
- **Search**: Instant local filtering
- **Item Links**: Direct to TitanReforged database

## Browser Compatibility

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Requires modern browser with ES6 support

## License

Data sourced from Altasloot addon and TitanReforged database.

## Support

For issues with:
- **Altasloot data**: Check Altasloot addon documentation
- **TitanReforged**: Visit wlk.scarlet5.com
- **This tool**: Review scripts and HTML code
