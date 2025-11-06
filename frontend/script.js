const API_BASE_URL = "http://127.0.0.1:8000";
const USER_ID = 1; // Placeholder: Replace with actual logged-in user ID
const ACCESS_TOKEN = "your_hardcoded_or_retrieved_token"; // Placeholder for auth

document.addEventListener("DOMContentLoaded", () => {
  fetchTasks();
  document
    .getElementById("addTaskForm")
    .addEventListener("submit", handleAddTask);
});

/**
 * Handles the form submission to add a new task.
 */
async function handleAddTask(event) {
  event.preventDefault();

  const taskPayload = {
    user_id: USER_ID,
    title: document.getElementById("title").value,
    description: document.getElementById("description").value,
    importance: parseInt(document.getElementById("importance").value),
    energy: parseInt(document.getElementById("energy").value),
    time_estimate: parseInt(document.getElementById("time_estimate").value),
    // priority_score is intentionally omitted as the backend calculates it!
    // deadline is omitted for simplicity in this frontend
  };

  try {
    const response = await fetch(`${API_BASE_URL}/tasks/add`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // Add Authorization header once you fully implement security
        // 'Authorization': `Bearer ${ACCESS_TOKEN}`
      },
      body: JSON.stringify(taskPayload),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const addedTask = await response.json();
    console.log("Task added with priority:", addedTask.priority_score);

    // Clear form and refresh list
    document.getElementById("addTaskForm").reset();
    fetchTasks();
  } catch (error) {
    console.error("Error adding task:", error);
    alert("Failed to add task. Check console for details.");
  }
}

/**
 * Fetches the user's tasks and renders them, sorted by priority.
 */
async function fetchTasks() {
  try {
    const response = await fetch(
      `${API_BASE_URL}/tasks/list?user_id=${USER_ID}`
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    let tasks = await response.json();

    // Sort tasks by priority_score (descending) in the frontend
    tasks.sort((a, b) => b.priority_score - a.priority_score);

    renderTaskList(tasks);
  } catch (error) {
    console.error("Error fetching tasks:", error);
    document.getElementById("taskList").innerHTML =
      '<li class="empty-list">Could not load tasks. Ensure backend is running!</li>';
  }
}

/**
 * Renders the list of tasks to the DOM.
 */
function renderTaskList(tasks) {
  const taskListElement = document.getElementById("taskList");
  taskListElement.innerHTML = ""; // Clear existing list

  if (tasks.length === 0) {
    taskListElement.innerHTML =
      '<li class="empty-list">No tasks yet. Add one!</li>';
    return;
  }

  tasks.forEach((task) => {
    const listItem = document.createElement("li");

    // Determine priority class based on score (adjust thresholds as needed)
    let priorityClass = "priority-low";
    if (task.priority_score >= 0.7) {
      priorityClass = "priority-high";
    } else if (task.priority_score >= 0.4) {
      priorityClass = "priority-medium";
    }

    listItem.className = priorityClass;

    listItem.innerHTML = `
            <div class="task-info">
                <div class="task-title">${task.title}</div>
                <div class="task-meta">
                    Imp: ${task.importance} / Energy: ${task.energy} / Time: ${
      task.time_estimate
    } min
                </div>
            </div>
            <span class="priority-score">
                ${(task.priority_score * 100).toFixed(0)}
            </span>
        `;
    taskListElement.appendChild(listItem);
  });
}
