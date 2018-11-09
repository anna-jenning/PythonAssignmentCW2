import urllib2
import pickle

# create the poodle database
def poodle_build():
    def web_crawler(seed):
        def getAllNewLinksOnPage(page,prevLinks):

            response = urllib2.urlopen(page)
            html = response.read()

            links,pos,allFound=[],0,False
            while not allFound:
                aTag=html.find("<a href=",pos)
                if aTag>-1:
                    href=html.find('"',aTag+1)
                    endHref=html.find('"',href+1)
                    url=html[href+1:endHref]
                    if url[:7]=="http://":
                        if url[-1]=="/":
                            url=url[:-1]
                        if not url in links and not url in prevLinks:
                            links.append(url)     
                            print url
                    closeTag=html.find("</a>",aTag)
                    pos=closeTag+1
                else:
                    allFound=True   
            return links

        toCrawl=[seed]
        crawled=[]
        graph={}
        urls=[]
        while toCrawl:
            url=toCrawl.pop()
            crawled.append(url)
            newLinks=getAllNewLinksOnPage(url,crawled)
            toCrawl=list(set(toCrawl)|set(newLinks))
            
        for link in crawled:
            urls.append(link[0])
        print crawled	
        return urls

    def page_scraper(urls):
        index=[]
        url="http://193.61.191.117/~B00686896/com506/Python/B3%20Parsing%20Web%20Pages/test_web/test_index.html"
        response = urllib2.urlopen(url)
        html = response.read()

        pageText,pageWords="",[]
        html=html[html.find("<body")+5:html.find("</body>")]

        finished=False
        while not finished:
            nextCloseTag=html.find(">")
            nextOpenTag=html.find("<")
            if nextOpenTag>-1:
                content=" ".join(html[nextCloseTag+1:nextOpenTag].strip().split())
                pageText=pageText+" "+content
                html=html[nextOpenTag+1:]
            else:
                finished=True
                
        for word in pageText.split():
            if word[0].isalnum() and len(word)>4:
                if not word in pageWords:
                    pageWords.append(word)
        def addToIndex(index,keyword,url):
            for entry in index:
                if entry[0]==word:
                    entry[1].append(url)
                    return
            index.append([word,[url]])

        for word in pageWords:
            addToIndex(index,word,url)	
                
        return index

    def create_graph(urls):
        def getAllNewLinksOnPage(page):

            response = urllib2.urlopen(page)
            html = response.read()

            links,pos,allFound=[],0,False
            while not allFound:
                aTag=html.find("<a href=",pos)
                if aTag>-1:
                    href=html.find('"',aTag+1)
                    endHref=html.find('"',href+1)
                    url=html[href+1:endHref]
                    if url[:7]=="http://":
                        if url[-1]=="/":
                            url=url[:-1]
                        if not url in links:
                            links.append(url)     
                            print url
                    closeTag=html.find("</a>",aTag)
                    pos=closeTag+1
                else:
                    allFound=True   
            return links

        def add_graph(graph, link, url):
            if not links == []:
                if url in graph:
                    graph[url].append(link)
                else:
                    graph[url] = [link]
            else:
                graph[url] = []

        graph = {}

        url="http://193.61.191.117/~B00686896/com506/Python/B3%20Parsing%20Web%20Pages/test_web/test_index.html"
        links = getAllNewLinksOnPage(url)

        # if not links == []:
        #     for link in links:
        #         add_graph(graph, link, url)
        # else:
        add_graph(graph, links, url)

        return graph

    def computeRanks(graph):
        d = 0.85
        numLoops = 10
        ranks = {}
        nPages = len(graph)

        for page in graph:
            ranks[page] = 1.0/nPages

        for i in range(0,numLoops):
            newRanks = {}
            for page in graph:
                newRank = (1-d) / nPages
                for node in graph:
                    if page in graph[node]:
                        newRank = newRank+d*(ranks[node]/len(graph[node]))
                        newRanks[page] = newRank
            ranks = newRanks

        return ranks

    seed = raw_input("Please provide a seed URL>>> ")

    urls = web_crawler(seed)

    index = page_scraper(urls)

    graph = create_graph(urls)

    ranks = computeRanks(graph)

    print "\nWOOF! Poodle data generated"

    return index, graph, ranks

# save the poodle database
def poodle_dump(index, graph, ranks):

    with open("Index.txt", "wb") as f:
        pickle.dump(index, f)

    with open("Graph.txt", "wb") as f:
        pickle.dump(graph, f)

    with open("Ranks.txt", "wb") as f:
        pickle.dump(ranks, f)

    print "WOOF! POODLE data buried"

# retrieve the poodle database
def poodle_restore():

    with open("Index.txt", "rb") as f:
        index = pickle.load(f)

    with open("Graph.txt", "rb") as f:
        graph = pickle.load(f)

    with open("Rank.txt", "rb") as f:
        ranks = pickle.load(f)

    print "WOOF! POODLE data retrieved"

    return index, graph, ranks

# show the poodle database
def poodle_print(index, graph, ranks):
    print "\n\nPOODLE INDEX ----------\n\n"
    print index
    print "\n\nPOODLE GRAPH ----------\n\n"
    print graph
    print "\n\nPOODLE RANKS ----------\n\n"
    print ranks

# show options available from this program
def poodle_help():
    print "POODLE Help options: \n"
    print "-build \t\t Create the Poodle database"
    print "-dump \t\t Save the Poodle database"
    print "-restore \t Retrieve the Poodle database"
    print "-print \t\t Show the Poodle database"
    print "-help \t\t Show this help information"
    print "-nothing \t To exit the program"

# exit the program
def poodle_exit():
    print "WOOF! POODLE shutting down..."

# search words
def poodle_search(ranks, index, search):

    results = {}

    for wordSearch in search.split():
        print "\n" + str(wordSearch)
        if wordSearch in index:
            for result in index[wordSearch]:
                results[result] = ranks[result]

            for key in sorted(results):
                print "%s: %s" % (key, results[key])
        else:
            print "WOOF! No results found."

    print

active = True

while active:
    option = raw_input("\nWOOF! What can POODLE fetch for you? ('-nothing' to exit or '-help' for POODLE Help Options)>>> ")
    option = option.lower()

    if option == "-build":
        index, graph, ranks = poodle_build()
    elif option == "-dump":
        poodle_dump(index, graph, ranks)
    elif option == "-restore":
        index, graph, ranks = poodle_restore()
    elif option == "-print":
        poodle_print(index, graph, ranks)   
    elif option == "-help":
        poodle_help()
    elif option == "-nothing":
        poodle_exit()
        active = False
    else:
        try:
            poodle_search(ranks, index, option)
        except NameError:
            print "You must -build or -restore POODLE before searching"
