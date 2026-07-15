import { useState } from "react";

import type { AppState } from "../types/app";

import AppStateRenderer from "./AppStateRenderer";

function App() {

    const [state] =
        useState<AppState>("EMPTY");

    return (

        <AppStateRenderer
            state={state}
        />

    );

}

export default App;