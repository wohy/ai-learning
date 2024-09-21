import * as React from "react";
import { Typography, Container } from "@mui/material";

export const ErrorPage = () => {
  return (
    <Container
      maxWidth="sm"
      style={{
        height: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div className="flex flex-col items-center justify-center h-full">
        <Typography variant="h1" className="text-red-500">
          ERROR
        </Typography>
        <Typography variant="h4" className="mt-4">
          Page ERROR
        </Typography>
        <Typography variant="body1" className="mt-2 text-gray-600">
          GET TEH AI RESPONSE FAILED
        </Typography>
      </div>
    </Container>
  );
}
