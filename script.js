document.getElementById('adviceForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const name = e.target.elements.name.value;

    fetch('/get-advice', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: name })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('adviceResult').innerText = data.message;
    })
    .catch(error => console.error('Error:', error));
});
