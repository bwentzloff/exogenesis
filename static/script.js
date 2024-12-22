async function fetchGameState() {
    try {
        const response = await fetch('/api/state');
        const data = await response.json();

        // Update resources and trends
        updateDashboard(data.resources);

        // Update active tasks
        const tasksContainer = document.getElementById('active-tasks');
        tasksContainer.innerHTML = ''; // Clear old tasks

        data.tasks.forEach(task => {
            const taskDiv = document.createElement('div');
            taskDiv.textContent = `${task.name} (${task.ticks_remaining} ticks remaining)`;
            tasksContainer.appendChild(taskDiv);
        });

        // Update alerts
        renderAlerts(data.alerts);
    } catch (error) {
        console.error("Failed to fetch game state:", error);
    }
}

async function fetchMapData() {
    try {
        const response = await fetch('/api/map');
        const data = await response.json();
        const mapContainer = document.getElementById('universe-map');
        mapContainer.innerHTML = ''; // Clear existing elements

        data.celestial_bodies.forEach(body => {
            const bodyDiv = document.createElement('div');
            bodyDiv.classList.add('celestial-body');
            bodyDiv.classList.add(body.explored ? 'explored' : 'unexplored');
            bodyDiv.style.left = `${Math.random() * 80 + 10}%`;
            bodyDiv.style.top = `${Math.random() * 80 + 10}%`;
            bodyDiv.title = `${body.name} (${body.type})`;
            bodyDiv.textContent = body.name.charAt(0); // Abbreviation for body name

            bodyDiv.onclick = () => {
                if (!body.explored) {
                    exploreBody(body.id);
                } else {
                    alert(`${body.name} is already explored.`);
                }
            };

            mapContainer.appendChild(bodyDiv);
        });
    } catch (error) {
        console.error("Failed to fetch map data:", error);
    }
}

function renderAlerts(alerts) {
    const alertsContainer = document.getElementById('alerts');
    alertsContainer.innerHTML = ''; // Clear existing alerts

    alerts.forEach(alert => {
        const alertDiv = document.createElement('div');
        alertDiv.classList.add('alert');
        alertDiv.classList.add(alert.includes('Warning') ? 'warning' : 'info');
        alertDiv.textContent = alert;
        alertsContainer.appendChild(alertDiv);
    });
}

let previousResources = {};

function updateDashboard(resources) {
    const resourcesDiv = document.getElementById('resources');
    resourcesDiv.innerHTML = ''; // Clear existing resources

    for (const [resource, value] of Object.entries(resources)) {
        const trend = value > (previousResources[resource] || 0) ? '▲' : '▼';
        const resourceDiv = document.createElement('div');
        resourceDiv.textContent = `${resource}: ${value} ${trend}`;
        resourcesDiv.appendChild(resourceDiv);
    }

    previousResources = { ...resources };
}

async function assignTask(task, room, ticks) {
    try {
        const response = await fetch('/api/assign_task', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task, room, ticks_required: ticks })
        });

        if (response.ok) {
            const data = await response.json();
            alert(data.message);
            fetchGameState();
        } else {
            const error = await response.json();
            alert(`Error: ${error.error}`);
        }
    } catch (err) {
        console.error("Failed to assign task:", err);
    }
}

async function exploreBody(bodyId) {
    try {
        const response = await fetch('/api/explore', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: bodyId })
        });

        if (response.ok) {
            const data = await response.json();
            alert(data.message);
            fetchMapData();
        } else {
            const error = await response.json();
            alert(`Error: ${error.error}`);
        }
    } catch (err) {
        console.error("Failed to explore body:", err);
    }
}

async function clearAlerts() {
    try {
        const response = await fetch('/api/clear_alerts', { method: 'POST' });
        if (response.ok) {
            fetchGameState();
        }
    } catch (err) {
        console.error("Failed to clear alerts:", err);
    }
}

async function register(event) {
    event.preventDefault();

    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;

    try {
        const response = await fetch('/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            alert('Registration successful! Please log in.');
        } else {
            const error = await response.json();
            alert(`Error: ${error.error}`);
        }
    } catch (err) {
        console.error("Registration failed:", err);
    }
}

async function login(event) {
    event.preventDefault();

    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            alert('Login successful!');
            toggleAuthControls(true);
        } else {
            const error = await response.json();
            alert(`Error: ${error.error}`);
        }
    } catch (err) {
        console.error("Login failed:", err);
    }
}

async function logout() {
    try {
        const response = await fetch('/auth/logout', { method: 'POST' });
        if (response.ok) {
            alert('Logged out successfully.');
            toggleAuthControls(false);
        }
    } catch (err) {
        console.error("Logout failed:", err);
    }
}

function toggleAuthControls(isLoggedIn) {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const logoutButton = document.getElementById('logout-button');

    if (isLoggedIn) {
        loginForm.style.display = 'none';
        registerForm.style.display = 'none';
        logoutButton.style.display = 'block';
    } else {
        loginForm.style.display = 'block';
        registerForm.style.display = 'block';
        logoutButton.style.display = 'none';
    }
}

async function checkLoginStatus() {
    toggleAuthControls(false);
}

document.addEventListener('DOMContentLoaded', () => {
    fetchGameState();
    fetchMapData();

    document.getElementById('login-form').addEventListener('submit', login);
    document.getElementById('register-form').addEventListener('submit', register);
    document.getElementById('logout-button').addEventListener('click', logout);

    checkLoginStatus();
});
