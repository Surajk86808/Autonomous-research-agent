import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_web(query: str):

    response = client.search(
        query=query,
        search_depth="advanced",   # important
        max_results=3
    )

    results = []

    for r in response["results"]:
        results.append(
            f"""
            Title: {r['title']}
            URL: {r['url']}
            Content: {r['content'][:1000]}

        """
        )

    return "\n\n".join(results)