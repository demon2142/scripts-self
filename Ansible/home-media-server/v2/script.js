document.addEventListener('DOMContentLoaded', function() {
    fetchWeatherData();
});

function fetchWeatherData() {
    fetch('/weather')
        .then(response => response.json())
        .
