#modified to try to parallize the process
import os,math,argparse, sys, itertools, networkx as nx
from networkx import*

def pairwise(iterable):
    "s -> (s0,s1), (s2,s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)
def NodeListInNetwork(nodelistAll, graphnodelist):
	finnodelist=[]
	for k in range(len(nodelistAll)):
		if nodelistAll[k] in graphnodelist:
			finnodelist.append(nodelistAll[k])
		else:
			pass
	return finnodelist

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='This code will take a nodelist provided find the shortest-paths to reachable targets only to those given a network and the edgelist file', epilog='If you use this code please...remember, remember the 5th of November')
        #parser.add_argument('networkfile', type=str, help='Please provide the base-network file. Format [n1<tab>n2<tab>]')
	parser.add_argument('edgelistfile', type=str, help='The edgelist file. Format [n1<tab>n2<tab><float value>]')
	parser.add_argument('nodelistfile', type=str, help='The list of nodes which will be considered as source for finding shortest paths. Format [n1<\n>')
	parser.add_argument('pathlengthcutoff', type=int, help='Path length cut-off as an integer value')
	parser.add_argument('opfilename', type=str, help='Output filename')
	args = parser.parse_args()
	fh=open(args.edgelistfile,'rb')
	G = nx.read_weighted_edgelist(fh, create_using = nx.DiGraph())
	foutput = args.opfilename
	fout = open(foutput,'w')
	graphnodelist=G.nodes() 
	nodelistAll=[]
	fnodelist = open(args.nodelistfile,'r')
	nodes = fnodelist.readlines()
	for i in range(len(nodes)):
		nodelistAll.append(nodes[i].strip())
	nodelist=NodeListInNetwork(nodelistAll, graphnodelist)
	fout.write("NodePairs\tPathScore\tPathLength\tNormalizedPathScore\tPaths\n")
	for nl in range(len(nodelist)):
			length,path=nx.single_source_dijkstra(G,nodelist[nl],weight='weight')
			pathkeys=path.keys()
			for t in range(len(pathkeys)):
				dp = path[list(path)[t]]
				dpstr = ",".join(map(str, dp))
				if len(dp)<args.pathlengthcutoff:
		 				pass
				else:
						pathscore=0.0
						for x, y in pairwise(dp):
								t=G.get_edge_data(x,y)
								pathscore=t['weight']+pathscore
						normpathscore = pathscore/float(len(dp))
						nodepairs = nodelist[nl]+"_"+dp[len(dp)-1]
						fout.write(nodepairs+"\t%s"%str(pathscore)+"\t%s"%str(len(dp))+"\t%s"%str(normpathscore)+"\t%s\n"%dpstr)
	fout.close()	
