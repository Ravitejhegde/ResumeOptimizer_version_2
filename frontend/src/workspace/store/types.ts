import type {
  Dispatch,
  SetStateAction,
} from "react";

/* =========================================================
   Workflow
========================================================= */

export type WorkspaceStep =
  | "analysis"
  | "optimization"
  | "register"
  | "login"
  | "pricing";

/* =========================================================
   Resume
========================================================= */

export interface ResumeInfo {
  id: string;

  filename: string;

  storedFilename: string;
}

/* =========================================================
   Authenticated User
========================================================= */

export interface CurrentUser {
  id: string;

  name: string;

  email: string;

  verified: boolean;
}

/* =========================================================
   Workspace State
========================================================= */

export interface WorkspaceState {

  /* -----------------------------------------
     Workflow
  ----------------------------------------- */

  step: WorkspaceStep;

  /* -----------------------------------------
     Resume
  ----------------------------------------- */

  resume: ResumeInfo | null;

  /* -----------------------------------------
     Job Description
  ----------------------------------------- */

  jobDescription: string;

  /* -----------------------------------------
     Analysis
  ----------------------------------------- */

    atsScore: number;

  role: string;

  roleId: string;

  experience: number;

matchedSkills: string[];

missingSkills: string[];

matchedTechnologies: string[];

missingTechnologies: string[];

selectedSkills: string[];

  /* -----------------------------------------
     Optimization
  ----------------------------------------- */

  optimizedFilename: string;

  previewBlocks: any[];

  previewLayout: any;

  /* -----------------------------------------
     Authentication
  ----------------------------------------- */

  user: CurrentUser | null;

  isAuthenticated: boolean;

  /* -----------------------------------------
     Free Sample
  ----------------------------------------- */

  isFreeSample: boolean;

  sampleCompleted: boolean;
}

/* =========================================================
   Workspace Context
========================================================= */

export interface WorkspaceContextType {

  state: WorkspaceState;

  setState: Dispatch<
    SetStateAction<WorkspaceState>
  >;
}