#from py_wikiracer.internet import Internet
from internet import Internet
from typing import List

from sentence_transformers import SentenceTransformer, SimilarityFunction

class Parser:

    @staticmethod
    def get_links_in_page(html: str) -> List[str]:
        """
        In this method, we should parse a page's HTML and return a list of links in the page.
        Be sure not to return any link with a DISALLOWED character.
        All links should be of the form "/wiki/<page name>", as to not follow external links
        """
        links = []
        disallowed = Internet.DISALLOWED

        # YOUR CODE HERE
        # You can look into using regex, or just use Python's find methods to find the <a> tags or any other identifiable features
        # A good starting place is to print out `html` and look for patterns before/after the links that you can string.find().
        # Make sure your list doesn't have duplicates. Return the list in the same order as they appear in the HTML.
        # This function will be stress tested so make it efficient!
        #print(html)
        while html.find('a href="/wiki/') != -1:

            #Searching for all the links which begin with '/wiki/'
            num = html.find('a href="/wiki/')

            #Dropping out the: 'a href="' characters
            html = html[num+8:]

            #Searching the end of the link with the character: "
            num = html.find('"')

            #Defining the link using it's len
            link = html[0:num]

            #Discarting links with disallowed characters
            if not any(c in link[6:] for c in disallowed):
                #Checking if the link is already in the list
                if link not in links:
                    links.append(link)

        return links

# In these methods, we are given a source page and a goal page, and we should return
#  the shortest path between the two pages. Be careful! Wikipedia is very large.

class DijkstrasProblem:
    def __init__(self):
        self.internet = Internet()
    # Links should be inserted into the heap as they are located in the page.
    # By default, the cost of going to a link is the length of a particular destination link's name. For instance,
    #  if we consider /wiki/a -> /wiki/ab, then the default cost function will have a value of 8.
    # This cost function is overridable and your implementation will be tested on different cost functions. Use costFn(node1, node2)
    #  to get the cost of a particular edge.
    # You should return the path from source to goal that minimizes the total cost. Assume cost > 0 for all edges.
    def dijkstras(self, source = "/wiki/Calvin_Li", goal = "/wiki/Wikipedia", costFn = lambda x, y: len(y), safe: int = 30):
        path = [source]
        

        #Initialization of variables

        page = source
        data = {}
        j = 0
        min_ = 0
        aux = []

        try:
            while j<safe:
                #Retrieving the info from a page
                html = self.internet.get_page(page)
                #Collecting the links from the html
                links = Parser.get_links_in_page(html)

                #Checking if the goal was found in the new links
                if goal in links:
                    #print(f'{goal} encontrado en {page}')
                    break
                
                #Appending new links' paths into the data dict and computing their costs
                for link in links:
                    if (link not in data.values()) and (link != page):
                        coste = min_ + costFn(goal, link)
                        data[coste] = aux + [link]

                #Founding the min cost inside the data dict
                min_ = min(data.keys())

                #Storing the cache of the current page for future paths
                aux = data[min_]

                #Redefining the page based on the link with the min cost
                page = aux[-1]

                #Deleting the current page key from the dict
                del data[min_]

                j += 1
        
            if goal in links:
                path = path + aux + [goal]
            else:
                print(f'ERROR: PATH not found in {safe} iterations')
                path = None

        except:
            path = None

        return path # if no path exists, return None
    
    def dijkstras2(self, source = "/wiki/Calvin_Li", goal = "/wiki/Wikipedia", costFn = lambda x, y: len(y), safe: int = 30):
        path = [source]

        #Initialization of variables
        
        try:
            html_targets = self.internet.get_page(goal)

            targets = Parser.get_links_in_page(html_targets)

            targets = set(targets)

            page = source

            visited = {source}

            path_caches = {}

            j = 0

            aux = []

            while j < safe:
                #Retrieving the info from a page
                html = self.internet.get_page(page)
                #Collecting the links from the html
                links = Parser.get_links_in_page(html)

                #Checking if the goal was found in the new links
                if goal in links:
                    #print(f'{goal} encontrado en {page}')
                    break
                
                #Appending new links into the path_caches dict and saving their paths
                for link in links:
                    if link not in path_caches:
                        path_caches[link] = aux + [link]
                
                #Appending the new links into the alredy checked links
                visited = visited.union(set(links))
                
                #Checking if there is a connection between the visited set and the targets set
                connection = list(visited.intersection(targets))
                

                #Redifining the value of page
                if len(connection) != 0:
                    #Retrieving the index of the item inside connection with the less distance from the goal
                    d = costFn(connection, [goal])
                    #Redifining page
                    page = connection[d]
                    #Deleting the connection from the targets
                    targets.discard(page)

                else:
                    #Otherwise, look at all the links in visited and take the one with more affinity with the targets
                    data1 = list(visited)
                    #Retrieving an index that minimizes the distance between the visited data and the targets
                    d = costFn(data1, targets)
                    #Redefining the page
                    page = data1[d]

                #Storing the cache of the current page for future paths
                aux = path_caches[page]

                j+=1

            #Checking if the loop was broken 
            if goal in links:
                path = path + aux + [goal]

            else:
                print(f'ERROR: PATH not found in {safe} iterations')
                print(f'The visited pages were: {visited}')
                print(links)
                path = None
        
        except:
            path = None
        
        return path

    

