const fs = require('fs');
const readline = require('readline');

const rl = readline.createInterface({
  input: fs.createReadStream('C:\\Users\\Sam\\.gemini\\antigravity\\brain\\423a7e7c-328c-4da5-b6e6-81eca21f020c\\.system_generated\\logs\\transcript.jsonl'),
  crlfDelay: Infinity
});

rl.on('line', (line) => {
  if (line.includes('"step_index":3984') || line.includes('"step_index":3985')) {
    try {
      const obj = JSON.parse(line);
      if (obj.source === 'USER_EXPLICIT') {
        const lines = obj.content.split('\n');
        console.log("Total lines:", lines.length);
        lines.forEach((l, idx) => console.log(`${idx}: ${l}`));
      }
    } catch(e) {}
  }
});
