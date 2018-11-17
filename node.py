"""
---------------------------------------------------------------------------

NODE:

Node is a custom object type. Each node represents a capability in the provided example.

attributes:

node.level = the level of the capability in the capability map. 
if node_x.level = 0 then node_x is the top capability
if node_x.level = 1 then node_x is a child of a node with level 1
etc.

node.rank = the index of a node in the list of nodes at the same level.
(all sibling nodes have the same level but different rank)


node.value = the name of the object represented by the node.
node.tree = the dictionary object from which the set of nodes is generated
node.parent = the Node object which is the parent of node.
node.siblings = the list of Node objects with the same parent as node.
node.children = the list of Node objects for which node is the parent.
node.xpos = the x position of the shape to be generated from the node.
node.ypos = the y position of the shape to be generated from the node.
node.width = the width of the shape to be generated from the node.
node.height = the x height of the shape to be generated from the node


methods:
....
For each of the above attributes, there is a method for populating the attribute based on where the node sits in the tree.

There is a method called "populate_node_attributes()" which populates the attributes, EXCEPT xpos and width, which are populated 
from the bottom up when the diagram generator function runs, as opposed to populate_node_attributes which is run on the nodes from 
the top down.

Additionally, there is a print_node() function which prints the attributes of the node in an easy-to-read fashion.

Many lines with print statements have been commented-out, un-comment them for debugging purposes if you are trying to draw a diagram
from your own data.
---------------------------------------------------------------------------
"""
class Node:
	def __init__(self, value, tree):
		self.value = value
		self.tree = tree
		self.level = 0
		self.rank = 0
		self.parent = 0
		self.siblings = []
		self.children = []
		self.xpos = 0
		self.ypos = 5
		self.width = 1.811
		self.height = 0.787402

	def set_level(self):

		def flatten_list(l):
			return [item for sublist in l for item in sublist]

		def get_root_string_from_dict(tree):
			keys = tree.keys()
			vals = tree.values()
			flat_values = flatten_list(vals)
			for key in keys:
				if key not in flat_values:
					return key

		def get_level_int_from_dict(node, tree):
			level = 0
			root = get_root_string_from_dict(tree)
			#print("root node: {}".format(root))
			current_level = [root]
			while node not in current_level and level<10:
				next_level = []
				for each in current_level:
					#print("each: {}".format(each))
					#print("tree[each]: {}".format(tree[each]))
					next_level.append(tree[each])
				next_level = flatten_list(next_level)
				level += 1
				current_level = next_level
				#print("Current Level {}".format(current_level))
			return level

		self.level = get_level_int_from_dict(self.value, self.tree)

	def set_rank(self):

		def flatten_list(l):
			return [item for sublist in l for item in sublist]

		def get_root_string_from_dict(tree):
			keys = tree.keys()
			vals = tree.values()
			flat_values = flatten_list(vals)
			for key in keys:
				if key not in flat_values:
					return key

		def get_level_int_from_dict(node, tree):
			level = 0
			root = get_root_string_from_dict(tree)
			current_level = [root]
			while node not in current_level and level<10:
				next_level = []
				for each in current_level:
					next_level.append(tree[each])
				next_level = flatten_list(next_level)
				level += 1
				current_level = next_level
			return level

		def get_node_names_at_level(level, tree):
			nodes = []
			keys = tree.keys()
			for key in keys:
				if get_level_int_from_dict(key, tree) == level:
					nodes.append(key)
			return nodes

		def get_rank():
			nodes = get_node_names_at_level(self.level, self.tree)
			rank = nodes.index(self.value)
			return rank

		self.rank = get_rank()

	def set_parent(self):
		try:
			keys = self.tree.keys()
			for key in keys:
				if self.value in self.tree[key]:
					parent = Node(key, self.tree)
					parent.set_level()
					parent.set_rank()
					self.parent = parent
		except:
			pass

	def set_siblings(self):
		try:
			tree = self.tree
			keys = tree.keys()
			sibling_names = []
			siblings = []
			for key in keys:
				if self.value in tree[key]:
					sibling_names = tree[key]
					break
			for sibling in sibling_names:
				sibling_node = Node(sibling, self.tree)
				if sibling_node.value != self.value:
					#print("Sibling Names {}".format(sibling_node.value))
					siblings.append(sibling_node)

			self.siblings = siblings
		except:
			pass

	def set_children(self):
		tree = self.tree
		child_names = tree[self.value]
		child_nodes = []
		for child in child_names:
			new_node = Node(child, tree)
			new_node.set_level()
			new_node.set_rank()
			new_node.set_parent()
			new_node.set_siblings()
			new_node.set_children()
			try:
				if len(new_node().children!=0):
					for grandchild in child.children:
						grandchild.set_level()
						grandchild.set_rank()
						grandchild.set_parent()
						grandchild.set_siblings()
						grandchild.set_children()
			except:
				pass
			child_nodes.append(new_node)
		self.children = child_nodes

	def set_height(self):
		#Assumes self.children is populated and and level is accurate for children
		if len(self.children) != 0:
			import config
			self.height = self.height + (config.PADDING_SIZE*2*(config.DEPTH - self.level))

	def set_width(self):
		#Assumes self.children is populated and width is accurate for children.
		if len(self.children) != 0:
			import config
			sum_of_child_widths = 0
			child_widths = []
			for child in self.children:
				child.set_width()
				sum_of_child_widths	= sum_of_child_widths + child.width
				child_widths.append(child.width)
				width = sum_of_child_widths
			else:
				width = sum_of_child_widths - config.PADDING_SIZE*2
			print("Node: {}\n sum_of_child_widths: {}\n len(self.children): {}\n child_widths: {}\n width: {}\n".format(self.value, sum_of_child_widths, len(self.children), child_widths, width))
			self.width = width

	def set_xpos(self):
		#self.set_children()
		self.set_width()
		if len(self.children) != 0:
			import numpy
			import config
			child_xpos = []
			for child in self.children:
				child.set_xpos()
				child_xpos.append(child.xpos)
			print("Node: {} \n Node Name: {} \n Node: Children {} \n child_xpos: {} \n numpy.mean(child_xpos): {}".format(self, self.value, self.children, child_xpos, numpy.mean(child_xpos)))
			xpos = numpy.mean(child_xpos)
			if self.level != 0:
				print("LEVEL NOT EQUAL ZERO {} LEVEL DOES EQUAL {}".format(self.value, self.level))
				self.xpos = xpos
			else:
				print("LEVEL EQUALS ZERO {}".format(self.value))
				self.xpos = xpos - config.BASE_WIDTH
		else:
			import config
			self.set_parent()
			padding_size = config.PADDING_SIZE
			depth = config.DEPTH
			base_width = config.BASE_WIDTH
			xpos = (padding_size * depth) + ((base_width/2) * (self.rank + 1)) + (padding_size*self.rank) + (padding_size*self.parent.rank)
			print("Node: {} \n Node Name: {} \n Node: Children {} \n parent rank: {}\n xpos: {}".format(self, self.value, self.children, self.parent.rank, xpos))
			self.xpos = xpos

	def populate_node_attributes(self):
		self.set_level()
		self.set_rank()
		if(self.level != 0):
			self.set_parent()
			self.set_siblings()
		self.set_children()
		#self.set_xpos()
		self.set_height()
		#self.set_width()

	
	def print_node(self):
		print(
			"""
			--------------------------------------------------------------------

			Node Value: {}\n
			Node Level: {}\n
			Node Rank:  {}\n
			Node Children: {}\n
			Node Xpos: {}\n
			Node Height: {}\n
			Node Width: {}\n

			---------------------------------------------------------------------
			""".format(self.value, self.level, self.rank, self.children, self.xpos, self.height, self.width)
		)


########################
"""
TESTS BELOW
"""
########################
"""
from capability_map import capability_map

new_node = Node('Customer Travel Experience', capability_map)
new_node.populate_node_attributes()



print("Node: {} {}".format(new_node, "\n"))
print("Value: {} {}".format(new_node.value, "\n"))
print("Level: {} {}".format(new_node.level, "\n"))
print("Rank: {} {}".format(new_node.rank, "\n"))
#print("Parent Node: {} {}".format(new_node.parent, "\n"))
#print("Parent Node Name: {} {}".format(new_node.parent.value, "\n"))
#print("Sibling Nodes: {} {}".format(new_node.siblings, "\n"))
print("Child Nodes: {} {}".format(new_node.children, "\n"))
print("Xpos: {} {}".format(new_node.xpos, "\n"))
print("Height: {} {}".format(new_node.height, "\n"))
print("Width: {} {}".format(new_node.width, "\n"))
"""