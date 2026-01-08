#!/usr/bin/env node
/**
 * Skill Evaluation Engine
 * Analyzes user prompts and matches them against skill definitions
 * Outputs activation suggestions when relevant skills are found
 * 
 * Adapted from ChrisWiles/claude-code-showcase for Unified_System_Core
 */

const fs = require('fs');
const path = require('path');

// Read configuration
const configPath = path.join(__dirname, 'skill-rules.json');
let config = {
  version: "1.0",
  minConfidenceScore: 3,
  maxSkillsToShow: 5,
  directoryMappings: {},
  skills: {}
};

try {
  if (fs.existsSync(configPath)) {
    config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  }
} catch (e) {
  // Use defaults if config can't be loaded
}

/**
 * Extract file paths from user input
 * Matches common file extensions and path patterns
 */
function extractFilePaths(input) {
  const patterns = [
    // Explicit file paths with extensions
    /(?:^|\s|["'`])([./\w-]+\.(?:tsx?|jsx?|py|sh|md|json|ya?ml|gql|graphql|sql|css|scss|html))\b/gi,
    // Directory paths
    /(?:^|\s|["'`])([./\w-]+\/[./\w-]+)\b/g,
  ];
  
  const paths = new Set();
  for (const pattern of patterns) {
    let match;
    while ((match = pattern.exec(input)) !== null) {
      paths.add(match[1]);
    }
  }
  return Array.from(paths);
}

/**
 * Check if input matches a regex pattern
 */
function matchesPattern(input, pattern) {
  try {
    const regex = new RegExp(pattern, 'i');
    return regex.test(input);
  } catch {
    return false;
  }
}

/**
 * Check if any extracted path matches a glob-like pattern
 */
function matchesGlob(paths, pattern) {
  // Convert simple glob to regex
  const regexPattern = pattern
    .replace(/\*/g, '.*')
    .replace(/\?/g, '.');
  
  try {
    const regex = new RegExp(regexPattern, 'i');
    return paths.some(p => regex.test(p));
  } catch {
    return false;
  }
}

/**
 * Evaluate a skill against the input
 * Returns a confidence score based on matches
 */
function evaluateSkill(skillName, skillDef, input, filePaths) {
  let score = 0;
  const matches = [];
  
  // Check keywords (score: 2 each)
  if (skillDef.keywords) {
    for (const keyword of skillDef.keywords) {
      if (input.toLowerCase().includes(keyword.toLowerCase())) {
        score += 2;
        matches.push(`keyword: "${keyword}"`);
      }
    }
  }
  
  // Check keyword patterns (score: 3 each)
  if (skillDef.keywordPatterns) {
    for (const pattern of skillDef.keywordPatterns) {
      if (matchesPattern(input, pattern)) {
        score += 3;
        matches.push(`pattern: "${pattern}"`);
      }
    }
  }
  
  // Check path patterns (score: 4 each)
  if (skillDef.pathPatterns && filePaths.length > 0) {
    for (const pattern of skillDef.pathPatterns) {
      if (matchesGlob(filePaths, pattern)) {
        score += 4;
        matches.push(`path: "${pattern}"`);
      }
    }
  }
  
  // Check directory mappings (score: 5 each)
  if (config.directoryMappings) {
    for (const [dir, mappedSkill] of Object.entries(config.directoryMappings)) {
      if (mappedSkill === skillName && filePaths.some(p => p.includes(dir))) {
        score += 5;
        matches.push(`directory: "${dir}"`);
      }
    }
  }
  
  // Check intent patterns (score: 4 each)
  if (skillDef.intentPatterns) {
    for (const pattern of skillDef.intentPatterns) {
      if (matchesPattern(input, pattern)) {
        score += 4;
        matches.push(`intent: "${pattern}"`);
      }
    }
  }
  
  return { score, matches };
}

/**
 * Main evaluation function
 */
function evaluatePrompt(input) {
  const filePaths = extractFilePaths(input);
  const results = [];
  
  for (const [skillName, skillDef] of Object.entries(config.skills)) {
    const { score, matches } = evaluateSkill(skillName, skillDef, input, filePaths);
    
    if (score >= config.minConfidenceScore) {
      results.push({
        skill: skillName,
        score,
        matches,
        description: skillDef.description || ''
      });
    }
  }
  
  // Sort by score descending
  results.sort((a, b) => b.score - a.score);
  
  // Return top N results
  return results.slice(0, config.maxSkillsToShow);
}

/**
 * Format output for Claude Code hook system
 */
function formatOutput(results) {
  if (results.length === 0) {
    return JSON.stringify({ continue: true });
  }
  
  const skillList = results.map(r => {
    const confidence = r.score >= 10 ? 'HIGH' : r.score >= 6 ? 'MEDIUM' : 'LOW';
    return `  - ${r.skill} [${confidence}]: ${r.description}`;
  }).join('\n');
  
  const feedback = `
╔══════════════════════════════════════════════════════════════╗
║                   SKILL ACTIVATION SUGGESTED                  ║
╚══════════════════════════════════════════════════════════════╝

The following skills may be relevant to this task:

${skillList}

Consider loading these skills for better context and patterns.
Use: Read the skill file at .claude/skills/<skill-name>/SKILL.md
`;

  return JSON.stringify({
    continue: true,
    feedback: feedback.trim()
  });
}

// Main execution
let input = '';
process.stdin.setEncoding('utf8');

process.stdin.on('readable', () => {
  let chunk;
  while ((chunk = process.stdin.read()) !== null) {
    input += chunk;
  }
});

process.stdin.on('end', () => {
  try {
    // Parse the hook input (JSON with prompt field)
    const hookInput = JSON.parse(input);
    const prompt = hookInput.prompt || hookInput.message || input;
    
    const results = evaluatePrompt(prompt);
    console.log(formatOutput(results));
  } catch (e) {
    // If parsing fails, try evaluating raw input
    try {
      const results = evaluatePrompt(input);
      console.log(formatOutput(results));
    } catch {
      // On any error, just continue without blocking
      console.log(JSON.stringify({ continue: true }));
    }
  }
});
