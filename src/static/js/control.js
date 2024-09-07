async function apiRequest(endpoint, method='POST', data={}) {
    
    const response = await fetch(endpoint, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
    return response.json();
}

async function adjustFocus() {
    const autofocus = document.getElementById('autofocus').checked;
    const focus_value = document.getElementById('focus_value').value;
    const data = autofocus ? {autofocus: true} : {focus_value: parseFloat(focus_value)};
    const result = await apiRequest('/api/adjust_focus', 'POST', data);
    document.getElementById('result').innerText = JSON.stringify(result);
}

async function zoom() {
    const zoom_value = document.getElementById('zoom_value').value;
    const result = await apiRequest('/api/zoom', 'POST', {zoom_value: parseFloat(zoom_value)});
    document.getElementById('result').innerText = JSON.stringify(result);
}
