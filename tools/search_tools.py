# import json
# import os

# import requests
# from langchain.tools import tool


# class SearchTools():

#     @tool("Search the internet")
#     def search_internet(query):
#         """Useful to search the internet
#         about a a given topic and return relevant results"""
#         top_result_to_return = 4
#         url = "https://google.serper.dev/search"
#         payload = json.dumps({"q": query})
#         headers = {
#             'X-API-KEY': os.environ['SERPER_API_KEY'],
#             'content-type': 'application/json'
#         }
#         response = requests.request("POST", url, headers=headers, data=payload)
#         # check if there is an organic key
#         if 'organic' not in response.json():
#             return "Sorry, I couldn't find anything about that, there could be an error with you serper api key."
#         else:
#             results = response.json()['organic']
#             string = []
#             for result in results[:top_result_to_return]:
#                 try:
#                     string.append('\n'.join([
#                         f"Title: {result['title']}", f"Link: {result['link']}",
#                         f"Snippet: {result['snippet']}", "\n-----------------"
#                     ]))
#                 except KeyError:
#                     next

#             return '\n'.join(string)

import json
import os
import requests
from langchain.tools import tool
from typing import Union

class SearchTools:
    @tool("Search the internet")
    def search_internet(query: Union[str, dict]) -> str:
        """Useful to search the internet about a given topic and return relevant results.
        
        Args:
            query: A string or dict containing the search query. If a dict, it should have a 'q' key.
        
        Returns:
            A formatted string with up to 4 search results (title, link, snippet) or an error message.
        """
        # Ensure query is a string
        if isinstance(query, dict):
            query = query.get("q", str(query))  # Extract 'q' if dict, else stringify
        elif not isinstance(query, str):
            query = str(query)  # Convert non-string inputs to string

        top_result_to_return = 4
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': os.environ.get('SERPER_API_KEY', ''),
            'content-type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()  # Raise exception for bad status codes
            data = response.json()
        except (requests.RequestException, ValueError) as e:
            return f"Error searching the internet: {str(e)}. Check your SERPER_API_KEY."

        if 'organic' not in data:
            return "Sorry, I couldn't find any results. There might be an issue with the Serper API key or the query."

        results = data['organic']
        string = []
        for result in results[:top_result_to_return]:
            try:
                string.append('\n'.join([
                    f"Title: {result['title']}",
                    f"Link: {result['link']}",
                    f"Snippet: {result['snippet']}",
                    "\n-----------------"
                ]))
            except KeyError:
                continue  # Skip malformed results

        return '\n'.join(string) if string else "No valid results found."