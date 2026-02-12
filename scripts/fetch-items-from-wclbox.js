#!/usr/bin/env node

/**
 * Fetch and cache item data from TitanReforged API for all Altasloot items
 * Data source: https://wlk.scarlet5.com/
 * Run this periodically to keep item database up-to-date
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const url = require('url');

const DATA_OUTPUT_PATH = path.join(__dirname, '../data');
const CACHE_FILE = path.join(DATA_OUTPUT_PATH, 'items-cache.json');

// Ensure data directory exists
if (!fs.existsSync(DATA_OUTPUT_PATH)) {
  fs.mkdirSync(DATA_OUTPUT_PATH, { recursive: true });
}

/**
 * Make HTTP GET request
 */
function httpGet(urlString, maxRetries = 3) {
  return new Promise((resolve, reject) => {
    const attemptFetch = (retryCount) => {
      const parsedUrl = new url.URL(urlString);
      const options = {
        hostname: parsedUrl.hostname,
        path: parsedUrl.pathname + parsedUrl.search,
        method: 'GET',
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        },
        timeout: 5000,
      };

      https
        .request(options, (res) => {
          let data = '';
          res.on('data', (chunk) => {
            data += chunk;
          });
          res.on('end', () => {
            if (res.statusCode === 200) {
              try {
                resolve(JSON.parse(data));
              } catch (e) {
                // Try parsing as text if JSON fails
                resolve({ raw: data });
              }
            } else if (retryCount < maxRetries) {
              console.log(`  Retry ${retryCount + 1}/${maxRetries} for status ${res.statusCode}`);
              setTimeout(() => attemptFetch(retryCount + 1), 1000 * (retryCount + 1));
            } else {
              reject(new Error(`HTTP ${res.statusCode}`));
            }
          });
        })
        .on('error', (error) => {
          if (retryCount < maxRetries) {
            console.log(`  Retry ${retryCount + 1}/${maxRetries} after error: ${error.message}`);
            setTimeout(() => attemptFetch(retryCount + 1), 1000 * (retryCount + 1));
          } else {
            reject(error);
          }
        })
        .on('timeout', () => {
          if (retryCount < maxRetries) {
            console.log(`  Retry ${retryCount + 1}/${maxRetries} after timeout`);
            setTimeout(() => attemptFetch(retryCount + 1), 1000 * (retryCount + 1));
          } else {
            reject(new Error('Request timeout'));
          }
        })
        .end();
    };
    attemptFetch(0);
  });
}

/**
 * Parse Lua file to extract ItemData
 */
function parseLuaFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const items = new Set();

  // Extract ItemData block
  const itemDataMatch = content.match(/\["ItemData"\]\s*=\s*\{([\s\S]*?)\n\}/);
  if (!itemDataMatch) {
    console.warn(`No ItemData found in ${filePath}`);
    return items;
  }

  const itemBody = itemDataMatch[1];
  const lineRegex = /\[(\d+)\]\s*=/g;
  let match;

  while ((match = lineRegex.exec(itemBody)) !== null) {
    const itemId = parseInt(match[1], 10);
    items.add(itemId);
  }

  return items;
}

/**
 * Fetch item info from TitanReforged API (wlk.scarlet5.com)
 */
async function fetchItemFromTitanReforged(itemId) {
  try {
    const response = await httpGet(
      `https://wlk.scarlet5.com/trt/mini/db/item/getItemDetail?itemId=${itemId}`
    );
    
    if (response && response.data) {
      const item = response.data;
      return {
        id: itemId,
        name: item.name || item.itemName || null,
        quality: item.quality || item.itemQuality || null,
        itemLevel: item.itemLevel || item.level || null,
        classes: item.classes || item.applicableClasses || null,
        slot: item.slot || item.itemSlot || null,
        source: 'titan-reforged',
      };
    }
    
    return {
      id: itemId,
      name: null,
      quality: null,
      itemLevel: null,
      source: 'failed',
    };
  } catch (e) {
    console.warn(`  Could not fetch item ${itemId}: ${e.message}`);
    return {
      id: itemId,
      name: null,
      quality: null,
      itemLevel: null,
      source: 'failed',
    };
  }
}

