// Toast Notification System
function showToast(message, type = "info") {
    const toastContainer = document.getElementById("toast-container");

    const toast = document.createElement("div");
    toast.className = `toast ${type}`;

    // Add an icon to the toast
    const icon = document.createElement("span");
    icon.className = `toast-icon ${type}`;
    toast.appendChild(icon);

    // Add the message
    const text = document.createElement("span");
    text.className = "toast-message";
    text.textContent = message;
    toast.appendChild(text);

    toastContainer.appendChild(toast);

    // Remove the toast after 5.3 seconds (5s display + 0.3s fade-out animation)
    setTimeout(() => {
        toast.remove();
    }, 5300);
}

// Fetch Game State
async function fetchGameState() {
    try {
        const response = await fetch('/api/state');
        const data = await response.json();

        // Update resources
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
        showToast("Failed to fetch game state.", "error");
    }
}

// Fetch Universe Map Data
async function fetchMapData() {
    try {
        const response = await fetch('/api/map');
        const data = await response.json();
        const mapContainer = document.getElementById('universe-map');
        mapContainer.innerHTML = ''; // Clear existing elements

        data.celestial_bodies.forEach(body => {
            // Create celestial body
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
                    showToast(`${body.name} is already explored.`, "info");
                }
            };

            mapContainer.appendChild(bodyDiv);
        });
    } catch (error) {
        console.error("Failed to fetch map data:", error);
        showToast("Failed to fetch map data.", "error");
    }
}

// Render Alerts
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

// Update Dashboard with Resources
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

// Assign Task
async function assignTask(task, room, ticks) {
    try {
        const response = await fetch('/api/assign_task', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task, room, ticks_required: ticks })
        });

        if (response.ok) {
            const data = await response.json();
            showToast(data.message, "success");
            fetchGameState();
        } else {
            const error = await response.json();
            showToast(`Error: ${error.error}`, "error");
        }
    } catch (err) {
        console.error("Failed to assign task:", err);
        showToast("Failed to assign task.", "error");
    }
}

// Explore a Celestial Body
async function exploreBody(bodyId) {
    try {
        const response = await fetch('/api/map/explore', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: bodyId })
        });

        if (response.ok) {
            const data = await response.json();
            showToast(data.message, "success");
            fetchMapData();
        } else {
            const error = await response.json();
            showToast(`Error: ${error.error}`, "error");
        }
    } catch (err) {
        console.error("Failed to explore body:", err);
        showToast("Failed to explore body.", "error");
    }
}

// Clear Alerts
async function clearAlerts() {
    try {
        const response = await fetch('/api/clear_alerts', { method: 'POST' });
        if (response.ok) {
            showToast("Alerts cleared successfully!", "success");
            fetchGameState();
        }
    } catch (err) {
        console.error("Failed to clear alerts:", err);
        showToast("Failed to clear alerts.", "error");
    }
}

// Authentication Functions
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
            showToast('Registration successful! Please log in.', "success");
        } else {
            const error = await response.json();
            showToast(`Error: ${error.error}`, "error");
        }
    } catch (err) {
        console.error("Registration failed:", err);
        showToast("Registration failed.", "error");
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
            showToast('Login successful!', "success");
            toggleAuthControls(true);
        } else {
            const error = await response.json();
            showToast(`Error: ${error.error}`, "error");
        }
    } catch (err) {
        console.error("Login failed:", err);
        showToast("Login failed.", "error");
    }
}

async function logout() {
    try {
        const response = await fetch('/auth/logout', { method: 'POST' });
        if (response.ok) {
            showToast('Logged out successfully.', "success");
            toggleAuthControls(false);
        }
    } catch (err) {
        console.error("Logout failed:", err);
        showToast("Logout failed.", "error");
    }
}

// Toggle Authentication UI
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

// Check Login Status
async function checkLoginStatus() {
    toggleAuthControls(false); // Assume logged out by default
}

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', () => {
    fetchGameState();
    fetchMapData();

    document.getElementById('login-form').addEventListener('submit', login);
    document.getElementById('register-form').addEventListener('submit', register);
    document.getElementById('logout-button').addEventListener('click', logout);

    checkLoginStatus();
});
