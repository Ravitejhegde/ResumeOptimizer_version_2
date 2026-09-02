import { useState } from "react";

import { WorkspaceContext } from "./WorkspaceContext";

import type {
  WorkspaceState,
} from "./types";

import type {
  ReactNode,
} from "react";

interface Props {
  children: ReactNode;
}

/* =========================================================
   Initial Workspace State
========================================================= */

const initialState: WorkspaceState = {

  /* Workflow */

  step: "analysis",

  /* Resume */

  resume: null,

  /* Job Description */

  jobDescription: "",

  /* Analysis */

  atsScore: 0,

  role: "",

  experience: 0,

  matchedSkills: [],

  missingSkills: [],

  selectedSkills: [],

  /* Optimization */

  optimizedFilename: "",

  previewBlocks: [],

  previewLayout: {},

  /* Authentication */

  user: null,

  isAuthenticated: false,

  /* Free Sample */

  isFreeSample: true,

  sampleCompleted: false,
};

/* =========================================================
   Provider
========================================================= */

const WorkspaceProvider = ({
  children,
}: Props) => {

  const [state, setState] =
    useState<WorkspaceState>(
      initialState,
    );

  return (

    <WorkspaceContext.Provider
      value={{
        state,
        setState,
      }}
    >

      {children}

    </WorkspaceContext.Provider>
  );
};

export default WorkspaceProvider;