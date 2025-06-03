// Define your backend URL at the top
const BACKEND_API_URL = "https://YOUR_RENDER_BACKEND_URL.onrender.com"; // <-- ***REPLACE THIS WITH YOUR ACTUAL RENDER URL***

async function fetchTodos() {
    const response = await fetch(`${BACKEND_API_URL}/get_todos`); // Use the constant
    const todos = await response.json();
    const todoList = document.getElementById("todoList");
    todoList.innerHTML = "";

    todos.forEach(todo => {
        const li = document.createElement("li");
        li.textContent = todo.todo;

        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = "Delete";
        deleteBtn.onclick = () => deleteTodo(todo.todo);

        li.appendChild(deleteBtn);
        todoList.appendChild(li);
    });
}

async function addTodo() {
    const todoInput = document.getElementById("todoInput");
    const todoText = todoInput.value.trim();

    await fetch(`${BACKEND_API_URL}/add`, { // Use the constant
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ todo: todoText })
    });

    todoInput.value = "";
    fetchTodos();
}

async function deleteTodo(todoText) {
    await fetch(`${BACKEND_API_URL}/delete`, { // Use the constant
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ todo: todoText })
    });

    fetchTodos();
}

document.addEventListener("DOMContentLoaded", fetchTodos);
