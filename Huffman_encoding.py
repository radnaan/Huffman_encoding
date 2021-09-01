import bisect
encoding = {}
class Node:
    def __init__(self, key, val):
        self.left = None
        self.right = None
        self.key =key
        self.value = val

    def is_leaf(self):
        return not(self.left or self.right)
    
    def __lt__(self, other):
         return self.key < other.key    
    
    def __str__(self):
        if self.is_leaf(): return "[{}]".format(self.value)
        return "[{} {} {}]".format(self.left or '_', self.value, self.right or '_')            

# takes: str; returns: [ (str, int) ] (Strings in return value are single characters)
def frequencies(s):
    return list(dict.fromkeys([(i,s.count(i)) for i in s]))

# takes: [ (str, int) ], str; returns: String (with "0" and "1")
def encode(freqs, s):
    global encoding
    if(len(freqs)<=1 or (max(freqs,key = lambda x: x[1])[1]<=1 and s=="")):return None
    construct_encoding(freqs)    
    return ''.join([encoding[i]for i in s])

# takes [ [str, int] ], str (with "0" and "1"); returns: str
def decode(freqs,bits):
    global encoding
    if(len(freqs)<=1 or (max(freqs,key = lambda x: x[1])[1]<=1 and bits=="")):return None
    construct_encoding(freqs)    
    decoding = {v: k for k, v in encoding.items()}
    current = decoded = ''
    for i in bits:
        current+=i
        if(current in decoding):
            decoded+=decoding[current]
            current = ''
    return decoded

def construct_encoding(freqs):
    global encoding
    encoding = {}
    freqs = sorted(freqs,key = lambda x : x[1])
    trees = []
    for i in freqs:
        leaf =  Node(i[1],i[0])
        trees.append(leaf)
    while(len(trees)>=2):
        a = trees.pop(0)
        b = trees.pop(0)
        tree = Node(a.key+b.key,None)
        tree.left=a
        tree.right=b
        bisect.insort(trees,tree)
    tree_explore(trees[0],'')    
    return trees[0]

def tree_explore(node, path):
    global encoding
    if(node.value!=None):
        encoding[node.value] = path
    if(node.left):
        tree_explore(node.left,path+'1')    
    if(node.right):
        tree_explore(node.right,path+'0')
