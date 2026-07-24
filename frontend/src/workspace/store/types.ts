export type WorkspaceStep =
    | "analysis"
    | "optimization";

export interface ResumeInfo {

    id: string;

    filename: string;

    storedFilename: string;

}

export interface WorkspaceState {

    step: WorkspaceStep;

    resume: ResumeInfo | null;

    jobDescription: string;

    atsScore: number;

    role: string;

    experience: number;

    matchedSkills: string[];

    missingSkills: string[];

    selectedSkills: string[];

    optimizedFilename: string;

    previewBlocks: any[];

    previewLayout: any;

}

export interface WorkspaceContextType {

    state: WorkspaceState;

    setState: React.Dispatch<
        React.SetStateAction<WorkspaceState>
    >;

}