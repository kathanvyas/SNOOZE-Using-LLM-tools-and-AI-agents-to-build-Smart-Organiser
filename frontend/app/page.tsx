"use client";

import { useState } from "react";
import Chat from "@/components/prebuilt/chat";
import Sidebar from "@/components/ui/sidebar";
import Calendar from "@/components/ui/calendar";
import Email from "@/components/ui/email";
import ToDoList from "@/components/ui/todoList";

export default function Home() {
  const [activeSection, setActiveSection] = useState("calendar");
  const [chatMessages, setChatMessages] = useState([]);

  const handleSendToChat = (message) => {
    setChatMessages((prev) => [...prev, { role: "user", content: message }]);
  };

  const renderMainContent = () => {
    switch (activeSection) {
      case "calendar":
        return <Calendar />;
      case "email":
        return <Email onSend={handleSendToChat} />;
      case "todo":
        return <ToDoList />;
      default:
        return <Calendar />;
    }
  };

  return (
    <main className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <Sidebar setActiveSection={setActiveSection} />

      {/* Main Content Area */}
      <div className="flex-grow p-4 bg-gray-100 overflow-y-auto" style={{ width: "50%" }}>
        {renderMainContent()}
      </div>

      {/* Chat Area with 50% Width */}
      <div
        style={{ width: "50%" }}
        className="p-4 border-l border-gray-300 overflow-y-auto bg-white flex flex-col justify-between"
      >
        <Chat messages={chatMessages} />
      </div>
    </main>
  );
}
