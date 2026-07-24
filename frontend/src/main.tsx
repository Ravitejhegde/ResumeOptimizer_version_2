import React from "react";
import ReactDOM from "react-dom/client";

import "./workspace/styles/globals.css";
import App from "./workspace/app/App";

ReactDOM.createRoot(
  document.getElementById("root")!
).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);