import re
import time
#checks string for query pattern
def has_query(html_string,query):
	m = re.findall(query,html_string)
	if m:
		return True
	else:
		return False
#Creates list of successors by parsing href page pattern
def get_hyperlink_list(html_string):
	return re.findall('(?<=page)\d+',html_string)
#Given a page index, creates a string of the contents in that page
def expand(file_name):
	global intra
	intra_n = intra + '/page'
	htmlFile = open(intra_n+file_name +'.html', 'r')
	return htmlFile.read()
#Counts the number of query# words in a file. Hueristic
def count_query_words(html_string):
	return len(re.findall('QUERY',html_string))

def get_hyperlink_query_words(html_string):
	m = re.findall('> (.*?) </A>', html_string)
	words = []
	if m:
		for i in range(len(m)):
			words.append(re.findall('QUERY\d+',m[i]))
	return words

def get_sequence(query_word_list):
	seq = [[] for i in range(len(query_word_list))]
	for i in range(len(query_word_list)):
		if query_word_list[i]:
			for j in range(len(query_word_list[i])):
				seq[i].append(int(re.findall('QUERY(.*)',query_word_list[i][j])[0]))
		else:
			seq[i].append(None)
	return seq
def max_sequences(seq_list):
	max_seqs = [0] * len(seq_list)
	for i in range(len(seq_list)):
		if(seq_list[i]):
			max_s = 1
			this_s = 1
			for j in range(1,len(seq_list[i])):
 				if(seq_list[i][j] == seq_list[i][j-1]+1):
 					this_s += 1
 					if(this_s > max_s):
 						max_s = this_s
 				else:
 					this_s = 1
		max_seqs[i] = max_s
	return max_seqs

def h_best_page(html_string,w1,w2,w3):
	l1 =get_hyperlink_list(html_string)
	link_scores = [0]*len(l1)
	l2 = get_hyperlink_query_words(html_string)
	l3 = get_sequence(l2)
	h3 = max_sequences(l3)


	for i in range(len(l1)):
		link_scores[i] = w1*count_query_words(expand(l1[i])) + w2*len(l2[i]) + w3*h3[i]
	return link_scores
def report_path(map, goal):
	path = []
	current_node = goal
	while(current_node in map):
		path.insert(0,current_node)
		current_node = map[current_node]
	path.insert(0,current_node)
	return path

def DFS(start_node,goal_query, visited=None):
	global expanded

	if(visited is None):
		visited = set()

	start = expand(start_node)

	if(has_query(start,goal_query)):
		return [start_node]
	
	for i in get_hyperlink_list(start):
		if not(i in visited):
			visited.add(i)
			expanded += 1
			path = DFS(i,goal_query,visited)

			if path is not None:
				path.insert(0, start_node)
				return path
	return None

def BFS(start_node, goal_query):
	global expanded
	
	open_l = []
	closed_l = set()
	path = {}
	open_l.append(start_node)
	closed_l.add(start_node)
	found = False

	while(open_l):
		node = open_l.pop()
		node_string = expand(node)
		expanded += 1
		
		if(has_query(node_string,goal_query)):
			found = True
			break
		
		children = get_hyperlink_list(node_string)
		for x in children:
			if not(x in closed_l):
				open_l.insert(0,x)
				closed_l.add(x)
				path[x] = node 
	if(found):
		return report_path(path,node)
	else:
 		return None
def Best_FS(start_node,goal_query,max_size = 0):
	global expanded
	
	open_l = {}
	closed_l = set()
	path = {}
	open_l[start_node] = 1000
	closed_l.add(start_node)
	found = False
	while(open_l):
		node = sorted(open_l, key=open_l.get)[-1]
		del open_l[node]
		node_string = expand(node)
		expanded += 1
		
		if(has_query(node_string,goal_query)):
			found = True
			break
		
		children = get_hyperlink_list(node_string)
		h_list = h_best_page(node_string,1,1,1)
		for x in range(len(children)):
			if not(children[x] in closed_l):
				open_l[children[x]] = h_list[x]
				closed_l.add(children[x])
				path[children[x]] = node 
				if(max_size != 0 and len(open_l) > max_size):
					remove = sorted(sorted(open_l, key=open_l.get))[0]
					closed_l.remove(remove)
					del open_l[remove]
	if(found):
		return report_path(path,node)
	else:
 		return None
intra = 'intranet1'	
expanded = 0
query = 'QUERY1 QUERY2 QUERY3 QUERY4'
start = '1'
h = {'page3':4,'page2':10}
time.clock()
print(DFS(start,query),expanded)
expanded = 0
print(time.clock())
print(BFS(start,query),expanded)
expanded = 0
print(time.clock())
print(Best_FS(start,query,10),expanded)
print(time.clock())


