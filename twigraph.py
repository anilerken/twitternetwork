import tweepy
import os
import networkx as nx
import matplotlib.pyplot as plt

# auth to twitter
auth = tweepy.AppAuthHandler('xxxxxxxxxxxxx', 'xxxxxxxxxxx')
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

def getIndex(str, alist):
	for i in range(len(alist)):
		if alist[i] == str:
			return i
	return -99

fromuser = raw_input('Enter the username to start from: ')
target = raw_input('Enter the target username: ')
cursor = fromuser
found = False
G = nx.Graph()
nameslist = [fromuser]

while found == False:
	try:
		print cursor
		for follower in tweepy.Cursor(api.followers, screen_name=cursor).items():
			if follower.screen_name not in nameslist:
				G.add_edge(cursor, follower.screen_name)
				nameslist.append(follower.screen_name)
				if follower.screen_name == target:
					found = True
					break
	except tweepy.TweepError:
    		print 'errrrrr muhtemelen protected account ' + cursor

	# move the cursor to the next item of the graph in bft
	#dict = nx.bfs_successors(G, fromuser)
	edges = nx.bfs_edges(G, fromuser)
	nodes = [fromuser] + [v for u, v in edges]
	i = getIndex(cursor, nodes)
	cursor = nodes[i+1]

#plt.subplot(233)
plt.figure(3,figsize=(12,12))
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()

print(nx.shortest_path(G,source=fromuser,target=target))
