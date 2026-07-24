import AppLayout from "../layout/AppLayout/AppLayout";

import WorkspaceProvider from "../store/WorkspaceProvider";
import { useWorkspace } from "../store/useWorkspace";

import AnalysisWorkspace from "../screens/AnalysisWorkspace";
import OptimizationWorkspace from "../screens/OptimizationWorkspace";

const WorkspaceRouter = () => {

    const { state } = useWorkspace();

    switch (state.step) {

        case "optimization":

            return <OptimizationWorkspace />;

        default:

            return <AnalysisWorkspace />;

    }

};

const App = () => {

    return (

        <WorkspaceProvider>

            <AppLayout>

                <WorkspaceRouter />

            </AppLayout>

        </WorkspaceProvider>

    );

};

export default App;