def word_distance(model, list1: list, list2: list):
    ''' 
    Computes the semantic textual similarity bewtween all the words inside two lists.
    It uses the similarity function defined in the model.
    Retrieves the index of the first list which corresponds to the min distance.

    *Args
    model: pretained transformer model used for words embedding and 
    list1: a list containing words or sentences
    list2: a list containing words or sentences

    *Return:
    idx: an index corresponding to the word inside the list1 with the min semantic textual similarity
    '''

    #Removing the first characters from the words corresponding to: '\wiki\'
    w1 = [word1[6:].replace('_', " ") for word1 in list1]

    w2 = [word2[6:].replace('_', " ") for word2 in list2]
    
    #Embedding the words/sentences with the model
    emb1 = model.encode(w1)
    emb2 = model.encode(w2)

    #Computing the distance between words in the two arrays
    #The model computes the negative EUCLIDEAN or MANHATTAN distance
    #that's why a (-) is set.
    dist = -model.similarity(emb1, emb2)
    
    #Returns the index corresponding to the word inside the list1 with the min semantic textual similarity
    idx = dist.argmin().item() // len(list2)

    return idx

class WikiracerProblem:
    def __init__(self):
        self.internet = Internet()

    # Time for you to have fun! Using what you know, try to efficiently find the shortest path between two wikipedia pages.
    # Your only goal here is to minimize the total amount of pages downloaded from the Internet, as that is the dominating time-consuming action.

    # Your answer doesn't have to be perfect by any means, but we want to see some creative ideas.
    # One possible starting place is to get the links in `goal`, and then search for any of those from the source page, hoping that those pages lead back to goal.

    # Note: a Dijkstra implementation with no optimizations will not get credit, and it will suck.
    # You may find Internet.get_random() useful, or you may not.

    def wikiracer(self, source = "/wiki/Calvin_Li", goal = "/wiki/Wikipedia", safe: int = 50, distance = SimilarityFunction.EUCLIDEAN):
        
        #Defining the transformer mode.
        #The similarity_fn_name could be set to be Euclidean, Manhattan or Cosine distance
        #The Euclidean and Manhattan distances are returned negatives
        model = SentenceTransformer("all-MiniLM-L6-v2", similarity_fn_name=distance)

        dji = DijkstrasProblem()

        path = dji.dijkstras2(source = source, goal=goal, safe=safe, costFn= lambda x,y: word_distance(model, x, y))

        #Retrieving the internet attribute from the dji
        self.internet = dji.internet
        print(100*'*')
        print(f'New query, number of requests: {len(self.internet.requests)} \nPath: {path}')
        return path # if no path exists, return None
