
from flask import Flask, request, jsonify, render_template, send_from_directory
from b_tree import BTree
import os

app = Flask(__name__, static_folder='static')

btree = BTree(degree=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/insert', methods=['POST'])
def insert():
    data = request.get_json()
    key = data.get('key')
    if key is not None:
        try:
            btree.insert(key)
            visualize_tree()  # Update visualization after insert
            return jsonify(message="Key inserted successfully"), 200
        except Exception as e:
            return jsonify(message=str(e)), 400
    return jsonify(message="No key provided"), 400

@app.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    key = data.get('key')
    if key is not None:
        try:
            btree.delete(key)
            visualize_tree()  # Update visualization after delete
            return jsonify(message="Key deleted successfully"), 200
        except Exception as e:
            return jsonify(message=str(e)), 400
    return jsonify(message="No key provided"), 400

import base64

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    key = data.get('key')
    if key is not None:
        found = btree.search_key(key)
        if found:
            return jsonify(message=f"Key {key} found"), 200
        else:
            return jsonify(message="Key not found"), 200
    return jsonify(message="No key provided"), 400


@app.route('/visualize', methods=['GET'])
def visualize_tree():
    try:
       
        dot = btree.generate_dot()
       
        if not os.path.exists('static'):
            os.makedirs('static')
        
        image_path = 'static/BTree_min_degree.png'
        
        dot.render(filename='static/BTree_min_degree', format='png', cleanup=True)
        
        return jsonify({'file': image_path}), 200 

    except Exception as e:
        return jsonify({'error': str(e)}), 500 
@app.route('/reset', methods=['POST'])
def reset():
    global btree
    btree = BTree(degree=2)  # Reinitialize the B-Tree with default degree
    visualize_tree()  # Update visualization after reset
    return jsonify(message="B-Tree has been reset"), 200

@app.route('/change_degree', methods=['POST'])
def change_degree():
    data = request.get_json()
    degree = data.get('degree')
    if degree is not None:
        try:
            global btree
            btree = BTree(degree=degree)  # Reinitialize B-Tree with the new degree
            visualize_tree()  # Update visualization after changing degree
            return jsonify(message="B-Tree degree changed successfully"), 200
        except Exception as e:
            return jsonify(message=str(e)), 400
    return jsonify(message="No degree provided"), 400

@app.route('/update_key', methods=['POST'])
def update_key():
    data = request.get_json()
    old_key = data.get('oldKey')
    new_key = data.get('newKey')
    if old_key is not None and new_key is not None:
        try:
            btree.update(old_key, new_key)
            visualize_tree()  # Update visualization after key update
            return jsonify(message="Key updated successfully"), 200
        except Exception as e:
            return jsonify(message=str(e)), 400
    return jsonify(message="Old or new key not provided"), 400

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
    #new
