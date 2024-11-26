"use client";

import { useState } from "react";
import { Box, Typography, Button, TextField } from "@mui/material";
import { blue } from "@mui/material/colors";
import { useActions } from "@/utils/client";
import { EndpointsContext } from "@/app/agent";
import { LocalContext } from "@/app/shared";

const Chat = () => {
  const actions = useActions<typeof EndpointsContext>();

  const [elements, setElements] = useState<JSX.Element[]>([]);
  const [history, setHistory] = useState<[role: string, content: string][]>([]);
  const [input, setInput] = useState("");
  const [selectedFile, setSelectedFile] = useState<File>();

  async function onSubmit(input: string) {
    const newElements = [...elements];
    let base64File: string | undefined = undefined;
    let fileExtension = selectedFile?.type.split("/")[1];

    if (selectedFile) {
      base64File = await convertFileToBase64(selectedFile);
    }

    const element = await actions.agent({
      input,
      chat_history: history,
      file:
        base64File && fileExtension
          ? {
              base64: base64File,
              extension: fileExtension,
            }
          : undefined,
    });

    newElements.push(
      <Box key={history.length} sx={{ display: "flex", flexDirection: "column", alignItems: "flex-end", mb: 1 }}>
        <Box sx={{ backgroundColor: blue[700], color: "white", borderRadius: 2, p: 1, maxWidth: "70%" }}>
          <Typography>{input}</Typography>
        </Box>
        <Box sx={{ backgroundColor: "#f3f4f6", borderRadius: 2, p: 1, maxWidth: "70%", mt: 1 }}>
          <Typography>{element.ui}</Typography>
        </Box>
      </Box>
    );

    // Process response asynchronously to get the last event
    (async () => {
      let lastEvent = await element.lastEvent;
      if (Array.isArray(lastEvent)) {
        if (lastEvent[0].invoke_model && lastEvent[0].invoke_model.result) {
          setHistory((prev) => [
            ...prev,
            ["human", input],
            ["ai", lastEvent[0].invoke_model.result],
          ]);
        } else if (lastEvent[1].invoke_tools) {
          setHistory((prev) => [
            ...prev,
            ["human", input],
            [
              "ai",
              `Tool result: ${JSON.stringify(lastEvent[1].invoke_tools.tool_result, null)}`,
            ],
          ]);
        } else {
          setHistory((prev) => [...prev, ["human", input]]);
        }
      } else if (lastEvent.invoke_model && lastEvent.invoke_model.result) {
        setHistory((prev) => [
          ...prev,
          ["human", input],
          ["ai", lastEvent.invoke_model.result],
        ]);
      }
    })();

    setElements(newElements);
    setInput("");
    setSelectedFile(undefined);
  }

  function convertFileToBase64(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const base64String = reader.result as string;
        resolve(base64String.split(",")[1]);
      };
      reader.onerror = (error) => {
        reject(error);
      };
      reader.readAsDataURL(file);
    });
  }

  return (
    <Box sx={{ display: "flex", flexDirection: "column", height: "100%", backgroundColor: "white", borderRadius: 1, boxShadow: 2 }}>
      {/* Header */}
      <Box sx={{ backgroundColor: blue[700], color: "white", p: 2, textAlign: "center", fontWeight: "bold", borderRadius: "8px 8px 0 0" }}>
        SNOOZE
      </Box>

      {/* Messages Area */}
      <Box sx={{ flex: 1, overflowY: "auto", p: 2, display: "flex", flexDirection: "column" }}>
        {elements}
      </Box>

      {/* Input Area */}
      <Box
        component="form"
        onSubmit={async (e) => {
          e.preventDefault();
          await onSubmit(input);
        }}
        sx={{
          display: "flex",
          alignItems: "center",
          p: 2,
          borderTop: "1px solid #e0e0e0",
          backgroundColor: "#f9f9f9",
        }}
      >
        <TextField
          variant="outlined"
          size="small"
          fullWidth
          placeholder="Type a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          sx={{ mr: 1 }}
        />
        <Button variant="contained" color="primary" type="submit" sx={{ height: "40px" }}>
          Send
        </Button>
      </Box>
    </Box>
  );
};

export default Chat;
