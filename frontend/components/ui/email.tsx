import React, { useState } from "react";
import { Box, Card, Typography, TextField, Button } from "@mui/material";
import { useActions } from "@/utils/client";
import { EndpointsContext } from "@/app/agent";

const Email = () => {
  const actions = useActions<typeof EndpointsContext>();
  const [draftMessage, setDraftMessage] = useState(`Hi Jane,

Thank you for the invitation to the Design Thinking Workshop. I am very interested in attending and would love to learn more about the principles of design thinking.

Could you please send me more details about the event schedule and the topics that will be covered?

Looking forward to your response.

Best,
Adam`);

  const handleSend = async () => {
    if (draftMessage.trim()) {
      await actions.agent({ 
        input: draftMessage, 
        chat_history: [] 
      });
      setDraftMessage(""); 
    }
  };

  return (
    <Box sx={{ p: 6, backgroundColor: "#f9fafb", height: "100vh", display: "flex", flexDirection: "column" }}>
      {/* Email Display */}
      <Card variant="outlined" sx={{ mb: 4, p: 4, boxShadow: 1, borderRadius: 2 }}>
        {/* Email Header */}
        <Box sx={{ borderBottom: 1, borderColor: "grey.200", pb: 2, mb: 3 }}>
          <Typography variant="h6" fontWeight="bold" color="text.primary">
            Subject: Design Thinking Workshop
          </Typography>
          <Typography variant="body2" color="text.secondary">
            From: Jane Doe <span style={{ color: "#3b82f6" }}>jane.doe@example.com</span>
          </Typography>
          <Typography variant="body2" color="text.secondary">
            To: Adam Williams <span style={{ color: "#3b82f6" }}>info@gmail.com</span>
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Date: Mon, 23 Jan 2023 09:30
          </Typography>
        </Box>
        {/* Email Body */}
        <Box>
          <Typography variant="body1" color="text.primary" paragraph>
            Dear Adam,
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            I hope this email finds you well. I wanted to reach out to invite you to our upcoming Design Thinking Workshop. It's a hands-on event where you'll learn the principles of design thinking and how to apply them to your projects.
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            Please let me know if you're interested in attending.
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Best regards,
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Jane Doe
          </Typography>
        </Box>
      </Card>

      {/* Draft Reply */}
      <Card variant="outlined" sx={{ p: 3, boxShadow: 1, borderRadius: 2, flexGrow: 0, display: "flex", flexDirection: "column" }}>
        {/* Draft Header */}
        <Box sx={{ borderBottom: 1, borderColor: "grey.200", pb: 2, mb: 2 }}>
          <Typography variant="h6" fontWeight="bold" color="text.primary">
            Draft Reply
          </Typography>
        </Box>

        {/* Draft Body */}
        <TextField
          multiline
          rows={4}
          fullWidth
          value={draftMessage}
          onChange={(e) => setDraftMessage(e.target.value)}
          placeholder="Start typing your reply here..."
          variant="outlined"
          sx={{
            "& .MuiOutlinedInput-root": {
              p: 2,
              borderRadius: 2,
              borderColor: "grey.300",
              "&:hover": {
                borderColor: "#3b82f6",
              },
              "&.Mui-focused": {
                borderColor: "#3b82f6",
              },
            },
            textarea: {
              color: "text.secondary",
            },
            mb: 2,
          }}
        />

        {/* Send Button */}
        <Button
          onClick={handleSend}
          variant="contained"
          color="primary"
          sx={{
            alignSelf: "flex-end",
            width: "100px",
          }}
        >
          Send
        </Button>
      </Card>
    </Box>
  );
};

export default Email;
