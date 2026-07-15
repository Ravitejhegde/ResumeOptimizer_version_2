import type { AppState } from "../types/app";

import EmptyScreen from "../screens/Empty/EmptyScreen";
import AnalysisScreen from "../screens/Analysis/AnalysisScreen";
import MatchCenterScreen from "../screens/MatchCenter/MatchCenterScreen";

type Props = {
    state: AppState;
};

export default function AppStateRenderer({
    state,
}: Props) {

    switch (state) {

        case "EMPTY":
            return <EmptyScreen />;

        case "ANALYZING":
            return <AnalysisScreen />;
            
        case "MATCH":
            return <MatchCenterScreen />;

        default:
            return <EmptyScreen />;

    }
}