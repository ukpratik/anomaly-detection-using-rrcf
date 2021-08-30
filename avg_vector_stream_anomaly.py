import numpy as np
import rrcf



# Set tree parameters
num_trees = 40
shingle_size = 4
tree_size = 256

# Create a forest of empty trees
forest = []
for _ in range(num_trees):
    tree = rrcf.RCTree()
    forest.append(tree)


lines = open("result_avg_vectors.csv",'r').read().split('\n')
# X = np.array([eval(line) for line in lines])
X = np.array([])
for data in lines:
    if len(data) < 2:
        continue
    X = np.append(X,eval(data))

# Use the "shingle" generator to create rolling window
points = rrcf.shingle(X, size=1)

# Create a dict to store anomaly score of each point
avg_codisp = {}

# For each shingle...
for index, point in enumerate(X):
    # For each tree in the forest...
    for tree in forest:
        # If tree is above permitted size...
        if len(tree.leaves) > tree_size:
            # Drop the oldest point (FIFO)
            tree.forget_point(index - tree_size)
        # Insert the new point into the tree
        tree.insert_point(point, index=index)
        # Compute codisp on the new point...
        new_codisp = tree.codisp(index)
        # And take the average over all trees
        if not index in avg_codisp:
            avg_codisp[index] = 0
        avg_codisp[index] += new_codisp / num_trees


print(avg_codisp)