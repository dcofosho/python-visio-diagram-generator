from capability_map import capability_map
"""
---------------------------------------------------------------------------

CAPABILITY_MAP:

capability_map is a dictionary representing hierarchically nest capabilities, for example as shown below:

capability_map = {
	'Customer Travel Experience' : ['Pre- and Post - Travel Experience', 'Check-In Desks Management', 'Gate Departure Management','Customer Airport Services'],
	'Pre- and Post - Travel Experience': ['Customer Products and Marketing', 'Sales', 'Customer Pre-Travel Experience', 'Access and Transportation', 'Customer Relations', 'Customer Loyalty Management'],
	'Check-In Desks Management': ['Luggage Acceptance', 'Passenger Information Management', 'Check-In Desks Management'],
	'Gate Departure Management': ['Outbound Flight Planning', 'Data Control Management', 'Passenger Boarding Management', 'Flight Closeout and Post Departure Management'],
	'Customer Airport Services': ['Retail Management', 'Lounge Services Management', 'Customer Special Needs Services Management'],
	'Customer Products and Marketing': [], 
	...

e;g;
capabilitiy_map['Customer Travel Experience'] is equal to the child nodes of the node named "Customer Travel Experience"

when capability_map[capability_x]=[], then capability_x has no children.

note that there can only be one "top level" capability (i.e. one which has no parents)
 

---------------------------------------------------------------------------
"""

from node import Node

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

import config

"""
config contains the following the predefined values:

PADDING_SIZE = The desired padding between shapes
DEPTH = The depth of the tree of hierarchically nested objects to be represented in the diagram
STARTING_XPOS = The starting x position at which bottom-level shapes are initially dropped
STARTING_YPOS = The starting y position at which bottom-level shapes are initially dropped
BASE_WIDTH = The width of the master shape used for generating the diagram
BASE_HEIGHT = The height of the master shape used for generating the diagram
"""


import os
import win32com.client
from win32com.client import constants




def generate_diagram(tree, template_path, stencil_path, output_path, master):
	"""
	generate_diagram generates a visio diagram given the following inputs:
	tree: a dict object representing a tree of hierarchically nested objects to be represented on the page
	template_path: a path to the template (vst or vstx file) from which the diagram is to be generated
	stencil_path: a path to the stencil (vss or vssx file) containing the shape representing the objects
	master: the master containing the shape
	output_path: a path ending with a vsd file name in which you would like the generated diagram to be saved

	Many lines with print statements have been commented-out, un-comment them for debugging purposes if you are trying to draw a diagram
	from your own data.
	"""

	def resize_right_and_up_and_set_text(width, base_width, height, base_height, text, vis_shape):
		"""
		resize_right_and_up_and_set_text takes a visio shape and resizes it based on the original and desired dimensions.
		This function also sets the shape text.

		The shapes are resized horizontally and vertically half in one direction, half in the other, to maintain the position of the shape.
		"""
		resize_amount_vertically = height - base_height
		print("RAV: {}\n Node: {}\n".format(resize_amount_vertically, text))
		"""
		The Resize function used below takes three arguments:

		an integer which represents the direction of the resize,
		an integer which represents the amount of the resize,
		an integer representing the units to be used

		visit the below site for more information:
		https://docs.microsoft.com/en-us/office/vba/api/visio.shape.resize
		"""
		vis_shape.Resize(2, resize_amount_vertically/2, 65)
		vis_shape.Resize(6, resize_amount_vertically/2, 65)
		resize_amount_horizontally = width - base_width

		print("RAH: {}\n Node: {}\n".format(resize_amount_horizontally, text))
		print("RAH + base_width: {}\n Node: {}\n".format(resize_amount_horizontally+base_width, text))
		vis_shape.Resize(0, resize_amount_horizontally/2, 65)
		vis_shape.Resize(4, resize_amount_horizontally/2, 65)
		vis_shape.Text = text
		return vis_shape

	def build_node_list_from_dict(tree):
		list_of_nodes = []
		for key in tree.keys():
			new_node = Node(key, tree)
			new_node.populate_node_attributes()
			list_of_nodes.append(new_node)
		for node in reversed(list_of_nodes):
			node.set_xpos()
			node.set_width()
		return list_of_nodes

	nodes = build_node_list_from_dict(tree)
	#print("Nodes: {}".format(nodes))
	xpos = config.STARTING_XPOS
	ypos = config.STARTING_YPOS
	PADDING_SIZE = config.PADDING_SIZE
	base_height = config.BASE_HEIGHT
	base_width = config.BASE_WIDTH
	checked_nodes = []
	appVisio = win32com.client.Dispatch("Visio.Application")
	appVisio.Visible =1
	#e.g. template = 'template.vst'
	doc = appVisio.Documents.Add(template_path)
	pagObj = doc.Pages.Item(1)
	#e.g. stencil_path = 'stencil.vss'
	stnObj = appVisio.Documents(stencil_path)
	#e.g. master = 'master'
	mastObj = stnObj.Masters(master)
	visited_nodes = []
	for node in nodes:
	# 	node.print_node()
	# 	for each in node.children:
	# 		print("""
	# 			---------------------------------------------------------------------------------------------------------------------------------------------
	# 			BEGIN CHILD NODE DETAILS FOR {}
	# 			""".format(node.value))
	# 		each.print_node()
	# 		print(
	# 			"""
	# 			END CHILD NODE DETAILS FOR {}
	# 			---------------------------------------------------------------------------------------------------------------------------------------------
	# 			""".format(node.value))
		shpObj = pagObj.Drop(mastObj, node.xpos, node.ypos)
		shpObj = resize_right_and_up_and_set_text(node.width, base_width, node.height, base_height, node.value, shpObj)
		
	doc.SaveAs(output_path)
	pagObj.AutoSizeDrawing()
	pagObj.CenterDrawing()


	#Un-comment the lines below to close the page and quit visio
	#doc.Close()
	#appVisio.Visible =0
	#appVisio.Quit()

#The code below runs the above function with the provided example data. Change the path strings to match the paths on your machine.
generate_diagram(
	capability_map, 
	"C:\\Users\\DanielCohen\\Documents\\CodingProjects\\cm_vis5\\template.vst", 
	"C:\\Users\\DanielCohen\\Documents\\CodingProjects\\cm_vis5\\stencil.vss", 
	"C:\\Users\\DanielCohen\\Documents\\CodingProjects\\cm_vis5\\output.vsd",
	"Capability")		
