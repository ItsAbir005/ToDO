async function fetchTodos() {
    const response = await fetch(`http://127.0.0.1:5000/get_todos`);
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

    await fetch(`http://127.0.0.1:5000/add`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ todo: todoText })
    });

    todoInput.value = "";
    fetchTodos();
}

async function deleteTodo(todoText) {
    await fetch(`http://127.0.0.1:5000/delete`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ todo: todoText })
    });

    fetchTodos();
}

document.addEventListener("DOMContentLoaded", fetchTodos);

