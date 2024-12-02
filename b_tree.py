from flask import jsonify
from graphviz import Digraph

class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t
        self.leaf = leaf
        self.keys = []
        self.child = []

class BTree:
    def __init__(self, degree):
        self.root = BTreeNode(degree, True)
        self.t = degree

    def insert(self, k):
        if self.search_key(k):
            print(f"Key {k} already exists, not inserting duplicate.")
            return  # Prevent inserting duplicate keys

        root = self.root
        if len(root.keys) == (2 * self.t - 1):  # Node is full
            new_root = BTreeNode(self.t, False)
            new_root.child.append(self.root)
            self.split_child(new_root, 0)
            self.root = new_root
        self.insert_non_full(self.root, k)
        print(f"Inserted: {k}")

    def insert_non_full(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            if k in x.keys:  # Check for duplicates
                print(f"Key {k} already exists.")
                return
            x.keys.append(None)  # Make space for the new key
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.child[i].keys) == (2 * self.t - 1):  # Child is full
                self.split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self.insert_non_full(x.child[i], k)

    def split_child(self, x, i):
        t = self.t
        y = x.child[i]
        z = BTreeNode(t, y.leaf)
        x.child.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t:]
        y.keys = y.keys[:t - 1]
        if not y.leaf:
            z.child = y.child[t:]
            y.child = y.child[:t]

    def search_key(self, k, x=None):
        if x is None:
            x = self.root
        while True:
            i = 0
            while i < len(x.keys) and k > x.keys[i]:
                i += 1
            if i < len(x.keys) and k == x.keys[i]:
                return True  # Key found
            elif x.leaf:
                return False  # Key not found
            else:
                x = x.child[i]

    def delete(self, k):
        found = self.delete_recursive(self.root, k)
        if len(self.root.keys) == 0:
            if len(self.root.child) > 0:
                self.root = self.root.child[0]
            else:
                self.root = BTreeNode(self.t, True)
        return found

    def delete_recursive(self, node, k):
        t = self.t
        i = 0
        while i < len(node.keys) and node.keys[i] < k:
            i += 1    

        if i < len(node.keys) and node.keys[i] == k:
            if node.leaf:
                node.keys.pop(i)
                return True
            else:
                if len(node.child[i].keys) >= t:
                    pred_key = self.get_predecessor(node, i)
                    node.keys[i] = pred_key
                    return self.delete_recursive(node.child[i], pred_key)
                elif len(node.child[i + 1].keys) >= t:
                    succ_key = self.get_successor(node, i)
                    node.keys[i] = succ_key
                    return self.delete_recursive(node.child[i + 1], succ_key)
                else:
                    self.merge_children(node, i)
                    return self.delete_recursive(node.child[i], k)
        else:
            if node.leaf:
                return False
            flag = (i == len(node.keys))
            if len(node.child[i].keys) < t:
                if i > 0 and len(node.child[i - 1].keys) >= t:
                    self.borrow_from_prev(node, i)
                elif i < len(node.keys) and len(node.child[i + 1].keys) >= t:
                    self.borrow_from_next(node, i)
                else:
                    if i < len(node.keys):
                        self.merge_children(node, i)
                    else:
                        self.merge_children(node, i - 1)
                        i -= 1
            if flag and i > len(node.keys):
                return self.delete_recursive(node.child[i - 1], k)
            else:
                return self.delete_recursive(node.child[i], k)

    def get_predecessor(self, node, index):
        curr = node.child[index]
        while not curr.leaf:
            curr = curr.child[-1]
        return curr.keys[-1]

    def get_successor(self, node, index):
        curr = node.child[index + 1]
        while not curr.leaf:
            curr = curr.child[0]
        return curr.keys[0]

    def merge_children(self, node, index):
        t = self.t
        child = node.child[index]
        sibling = node.child[index + 1]
        child.keys.append(node.keys[index])
        child.keys.extend(sibling.keys)
        if not child.leaf:
            child.child.extend(sibling.child)
        node.keys.pop(index)
        node.child.pop(index + 1)

    def borrow_from_prev(self, node, index):
        child = node.child[index]
        sibling = node.child[index - 1]
        child.keys.insert(0, node.keys[index - 1])
        if not child.leaf:
            child.child.insert(0, sibling.child.pop())
        node.keys[index - 1] = sibling.keys.pop()

    def borrow_from_next(self, node, index):
        child = node.child[index]
        sibling = node.child[index + 1]
        child.keys.append(node.keys[index])
        if not child.leaf:
            child.child.append(sibling.child.pop(0))
        node.keys[index] = sibling.keys.pop(0)

    def update(self, old_key, new_key):
        result = self.search_key(old_key)
        if result:
            self.delete(old_key)
            self.insert(new_key)
            print(f"Updated: {old_key} to {new_key}")
        else:
            print(f"Update failed: {old_key} not found.")

    def generate_dot(self):
        dot = Digraph('BTree', node_attr={'shape': 'record', 'style': 'rounded,filled', 
                                          
        'fillcolor': 'lightyellow', 'color': 'black', 'fontcolor': 'black', 'fontsize': '14'}, edge_attr={'color': 'gray', 'arrowhead': 'vee'})

        def add_nodes_edges(node, parent=None):
            if node.keys:
                node_label = '|'.join(f'<f{i}> {key}' for i, key in enumerate(node.keys))
                node_id = str(id(node))  
                dot.node(node_id, label=node_label)
                if parent:
                    dot.edge(str(id(parent)), node_id)
                if not node.leaf:
                    for child in node.child:
                        add_nodes_edges(child, node)

        add_nodes_edges(self.root)
        return dot


        
    
#def visualize_tree():
#        dot = tree.generate_dot()
 #       image_path = 'static/BTree_min_degree'
  #      try:
   #         dot.render(filename=image_path, format='png', cleanup=True)
   #     except Exception as e:
    #        print(f"Error rendering DOT file: {e}")
    #    return jsonify({'file': image_path + '.png'}), 200
    

    def print_tree(self, x, l=0):
        print("Level ", l, " ", len(x.keys), end=": ")
        for i in x.keys:
            print(i, end=" ")
        print()
        l += 1
        if len(x.child) > 0:
            for i in x.child:
                self.print_tree(i, l)

    def perform_operations(self, insert_keys, delete_keys, search_keys, update_pairs):
        for key in insert_keys:
            self.insert(key)
            self.print_tree(self.root)

        for key in delete_keys:
            found = self.delete(key)
            if found:
                print(f"Deleted: {key}")
            else:
                print(f"Not Found: {key}")

        for key in search_keys:
            result = self.search_key(key)
            if result:
                print(f"Found: {key}")
            else:
                print(f"Not Found: {key}")

        for old_key, new_key in update_pairs:
            self.update(old_key, new_key)
            self.print_tree(self.root)

def main():
    B = BTree(2)  # this is degree 3 (max 2*3-1 = 5 keys)
    insert_keys = [1, 2, 3, 4, 5,6,7,8,9]
    delete_keys = []
    search_keys = []
    update_pairs = []

    B.perform_operations(insert_keys, delete_keys, search_keys, update_pairs)

    dot = B.generate_dot()
    dot.render('static/BTree_min_degree', format='png', view=False)

if __name__ == '__main__':
    main()
#new