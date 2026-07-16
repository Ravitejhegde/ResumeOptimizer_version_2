import { AppProvider } from "../context/AppContext";

import AppStateRenderer from "./AppStateRenderer";

function App() {

    return (

        <AppProvider>

            <AppStateRenderer />

        </AppProvider>

    );

}

export default App;