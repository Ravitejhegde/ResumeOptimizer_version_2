import { createContext } from "react";

import type { WorkspaceContextType } from "./types";

export const WorkspaceContext =
    createContext<WorkspaceContextType | null>(null);