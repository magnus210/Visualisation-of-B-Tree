# Visualisation-of-B-Tree
Web application for the visualisation fo B-tree data structure

This is a simple web-based tool to visualise B-tree operations like Insert, Delete, Search, and Update. It helps users understand how B-trees maintain balance with real-time graphical updates.

## What This Project Does

This project allows users to interactively visualise how a B-tree data structure works. A B-tree is a self-balancing search tree that keeps data sorted and allows for efficient insertion, deletion, and search operations. The tool helps demonstrate how these operations affect the structure of the tree in real-time, making it easier to grasp the concept of B-trees.

Key operations that can be visualised include:
- **Insertion:** Adds new nodes while keeping the tree balanced.
- **Deletion:** Removes nodes and rebalances the tree.
- **Search:** Locates a node based on the key provided.
- **Update:** Modifies the value of a node.

The tool uses Flask for the backend and Graphviz to dynamically render and update the tree structure as operations are performed.

## Features

- Visualisfe real-time B-tree operations.
- Dynamic tree structure representation.
- Built using Flask, HTML, CSS, and JavaScript.

## Getting Started

1. Clone the repository.
2. Install required dependencies using `pip install -r requirements.txt`.
3. Run the Flask server with `python app.py`.
4. Access the tool at `http://localhost:5000`.

