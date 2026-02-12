#!/usr/bin/env node

/**
 * Parse Altasloot Lua files and fetch item data from wclbox.com
 * Generates JSON data files with item mappings
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const ALTASLOOT_PATH = path.join(__dirname, '../Altasloot/AtlasLootMY_Data');
const DATA_OUTPUT_PATH = path.join(__dirname, '../data');

// Ensure data directory exists
if (!fs.existsSync(DATA_OUTPUT_PATH)) {
  fs.mkdirSync(DATA_OUTPUT_PATH, { recursive: true });
}

/**
 * Parse Lua file to extract ItemData
 */
function parseLuaFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const items = new Map();

  // Extract ItemData block
  const itemDataMatch = content.match(/\["ItemData"\]\s*=\s*\{([\s\S]*?)\n\}/);
  if (!itemDataMatch) {
    console.warn(`No ItemData found in ${filePath}`);
    return items;
  }

  const itemBody = itemDataMatch[1];
  const lineRegex = /\[(\d+)\]\s*=\s*(\{[\s\S]*?\}),?/g;
  let match;

  while ((match = lineRegex.exec(itemBody)) !== null) {
    const itemId = parseInt(match[1], 10);
    items.set(itemId, {
      id: itemId,
      name: null, // Will be fetched from wclbox
      quality: null,
      itemLevel: null,
    });
  }

  return items;
}

/**
 * Fetch item info from wclbox API
 */
function fetchItemFromWclbox(itemId) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'www.wclbox.com',
      port: 443,
      path: `/api/games/1/db?id=${itemId}`, // Adjust path based on actual API
      method: 'GET',
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      },
    };

    https
      .request(options, (res) => {
        let data = '';
        res.on('data', (chunk) => {
          data += chunk;
        });
        res.on('end', () => {
          try {
            const json = JSON.parse(data);
            resolve(json);
          } catch (e) {
            reject(e);
          }
        });
      })
      .on('error', reject)
      .end();
  });
}

/**
 * Main execution
 */
async function main() {
  try {
    console.log('🔍 Parsing Altasloot data files...\n');

    // Parse all source files
    const sourceFiles = [
      { file: 'source.lua', version: 'classic' },
      { file: 'source-tbc.lua', version: 'tbc' },
      { file: 'source-wrath.lua', version: 'wrath' },
    ];

    const allItems = new Map();

    for (const source of sourceFiles) {
      const filePath = path.join(ALTASLOOT_PATH, source.file);
      if (fs.existsSync(filePath)) {
        console.log(`📖 Parsing ${source.file}...`);
        const items = parseLuaFile(filePath);
        console.log(`   Found ${items.size} items\n`);

        // Merge into allItems
        items.forEach((value, key) => {
          allItems.set(key, { ...value, version: source.version });
        });
      }
    }

    console.log(`✅ Total unique items: ${allItems.size}\n`);

    // Convert to array for easier processing
    const itemArray = Array.from(allItems.values());

    // Save raw item list as JSON
    const outputPath = path.join(DATA_OUTPUT_PATH, 'items-raw.json');
    fs.writeFileSync(outputPath, JSON.stringify(itemArray, null, 2));
    console.log(`💾 Saved raw items list to: ${outputPath}\n`);

    console.log('✨ Done! Now you can fetch item details from wclbox.com');
    console.log('Next steps:');
    console.log('1. Update HTML to fetch item names from wclbox.com when needed');
    console.log('2. Or create a server-side API to batch fetch from wclbox.com');
  } catch (err) {
    console.error('❌ Error:', err.message);
    process.exit(1);
  }
}

main();
