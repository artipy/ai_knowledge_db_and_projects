# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository (`knowledge_lib`) is a personal knowledge base maintained as an Obsidian vault, containing educational notes about Large Language Models (LLMs), AI APIs, and related technologies. All content is written in Russian and stored as Markdown files.

## Repository Structure

The knowledge base follows a topic-based organization:

- **Topic directories** (e.g., `OpenAI_API/`, `Local_LLM_Deployment/`): Each subdirectory contains focused notes on a specific subject area
- **`Exercises/`**: Practical assignments with step-by-step instructions, code templates, and grading criteria
  - `Exercises/Solves/`: Student solutions in Jupyter notebook format (`.ipynb`)
  - `Exercises/Reviews/`: Detailed review files with analysis and grading (`*_Review.md`)
- **`raw_notes/`**: Unprocessed notes (`.ipynb`, `.md`) awaiting refinement and organization before being moved to topic-specific locations
- **`.obsidian/`**: Obsidian vault configuration (workspace, appearance, plugins) - do not modify unless explicitly requested

## Content Organization Principles

1. **Markdown files only**: All knowledge articles are in `.md` format
2. **Topic-based hierarchy**: Notes are organized into subdirectories by topic
3. **Obsidian linking**: Internal links use Obsidian's syntax: `[[Topic/Note Title]]`
4. **Bidirectional linking**: Create logical backlinks between related notes (excluding `raw_notes/`) to build an interconnected knowledge graph
5. **Russian language**: All content is written in Russian

## Working with This Repository

### Adding New Notes

When adding new notes:
- Create topic-specific subdirectories as needed (use `Topic_Name/` format with underscores)
- Move processed notes from `raw_notes/` to appropriate topic directories
- **File naming convention**: Use descriptive English filenames with underscores (e.g., `Introduction_to_OpenAI_API.md`, `Working_with_OpenAI_API_in_Python.md`)
  - All filenames MUST be in English for consistency and cross-platform compatibility
  - Use underscores to separate words, not spaces or hyphens
  - Be descriptive but concise
- Maintain Russian language for all content inside the files
- **Automatically add bidirectional links**: When creating or editing notes (excluding `raw_notes/`), establish logical connections by adding backlinks between related topics using Obsidian's `[[Note Name]]` syntax. This creates a interconnected knowledge graph.

### Editing Existing Notes

- Preserve existing formatting and structure
- Maintain the Russian language
- Keep technical terminology consistent with existing notes
- Preserve code examples and their explanatory comments
- When adding content that references other notes, create bidirectional links: if Note A links to Note B, ensure Note B also links back to Note A where contextually appropriate

### Linking Strategy

When working with notes (except those in `raw_notes/`):
- Identify related topics and concepts across different notes
- Add cross-references using `[[Note_Name]]` syntax
- Create backlinks in referenced notes to maintain bidirectional connections
- Example: If `OpenAI_API/Working_with_OpenAI_API_in_Python.md` mentions prompt engineering concepts, add a link to `Prompt_Engineering.md`, and ensure `Prompt_Engineering.md` references the OpenAI API note in relevant sections

### Git Workflow

The repository uses simple git practices:
- Main branch: `main`
- Commit messages follow conventional format (e.g., "feat: Add LLM deployment notes")
- No complex branching strategy required

## Creating Exercises from Raw Notes

When converting Jupyter notebooks from `raw_notes/` into structured learning materials:

1. **Create the knowledge note** in appropriate topic directory (e.g., `OpenAI_API/Working_with_OpenAI_API_in_Python.md`)
2. **Create corresponding exercise** in `Exercises/` with format: `##_Topic_Name_Exercise.md`
3. **Exercise structure must include:**
   - Clear learning objectives
   - Prerequisites (libraries, setup)
   - Multiple parts with progressive difficulty
   - Expected results for self-checking
   - Code templates with `# Your code here` placeholders
   - Grading criteria table with point distribution
   - Recommendations section
4. **Establish bidirectional links** between knowledge note, exercise, and related materials
5. **When reviewing solutions:**
   - Save student solutions as `.ipynb` files in `Exercises/Solves/`
   - Create detailed review as `*_Review.md` in `Exercises/Reviews/`
   - Review must include: point breakdown, specific errors with code examples, recommendations for improvement

## Current Topics

As of the latest commit, the knowledge base covers:
- **OpenAI API**: Python integration, API usage, prompt engineering techniques, text processing, chat roles (system/user/assistant), multi-turn conversations with context preservation
- **Prompt Engineering**: Best practices for creating effective prompts, action verbs, structured prompts, formatted outputs (tables, lists, custom formats), conditional logic in prompts, iterative prompt development. Advanced strategies including Zero-Shot/One-Shot/Few-Shot prompting, Multi-Step Prompting, Chain-of-Thought (CoT), Self-Consistency prompting, and iterative refinement techniques.
- **Local LLM Deployment**: Using LM Studio for local model hosting
- **Python for AI**: Essential Python tools and patterns for AI engineers, including decorators, retry logic with tenacity library, error handling, caching, monitoring, and production-ready API wrappers
- **Practical Exercises**: 4 assignments covering OpenAI API Text Processing (shot prompting, temperature control, cost calculation), Chat Roles and Conversations (multi-turn dialogs, context preservation), Prompt Engineering Best Practices (structured prompts, formatting, conditional logic), and Advanced Prompt Engineering Strategies (Zero/One/Few-Shot, Multi-Step, Chain-of-Thought, Self-Consistency, iterative refinement). Completed exercises (01-03) include student solutions and comprehensive reviews with detailed feedback, error analysis, and recommendations for improvement.

## Exercise Naming Convention

Exercises follow a strict numbering system:
- Format: `##_Topic_Name_Exercise.md` (e.g., `01_OpenAI_API_Text_Processing_Exercise.md`)
- Solutions: `##_Topic_Name_Solve.ipynb` (e.g., `01_OpenAI_API_Text_Processing_Solve.ipynb`)
- Reviews: `##_Topic_Name_Review.md` (e.g., `01_OpenAI_API_Text_Processing_Review.md`)
- All exercise files use English names with underscores
- Increment numbers sequentially as new exercises are added

## Important Notes

- This is a documentation/knowledge repository - there is no build, test, or deployment process
- The `.obsidian/` directory should generally not be modified as it contains user-specific Obsidian settings
- The `raw_notes/` directory contains source materials (Jupyter notebooks, markdown) that are converted into structured notes and exercises
- `raw_notes/` also contains `.env` files for API credentials used in notebook examples - these are gitignored
- When creating exercises from notebooks, preserve all code examples but transform them into templates with clear instructions
