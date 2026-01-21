import os
from prob.memory.memory_engine import MemoryEngine

class WikiEngine:
    def __init__(self, memory: MemoryEngine, wiki_dir="prob/output/wiki"):
        self.memory = memory
        self.wiki_dir = wiki_dir
        os.makedirs(self.wiki_dir, exist_ok=True)

    def update_wiki(self):
        discoveries = self.memory.get_discoveries()
        index_content = "# Prob AI Knowledge Wiki\n\n## Table of Discoveries\n\n"

        for d in discoveries:
            title = d['query'][:50].strip() + "..."
            filename = f"article_{d['id']}.md"
            index_content += f"- [{title}]({filename})\n"

            # Create individual article
            article_path = os.path.join(self.wiki_dir, filename)
            with open(article_path, "w") as f:
                f.write(f"# {d['query']}\n\n**Timestamp:** {d['timestamp']}\n\n## Discovery\n{d['result']}\n")

        with open(os.path.join(self.wiki_dir, "index.md"), "w") as f:
            f.write(index_content)

        return os.path.join(self.wiki_dir, "index.md")
