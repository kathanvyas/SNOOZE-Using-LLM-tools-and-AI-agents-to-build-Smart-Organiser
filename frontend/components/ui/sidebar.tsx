import React from "react";
import { IconButton, Box } from "@mui/material";
import MailIcon from "@mui/icons-material/Mail";
import ListAltIcon from "@mui/icons-material/ListAlt";
import CalendarTodayIcon from "@mui/icons-material/CalendarToday";
import SettingsIcon from "@mui/icons-material/Settings";
import { blue } from "@mui/material/colors";

const Sidebar = ({ setActiveSection }) => {
  return (
    <Box
      sx={{
        width: 64,
        height: "100vh",
        bgcolor: blue[800],
        color: "white",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        py: 2,
      }}
    >
      <IconButton onClick={() => setActiveSection("email")} sx={{ color: blue[200], mb: 4 }}>
        <MailIcon fontSize="large" />
      </IconButton>
      <IconButton onClick={() => setActiveSection("todo")} sx={{ color: blue[200], mb: 4 }}>
        <ListAltIcon fontSize="large" />
      </IconButton>
      <IconButton onClick={() => setActiveSection("calendar")} sx={{ color: blue[200], mb: 4 }}>
        <CalendarTodayIcon fontSize="large" />
      </IconButton>
      <IconButton onClick={() => setActiveSection("settings")} sx={{ color: blue[200] }}>
        <SettingsIcon fontSize="large" />
      </IconButton>
    </Box>
  );
};

export default Sidebar;
