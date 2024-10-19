document.getElementById('file').addEventListener('change', function() {
    document.getElementById('loading-spinner').style.display = 'block';
    setTimeout(function() {
        document.getElementById('loading-spinner').style.display = 'none';
    }, 2000); // Hide spinner after 2 seconds
});

document.getElementById('upload-form').addEventListener('submit', function() {
    document.getElementById('loading-spinner').style.display = 'block';
});