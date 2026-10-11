const fs = require('fs');
const readline = require('readline');

const rl = readline.createInterface({
  input: fs.createReadStream('C:\\Users\\Sam\\.gemini\\antigravity\\brain\\423a7e7c-328c-4da5-b6e6-81eca21f020c\\.system_generated\\logs\\transcript.jsonl'),
  crlfDelay: Infinity
});

rl.on('line', (line) => {
  if (line.includes('"step_index":296') || line.includes('"step_index":297')) {
    try {
      const obj = JSON.parse(line);
      console.log(`=== Step ${obj.step_index} (${obj.source} ${obj.type}) ===`);
      if (obj.content) console.log(obj.content.substring(0, 1000));
    } catch(e) {}
  }
});
