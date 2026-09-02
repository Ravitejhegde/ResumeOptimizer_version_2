import AppLayout from "../layout/AppLayout/AppLayout";

import WorkspaceProvider from "../store/WorkspaceProvider";

import { useWorkspace } from "../store/useWorkspace";

import AnalysisWorkspace from "../screens/AnalysisWorkspace";

import OptimizationWorkspace from
  "../screens/OptimizationWorkspace";
import PricingPage from
  "../../features/billing/components/PricingPage";

/* =========================================================
   Workspace Router
========================================================= */

const WorkspaceRouter = () => {

  const {
    state,
  } = useWorkspace();

  switch (state.step) {

    case "optimization":

      return (
        <OptimizationWorkspace />
      );

    case "register":

      return (
        <div>
          Register screen coming next.
        </div>
      );

    case "login":

      return (
        <div>
          Login screen coming next.
        </div>
      );

    case "pricing":

  return (
    <PricingPage />
  );

    case "analysis":

    default:

      return (
        <AnalysisWorkspace />
      );
  }
};

/* =========================================================
   App
========================================================= */

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