import requests #this is to send HTTP requests
import re #this is to implement the regular expressions
from urllib.parse import urlparse #this is to parse the URLs
import networkx as nx #Networkx is used for graph functionalities
import matplotlib.pyplot as plt #This is to plot the graphs for visualisation
from community import community_louvain #this is used for community detection
class webCrawler(object): #creating class for crawler.
    def __init__(self, baseURL): #intially this will be called when the program is executed
        self.baseURL = baseURL #baseURL variable stores the starting url
        self.visitedLinks = set() #visitedLinks is a set to store unique URL data
        self.uoitLinks = [] #uoitLinks variable is to store the links related to uoit
        self.nodeEdge = [] #nodeEdge dictionary
    def gethtmlinfo(self, URL): #to get html page information
        try:
            htmlInfo = requests.get(URL) #library htmldata of the url is retrieved using requests
        except Exception as e: #Exception handling will be thrown if there is any error.
            print(e)
            return ""
        return htmlInfo.content.decode('latin-1') #decoded data will be returned here.
    def get_uoitURL(self, URL): #get_uoitURL is a function to retrieve uoit links and these are also defined as nodes.
        uoitlinks = []
        htmlInfo = self.gethtmlinfo(URL) #gethtmlinfo function is called
        linkInformation = re.findall('<a\s+(?:[^>]*?\s+)?href="([^"]*)"', htmlInfo) #filtering the href tags from html info
        for link in linkInformation: #retrieving uoit associated links
            splitLink = link.split(".")
            if "https://ontariotechu" in splitLink:
                uoitlinks.append(link)
                if "ontariotechu" in splitLink:
                    uoitlinks.append(link)
            if "https://uoit" in splitLink:
                uoitlinks.append(link)
                if "uoit" in splitLink:
                    uoitlinks.append(link)
        return set(filter(lambda x: 'mailto' not in x, uoitlinks)) #here unique uoit links is returned as a set.
    def Crawler(self, URL): #Crawler is used for crawling the links in a page and this is also defined as Edges.
        edgeDict = [] #edgeDict is used to store edges associated touoit
        for link in self.get_uoitURL(URL):
            edgeDict.append(link) #to add all urls to edgeDict
            if link in self.uoitLinks:
                continue #ignors the links which are already available.
            self.uoitLinks.append(link) #add links to uoitLinks
        for i,link in enumerate(edgeDict): #prints and map the nodes, edges together
            print(f"{i}.{link}")
            self.nodeEdge.append((URL,link)) #mapping the nodes and edges
    def main(self): #Main function for our program
        self.Crawler(self.baseURL) # calling Crawler function with the baseURL
        for i,link in enumerate(self.uoitLinks): #iterating the uniqueURLS and finds the associated edges/links
            print(f"------------No-{i}--> Node: {link} -----------------------")
            self.Crawler(link)
            self.visitedLinks.add(link) #adding to visitedLinks, to avoid duplicate links
        self.Results() #Calling Results functions
    def Results(self): # This is used for graph calculations
        G=nx.Graph() #Initialize the graph
        G.add_edges_from(self.nodeEdge) # add nodes and edges to the graph
        #Below functions calculate the graph functionalities
        print("{} \n Average Degree: {} \n Density: {} \n Weakly Connected Graphs: {} \n Average Clustering: {} \n is_directed: {} \n is_weighted: {} \n Diameter: {} \n Average Path Length: {}\n ".format(nx.info(G),nx.degree(G),nx.density(G),[c for c in (nx.connected_components(G))],nx.average_clustering(G),nx.is_directed(G),nx.is_weighted(G),nx.diameter,nx.average_shortest_path_length(G)))
        print("---------------List of Betweenness_Centrality----------------")
        for betweenness in sorted(nx.betweenness_centrality(G), key=nx.betweenness_centrality(G).get, reverse= True):
            print("{},{}".format(betweenness,nx.betweenness_centrality(G)[betweenness]))
        print("---------------List of Closeness_Centrality------------------")
        for closeness in sorted(nx.closeness_centrality(G), key=nx.closeness_centrality(G).get, reverse= True):
            print("{},{}".format(closeness,nx.closeness_centrality(G)[closeness]))
        print("---------------List of Degree_Centrality---------------------")
        for degree in sorted(nx.degree_centrality(G), key=nx.degree_centrality(G).get, reverse= True):
            print("{},{}".format(degree,nx.degree_centrality(G)[degree]))
        print("--------------List of Page_Rank_Centrality-------------------")
        for pagerank in sorted(nx.pagerank(G), key=nx.pagerank(G).get,reverse= True):
            print("{},{}".format(pagerank,nx.pagerank(G)[pagerank]))
        print("----------------Community_Detection-----------------------")
        part = community_louvain.best_partition(G)
        values = [part.get(node) for node in G.nodes()]
        nx.draw_spring(G, cmap = plt.get_cmap('jet'), node_color = values, node_size=30, with_labels=False)
        print (len(values))
        
        plt.show()
        plt.savefig("mv.png")
        
        degrees = [G.degree(n) for n in G.nodes()]
        plt.hist(degrees)
        plt.show()
        s = sorted(G.degree, key=lambda x: x[1], reverse=True)
        degrees = sorted([x[0] for x in s])
        frequency = sorted([x[1] for x in s])
        plt.loglog(frequency, degrees)
        plt.xlabel("Degree")
        plt.ylabel("No. of nodes (Frequency)")
        plt.title("Degree distribution")
        plt.show()
        
        #this function is called for visualization of the graph
        nx.draw(G, with_labels=True)
        plt.show()
        #This gives the degree distribution graph
        degrees = [G.degree(n) for n in G.nodes()]
        plt.hist(degrees)
        plt.show()
if __name__ == "__main__":
    crawler = webCrawler("https://ontariotechu.ca/")
    crawler.main()
