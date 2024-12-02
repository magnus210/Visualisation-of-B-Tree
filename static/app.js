function insertKey() {
    const keyInput = document.getElementById('keyInput');
    const keys = keyInput.value.split(/[\s,]+/).map(Number);

    if (keys.some(isNaN)) {
        console.error('Invalid keys provided');
        return;
    }

    keys.forEach(key => {
        fetch('/insert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ key: key })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            document.getElementById('statusMessage').innerText = data.message;
            visualizeTree();
        })
        .catch(error => console.error('Error:', error));
    });
}

function deleteKey() {
    const keyInput = document.getElementById('keyInput');
    const keys = keyInput.value.split(/[\s,]+/).map(Number);

    if (keys.some(isNaN)) {
        console.error('Invalid keys provided');
        return;
    }

    keys.forEach(key => {
        fetch('/delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ key: key })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            document.getElementById('statusMessage').innerText = data.message;
            visualizeTree();
        })
        .catch(error => console.error('Error:', error));
    });
}

function searchKey() {
    const keyInput = document.getElementById('keyInput');
    const key = keyInput.value.trim();

    if (isNaN(key) || key === '') {
        console.error('Invalid key provided');
        return;
    }

    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ key: parseInt(key, 10) })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('statusMessage').innerText = data.message;
    })
    .catch(error => console.error('Error:', error));
}


function visualizeTree() {
    fetch('/visualize', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('treeImage').src = `${data.file}?timestamp=${new Date().getTime()}`;
    })
    .catch(error => console.error('Error:', error));
}


function resetTree() {
    fetch('/reset', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        document.getElementById('treeImage').src = "/static/placeholder.png";
        document.getElementById('statusMessage').innerText = data.message;
    })
    .catch(error => console.error('Error:', error));
}

function changeDegree() {
    const degreeInput = document.getElementById('degree');
    const degree = parseInt(degreeInput.value, 10);

    if (isNaN(degree)) {
        console.error('Invalid degree value provided');
        return;
    }

    fetch('/change_degree', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ degree: degree })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        document.getElementById('treeImage').src = ""; // Clear the tree image
        document.getElementById('statusMessage').innerText = data.message;
    })
    .catch(error => console.error('Error:', error));
}

function updateKey() {
    const oldKeyInput = document.getElementById('oldKey');
    const newKeyInput = document.getElementById('newKey');
    const oldKey = parseInt(oldKeyInput.value, 10);
    const newKey = parseInt(newKeyInput.value, 10);

    if (isNaN(oldKey) || isNaN(newKey)) {
        console.error('Invalid key values provided');
        return;
    }

    fetch('/update_key', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ oldKey: oldKey, newKey: newKey })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        document.getElementById('statusMessage').innerText = data.message;
        visualizeTree();
    })
    .catch(error => console.error('Error:', error));
}