/**
 * Main execution
 */
async function main() {
  try {
    console.log('🔍 Parsing Altasloot data files...\n');

    // Get all Altasloot paths
    const altaslootPath = path.join(__dirname, '../Altasloot/AtlasLootMY_Data');
    
    // Parse all source files
    const sourceFiles = [
      { file: 'source.lua', version: 'classic' },
      { file: 'source-tbc.lua', version: 'tbc' },
      { file: 'source-wrath.lua', version: 'wrath' },
    ];

    const allItemIds = new Set();

    for (const source of sourceFiles) {
      const filePath = path.join(altaslootPath, source.file);
      if (fs.existsSync(filePath)) {
        console.log(`📖 Parsing ${source.file}...`);
        const items = parseLuaFile(filePath);
        console.log(`   Found ${items.size} items\n`);
        items.forEach(id => allItemIds.add(id));
      }
    }

    const itemArray = Array.from(allItemIds).sort((a, b) => a - b);
    console.log(`✅ Total unique items: ${itemArray.length}\n`);

    // Load existing cache
    let cache = {};
    if (fs.existsSync(CACHE_FILE)) {
      try {
        cache = JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8'));
        console.log(`📋 Loaded existing cache with ${Object.keys(cache).length} items\n`);
      } catch (e) {
        console.log('⚠️  Could not load existing cache, starting fresh\n');
      }
    }

    // Fetch items that are not in cache
    const itemsToFetch = itemArray.filter(id => !cache[id]);
    console.log(`📥 Fetching ${itemsToFetch.length} items from TitanReforged API...`);
    console.log('(This may take a while, please be patient)\n');

    const BATCH_SIZE = 5;
    const BATCH_DELAY = 1500; // ms between batches

    for (let i = 0; i < itemsToFetch.length; i += BATCH_SIZE) {
      const batch = itemsToFetch.slice(i, i + BATCH_SIZE);
      const batchNum = Math.floor(i / BATCH_SIZE) + 1;
      const totalBatches = Math.ceil(itemsToFetch.length / BATCH_SIZE);

      process.stdout.write(`   [${batchNum}/${totalBatches}] Fetching items: `);

      const promises = batch.map(async (itemId) => {
        try {
          const data = await fetchItemFromTitanReforged(itemId);
          cache[itemId] = data;
          process.stdout.write('.');
        } catch (e) {
          console.error(`Error fetching item ${itemId}:`, e.message);
        }
      });

      await Promise.all(promises);
      console.log();

      // Delay between batches to avoid rate limiting
      if (i + BATCH_SIZE < itemsToFetch.length) {
        await new Promise(resolve => setTimeout(resolve, BATCH_DELAY));
      }
    }

    // Save cache
    fs.writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2));
    console.log(`\n💾 Saved cache with ${Object.keys(cache).length} items to: ${CACHE_FILE}\n`);

    // Generate statistics
    const withNames = Object.values(cache).filter(item => item.name).length;
    const withQuality = Object.values(cache).filter(item => item.quality).length;
    const successful = Object.values(cache).filter(item => item.source !== 'failed').length;

    console.log('📊 Statistics:');
    console.log(`   Total items: ${Object.keys(cache).length}`);
    console.log(`   Items with names: ${withNames} (${((withNames / Object.keys(cache).length) * 100).toFixed(1)}%)`);
    console.log(`   Items with quality: ${withQuality} (${((withQuality / Object.keys(cache).length) * 100).toFixed(1)}%)`);
    console.log(`   Successfully fetched: ${successful} (${((successful / Object.keys(cache).length) * 100).toFixed(1)}%)\n`);

    console.log('✅ Done! Your item database is now ready.');
    console.log('   Open index.html in your browser to view the loot table.');

  } catch (err) {
    console.error('❌ Error:', err.message);
    process.exit(1);
  }
}

main();
