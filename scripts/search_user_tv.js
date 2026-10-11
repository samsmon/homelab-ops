const fs = require('fs');
const readline = require('readline');

const rl = readline.createInterface({
  input: fs.createReadStream('C:\\Users\\Sam\\.gemini\\antigravity\\brain\\423a7e7c-328c-4da5-b6e6-81eca21f020c\\.system_generated\\logs\\transcript.jsonl'),
  crlfDelay: Infinity
});

rl.on('line', (line) => {
  if (line.includes('"source":"USER_EXPLICIT"') && (line.includes('TV') || line.includes('Anime') || line.includes('diluar') || line.includes('di luar'))) {
    try {
      const obj = JSON.parse(line);
      console.log('=== Step ' + obj.step_index + ' ===');
      console.log(obj.content);
    } catch(e) {}
  }
});
