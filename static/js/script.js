// Global Variables
let playerId = null; // Placeholder for the player's ID

// Toast Notification System
function showToast(message, type = "info") {
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// Fetch Player Data
async function fetchPlayerData() {
    try {
        const response = await fetch(`/api/player/${playerId}`);
        if (!response.ok) throw new Error("Failed to fetch player data.");
        const data = await response.json();
        updatePlayerResources(data.resources);
    } catch (error) {
        showToast(error.message, "error");
    }
}

// Update Player Resources on the UI
function updatePlayerResources(resources) {
    const resourceContainer = document.getElementById("resources");
    resourceContainer.innerHTML = "";
    for (const [key, value] of Object.entries(resources)) {
        const resourceDiv = document.createElement("div");
        resourceDiv.textContent = `${key}: ${value}`;
        resourceContainer.appendChild(resourceDiv);
    }
}

// Fetch Available Tasks
async function fetchAvailableTasks() {
    try {
        const response = await fetch(`/api/tasks/${playerId}`);
        if (!response.ok) throw new Error("Failed to fetch tasks.");
        const data = await response.json();
        displayTasks(data.tasks);
    } catch (error) {
        showToast(error.message, "error");
    }
}

// Display Tasks on the UI
function displayTasks(tasks) {
    const taskContainer = document.getElementById("tasks");
    taskContainer.innerHTML = "";
    tasks.forEach(task => {
        const taskDiv = document.createElement("div");
        taskDiv.className = "card";
        taskDiv.innerHTML = `
            <h3>${task.name}</h3>
            <p>${task.description}</p>
            <p>Resources Required: ${JSON.stringify(task.required_resources)}</p>
            <p>Duration: ${task.duration} ticks</p>
            <button onclick="assignTask(${task.id})">Start Task</button>
        `;
        taskContainer.appendChild(taskDiv);
    });
}

// Assign a Task
async function assignTask(taskId) {
    try {
        const response = await fetch("/api/tasks/assign", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ player_id: playerId, task_id: taskId })
        });
        const data = await response.json();
        if (data.error) throw new Error(data.error);
        showToast(data.message, "success");
        fetchPlayerData();
        fetchActiveTasks();
    } catch (error) {
        showToast(error.message, "error");
    }
}

// Fetch Active Tasks
async function fetchActiveTasks() {
    try {
        const response = await fetch(`/api/tasks/active/${playerId}`);
        if (!response.ok) throw new Error("Failed to fetch active tasks.");
        const data = await response.json();
        displayActiveTasks(data.active_tasks);
    } catch (error) {
        showToast(error.message, "error");
    }
}

// Display Active Tasks with Progress
function displayActiveTasks(activeTasks) {
    const activeTasksContainer = document.getElementById("active-tasks");
    activeTasksContainer.innerHTML = "";
    activeTasks.forEach(task => {
        const taskDiv = document.createElement("div");
        taskDiv.className = "card";
        const progress = (task.ticks_remaining / task.duration) * 100;
        taskDiv.innerHTML = `
            <h3>${task.name}</h3>
            <div class="progress-bar">
                <div class="progress" style="width: ${100 - progress}%"></div>
            </div>
            <p>${task.ticks_remaining} ticks remaining</p>
        `;
        activeTasksContainer.appendChild(taskDiv);
    });
}

// Fetch Galactic Map Data
async function fetchGalacticMap() {
    try {
        const response = await fetch("/api/map");
        if (!response.ok) throw new Error("Failed to fetch galactic map.");
        const data = await response.json();
        displayGalacticMap(data.celestial_bodies);
    } catch (error) {
        showToast(error.message, "error");
    }
}

// Display Galactic Map
function displayGalacticMap(celestialBodies) {
    const mapContainer = document.getElementById("galactic-map");
    mapContainer.innerHTML = "";
    celestialBodies.forEach(body => {
        const bodyDiv = document.createElement("div");
        bodyDiv.className = "card";
        bodyDiv.innerHTML = `
            <h3>${body.name} (${body.type})</h3>
            <p>Resources: ${JSON.stringify(body.resources)}</p>
            <p>Explored: ${body.explored ? "Yes" : "No"}</p>
            <button onclick="exploreBody(${body.id})" ${body.explored ? "disabled" : ""}>Explore</button>
        `;
        mapContainer.appendChild(bodyDiv);
    });
}

// Explore a Celestial Body
async function exploreBody(bodyId) {
    try {
        const response = await fetch("/api/map/explore", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: bodyId })
        });
        const data = await response.json();
        if (data.error) throw new Error(data.error);
        showToast(data.message, "success");
        fetchGalacticMap();
    } catch (error) {
        showToast(error.message, "error");
    }
}

// Initialize Game
function initializeGame(playerIdParam) {
    playerId = playerIdParam;
    fetchPlayerData();
    fetchAvailableTasks();
    fetchActiveTasks();
    fetchGalacticMap();
}
