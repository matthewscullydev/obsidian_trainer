## Obsidian Mindmap Generator
---

This is a tool for generating mindmaps within obsidian. In order to use this you will want to follow these preliminary steps first.

* Create a new Obsidian vault
	* This is for the safety of your other .md files within the directory you will place this script.
	* It becomes harder to visualize your mindmaps with larger vaults so small vault sizes will be the most optimal

- Place mindmap_generator.py in your obsidian vault directory
```bash
mv mindmap_generator.py /home/User/Documents/yourvault/
```
- Configure your Obsidian Graph View Force Filters so that the mindmap is discernible
	- Set Center Force, Repel Force, and Link Force to 1.0
	- Set Link Distance to 30
 
---
## Importing Mindmaps
---

To import mindmaps find your Flashcard directory where mindmaps are saved.

use a copy command with a wildcard to copy all markdown files into your vault

```
cd Flashcards/
cp History/*.md /your_vault/
```

