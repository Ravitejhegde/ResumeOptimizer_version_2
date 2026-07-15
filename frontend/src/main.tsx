import React from "react";
import ReactDOM from "react-dom/client";

import App from "./app/App";

import "./styles/global.css";

import { ResumeProvider } from "./context/ResumeContext";

ReactDOM.createRoot(
    document.getElementById("root")!
).render(

    <React.StrictMode>

        <ResumeProvider>

            <App/>

        </ResumeProvider>

    </React.StrictMode>

);