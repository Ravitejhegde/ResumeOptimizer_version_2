import { useApp } from "../context/AppContext";

import EmptyScreen from "../screens/Empty/EmptyScreen";
import MatchCenterScreen from "../screens/MatchCenter/MatchCenterScreen";

export default function AppStateRenderer() {

    const { state } = useApp();

    switch (state) {

        case "EMPTY":

        case "RESUME_UPLOADED":

        case "JD_READY":

        case "ANALYZING":

            return <EmptyScreen />;

        case "MATCH":

        case "OPTIMIZING":

        case "REVIEW":

        case "DOWNLOAD":

            return <MatchCenterScreen />;

        default:

            return <EmptyScreen />;

    }

}