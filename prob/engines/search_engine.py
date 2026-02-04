try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None

class SearchEngine:
    def __init__(self):
        self.ddgs = None
        if DDGS:
            try:
                self.ddgs = DDGS()
            except:
                self.ddgs = None

    def search(self, query, max_results=5):
        """Searches the web and returns a list of results."""
        if not self.ddgs:
            # Try re-initializing if it failed once
            if DDGS:
                try:
                    self.ddgs = DDGS()
                except:
                    return [{"title": "Search Error", "href": "#", "body": "Could not initialize DDGS."}]
            else:
                return [{"title": "Search Disabled", "href": "#", "body": "duckduckgo_search not installed."}]

        results = []
        try:
            # Use the newer text() generator
            resp = self.ddgs.text(query, max_results=max_results)
            for r in resp:
                results.append({
                    "title": r.get("title"),
                    "href": r.get("href"),
                    "body": r.get("body")
                })
        except Exception as e:
            # Fallback for older versions or different API signatures
            try:
                # Some versions used a different approach
                with DDGS() as ddgs:
                    for r in ddgs.text(query, max_results=max_results):
                        results.append({
                            "title": r.get("title"),
                            "href": r.get("href"),
                            "body": r.get("body")
                        })
            except Exception as e2:
                print(f"Search error: {e} | Fallback error: {e2}")
                return [{"title": "Search Failure", "href": "#", "body": str(e)}]

        return results

    def format_results(self, results):
        """Formats search results for LLM consumption."""
        formatted = "Search Results:\n"
        for i, r in enumerate(results):
            formatted += f"{i+1}. {r.get('title', 'No Title')} ({r.get('href', '#')})\n{r.get('body', 'No Content')}\n\n"
        return formatted
