document.getElementsByClassName('form').addEventListener('submit', function(event) {
    event.preventDefault();
    const data = document.getElementById('data').value;

    fetch('/setweight', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: data })
    })
    .then(response => response.json())
    .then(result => console.log('Success:', result))
    .catch(error => console.error('Error:', error));
});