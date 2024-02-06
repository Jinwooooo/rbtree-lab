import sys

class Node():
	def __init__(self, data):
		self.data = data
		self.color = 'r'
		self.parent = None
		self.left = None
		self.right = None

class RBTree():
	def __init__(self):
		self.TNULL = Node(0)
		self.TNULL.color = 'b'
		self.TNULL.left = None
		self.TNULL.right = None
		self.root = self.TNULL

	def rotate_left(self, curr):
		r = curr.right
		curr.right = r.left

		if r.left != self.TNULL:
			r.left.parent = curr

		r.parent = curr.parent

		if curr.parent == None:
			self.root = r
		elif curr == curr.parent.left:
			curr.parent.left = r
		else:
			curr.parent.right = r

		r.left = curr
		curr.parent = r

	def rotate_right(self, curr):
		l = curr.left
		curr.left = l.right

		if l.right != self.TNULL:
			l.right.parent = curr

		l.parent = curr.parent

		if curr.parent == None:
			self.root = l
		elif curr == curr.parent.right:
			curr.parent.right = l
		else:
			curr.parent.left = l

		l.right = curr
		curr.parent = l

	def insert_fix(self, curr):
		while curr.parent.color == 'r':
			# subtree in the right side
			if curr.parent == curr.parent.parent.right:
				uncle = curr.parent.parent.left
				# case 1r : uncle is red = RECOLOR
				if uncle.color == 'r':
					uncle.color = 'b'
					curr.parent.color = 'b'
					curr.parent.parent.color = 'r'
					curr = curr.parent.parent
				else:
					# case 3r : uncle is black + left subtree = RESTRUCTURE (double rotation)
					if curr == curr.parent.left:
						curr = curr.parent
						self.rotate_right(curr)
					# case 2r : uncle is black + right subtree = RESTRUCTURE (single rotation)
					curr.parent.color = 'b'
					curr.parent.parent.color = 'r'
					self.rotate_left(curr.parent.parent)
			# subtree in the left side
			else:
				uncle = curr.parent.parent.right
				# case 1l : uncle is red = RECOLOR
				if uncle.color == 'r':
					uncle.color = 'b'
					curr.parent.color = 'b'
					curr.parent.parent.color = 'r'
					curr = curr.parent.parent
				else:
					# case 3l : uncle is black + right subtree = RESTRUCTURE (double rotation)
					if curr == curr.parent.right:
						curr = curr.parent
						self.rotate_left(curr)
					# case 2 : uncle is black + left subtree = RESTRUCTURE (single rotation)
					curr.parent.color = 'b'
					curr.parent.parent.color = 'r'
					self.rotate_right(curr.parent.parent)
			if curr == self.root:
				break
		self.root.color = 'b'

	def insert(self, value):
		node = Node(value)
		node.data = value
		node.parent = None
		node.left = self.TNULL
		node.right = self.TNULL
		node.color = 'r'

		parent_position = None
		insert_position = self.root

		# finding node insert position
		while insert_position != self.TNULL:
			parent_position = insert_position
			if node.data < insert_position.data:
				insert_position = insert_position.left
			else:
				insert_position = insert_position.right

		node.parent = parent_position
		if parent_position == None:
			self.root = node
		elif node.data < parent_position.data:
			parent_position.left = node
		else:
			parent_position.right = node

		# parent is BLACK, no fix is required
		if node.parent == None:
			node.color = 'b'
			return

		if node.parent.parent == None:
			return

		self.insert_fix(node)

	def minimum(self, node):
		while node.left != self.TNULL:
			node = node.left
		return node

	def find_node(self, val):
		node = self.root
		node_position = self.TNULL

		while node != self.TNULL:
			if node.data == val:
				node_position = node

			if node.data <= val:
				node = node.right
			else:
				node = node.left

		if node_position == self.TNULL:
			print("element does not exist in RBTree")
			return None

		return node_position

	def transplant(self, node_del, node_sub):
		if node_del.parent == None:
			self.root = node_sub
		elif node_del == node_del.parent.left:
			node_del.parent.left = node_sub
		else:
			node_del.parent.right = node_sub
		node_sub.parent = node_del.parent

	def delete_fix(self, curr):
		while curr != self.root and curr.color == 'b':
			# // case 1l : curr left & sibling right + black height property violation
			if curr == curr.parent.left:
				sibling = curr.parent.right
				# case 1.1l : sibiling is red
				if sibling.color == 'r':
					sibling.color = 'b'
					curr.parent.color = 'r'
					self.rotate_left(curr.parent)
					sibling = curr.parent.right
				# case 1.2l: sibling and children are black
				if sibling.left.color == 'b' and sibling.right.color == 'b':
					sibling.color = 'r'
					curr = curr.parent
				else:
					# case 1.3l: sibling is black, sibling left child is red, sibling right child is black
					if sibling.right.color == 'b':
						sibling.left.color = 'b'
						sibling.color = 'r'
						self.rotate_right(sibling)
						sibling = curr.parent.right
					# case 1.4l: sibling is black, and sibling right child is red
					sibling.color = curr.parent.color
					curr.parent.color = 'b'
					sibling.right.color = 'b'
					self.rotate_left(curr.parent)
					curr = self.root
			# case 1r : curr right & sibling left + black height property violation
			else:
				sibling = curr.parent.left
				# case 1.1r : sibiling is red
				if sibling.color == 'r':
					sibling.color = 'b'
					curr.parent.color = 'r'
					self.rotate_right(curr.parent)
					sibling = curr.parent.left
				# case 1.2r: sibling and children are black
				if sibling.right.color == 'b' and sibling.right.color == 'b':
					sibling.color = 'r'
					curr = curr.parent
				# case 1.3r: sibling is black, sibling left child is red, sibling right child is black
				else:
					if sibling.left.color == 'b':
						sibling.right.color = 'b'
						sibling.color = 'r'
						self.rotate_left(sibling)
						sibling = curr.parent.left
					# case 1.4r: sibling is black, and sibling right child is red
					sibling.color = curr.parent.color
					curr.parent.color = 'b'
					sibling.left.color = 'b'
					self.rotate_right(curr.parent)
					curr = self.root
		curr.color = 'b'

	def delete_node(self, key):
		curr = self.find_node(key)

		node_ref = curr
		o_color = node_ref.color
		if curr.left == self.TNULL:
			node_rep = curr.right
			self.transplant(curr, curr.right)
		elif curr.right == self.TNULL:
			node_rep = curr.left
			self.transplant(curr, curr.left)
		else:
			node_ref = self.minimum(curr.right)
			o_color = node_ref.color
			node_rep = node_ref.right
			# the successor is the right child of current node
			if node_ref.parent == curr:
				node_rep.parent = node_ref
			else:
				self.transplant(node_ref, node_ref.right)
				node_ref.right = curr.right
				node_ref.right.parent = node_ref

			self.transplant(curr, node_ref)
			node_ref.left = curr.left
			node_ref.left.parent = node_ref
			node_ref.color = curr.color
		if o_color == 'b':
			self.delete_fix(node_rep)

	
	def print_tree(self, node = None, depth = 0):
		if node is None:
			node = self.root

		if node is self.TNULL:
			return

		self.print_tree(node.right, depth + 1)
		print('     ' * depth + f"R----{node.data} ({'Red' if node.color == 'r' else 'Black'})")
		self.print_tree(node.left, depth + 1)


if __name__ == "__main__":
	rbt = RBTree()

	for i in range(1,11):
		rbt.insert(i)

	rbt.print_tree()

	rbt.delete_node(6)
	print('after delete')
	rbt.print_tree()
