import React, { useState } from "react";

export default function ToDoList() {
  const [tasks, setTasks] = useState([
    { text: "Finish the project report", completed: true },
    { text: "Attend the team meeting", completed: false },
    { text: "Reply to client emails", completed: false },
  ]);
  const [newTask, setNewTask] = useState("");

  const addTask = () => {
    if (newTask.trim()) {
      setTasks([...tasks, { text: newTask, completed: false }]);
      setNewTask("");
    }
  };

  const deleteTask = (index: number) => {
    const updatedTasks = tasks.filter((_, i) => i !== index);
    setTasks(updatedTasks);
  };

  const toggleTaskCompletion = (index: number) => {
    const updatedTasks = tasks.map((task, i) =>
      i === index ? { ...task, completed: !task.completed } : task
    );
    setTasks(updatedTasks);
  };

  return (
    <div className="flex flex-col h-full w-full bg-gray-100">
      <div className="flex flex-col h-full w-full bg-white shadow-lg rounded-lg p-6">
        {/* To-Do Header */}
        <div className="border-b border-gray-200 py-3 mb-4">
          <h3 className="text-2xl font-semibold text-gray-800">To-Do List</h3>
        </div>

        {/* To-Do Items */}
        <div className="flex-1 overflow-y-auto">
          <ul className="space-y-4">
            {tasks.map((task, index) => (
              <li key={index} className="flex items-center justify-between">
                <span
                  className={`text-gray-600 cursor-pointer ${
                    task.completed ? "line-through" : ""
                  }`}
                  onClick={() => toggleTaskCompletion(index)}
                >
                  {task.text}
                </span>
                <button
                  className="bg-red-500 text-white px-3 py-1 rounded-lg"
                  onClick={() => deleteTask(index)}
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        </div>

        {/* Add New To-Do Item */}
        <div className="pt-4">
          <input
            type="text"
            value={newTask}
            onChange={(e) => setNewTask(e.target.value)}
            placeholder="Add a new task..."
            className="w-full p-2 text-gray-600 border rounded-lg focus:ring-blue-500 focus:border-blue-500"
          />
          <button
            onClick={addTask}
            className="mt-2 bg-blue-500 text-white px-4 py-2 rounded-lg w-full"
          >
            Add Task
          </button>
        </div>
      </div>
    </div>
  );
}
