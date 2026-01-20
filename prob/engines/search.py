from duckduckgo_search import DDGS

class SearchEngine:
    def __init__(self):
        self.ddgs = DDGS()

    def search(self, query, max_results=5):
        """Searches the web and returns a list of results."""
        results = []
        try:
            for r in self.ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title"),
                    "href": r.get("href"),
                    "body": r.get("body")
                })
        except Exception as e:
            print(f"Search error: {e}")
        return results

    def format_results(self, results):
        """Formats search results for LLM consumption."""
        formatted = "Search Results:\n"
        for i, r in enumerate(results):
            formatted += f"{i+1}. {r['title']} ({r['href']})\n{r['body']}\n\n"
        return formatted
