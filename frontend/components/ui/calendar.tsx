import React from "react";
import { Box, Typography, Grid, Card } from "@mui/material";

const Calendar = () => {
  return (
    <Box sx={{ width: "100%", height: "100%", p: 3, backgroundColor: "#f9fafb", display: "flex", justifyContent: "center", alignItems: "center" }}>
      <Card sx={{ width: "100%", height: "100%", p: 3, borderRadius: 2, boxShadow: 2 }}>
        <Typography variant="h5" sx={{ fontWeight: "bold", mb: 3, textAlign: "center" }}>
          November 2024
        </Typography>
        
        {/* Days of the Week */}
        <Grid container spacing={1} sx={{ mb: 1 }}>
          {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((day) => (
            <Grid item xs={12 / 7} key={day}>
              <Typography variant="body2" fontWeight="bold" textAlign="center">
                {day}
              </Typography>
            </Grid>
          ))}
        </Grid>

        {/* Calendar Days */}
        <Grid container spacing={1}>
          {[...Array(5)].map((_, i) => (
            <Grid item xs={12 / 7} key={`empty-${i}`} />
          ))}
          {[...Array(30)].map((_, day) => (
            <Grid item xs={12 / 7} key={day}>
              <Card
                variant="outlined"
                sx={{
                  height: "70px",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  borderRadius: 1,
                  backgroundColor: day + 1 === 15 || day + 1 === 22 || day + 1 === 29 ? "rgba(59, 130, 246, 0.1)" : "transparent",
                  borderColor: "rgba(229, 231, 235, 1)",
                }}
              >
                <Typography variant="body2" sx={{ fontWeight: "medium", mb: 0.5 }}>
                  {day + 1}
                </Typography>
                {day + 1 === 15 && (
                  <Typography sx={{ fontSize: "0.7rem", color: "#3b82f6", textAlign: "center" }}>
                    Mid-month Review
                  </Typography>
                )}
                {day + 1 === 22 && (
                  <Typography sx={{ fontSize: "0.7rem", color: "#3b82f6", textAlign: "center" }}>
                    Team Outing at 4 PM
                  </Typography>
                )}
                {day + 1 === 29 && (
                  <Typography sx={{ fontSize: "0.7rem", color: "#3b82f6", textAlign: "center" }}>
                    Project Deadline
                  </Typography>
                )}
              </Card>
            </Grid>
          ))}
        </Grid>
      </Card>
    </Box>
  );
};

export default Calendar;
