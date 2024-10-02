#WikiRacer Transformed
WikiRacer Transformed is an approach to the WikiRacer problem, using transformer-based models for enhanced navigation through Wikipedia pages. This project utilizes Sentence Transformer to embed words or sentences and compute the Euclidean distance between these embedded links (nodes), enabling more efficient pathfinding across Wikipedia pages.

Project Structure
internet.py: This script uses web scraping to enter a specified Wikipedia link in the format /wiki/any_link and returns all the hyperlinks on that page. The scraped links are stored in the wiki_cache folder, and the filenames of the new links are encoded for organization.

random_links.txt: A text file containing 12 Wikipedia links that were used for testing the performance of WikiRacer Transformed. You can use these links to run your own tests.

test_search.py: Contains functions for initial testing of WikiRacer Transformed, allowing you to verify the basic functionality of the algorithm.

test_and_graphs.ipynb: A Jupyter Notebook used for testing the performance of WikiRacer Transformed and generating meaningful graphs to visualize the results.

wikiracer.py: This file implements the core logic of the algorithm, including the embedding of Wikipedia links, computation of Euclidean distances, and the search mechanics for finding paths between nodes.

wikiracer_transformed.py: A user-friendly interface allowing you to test WikiRacer Transformed. This program can be used to try out the algorithm on different Wikipedia pages and see how it performs.

How It Works
Embedding Links: WikiRacer Transformed embeds the words or sentences from Wikipedia links using Sentence Transformer.
Distance Calculation: The algorithm computes the Euclidean distance between the embedded links/nodes to determine their similarity or proximity in the Wikipedia network.
Pathfinding: The algorithm aims to find the shortest path between two Wikipedia pages by minimizing the distances between nodes, ensuring efficient navigation.
Usage
To try out WikiRacer Transformed, clone this repository and run wikiracer_transformed.py. The program will allow you to input Wikipedia links and observe the algorithm's pathfinding performance.
