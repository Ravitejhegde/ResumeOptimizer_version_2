import type {
  Dispatch,
  SetStateAction,
} from "react";

export type WorkspaceStep =
  | "analysis"
  | "optimization";

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

  experience: number;

  matchedSkills: string[];

  missingSkills: string[];

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