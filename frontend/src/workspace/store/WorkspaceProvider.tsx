import { useState } from "react";

import { WorkspaceContext } from "./WorkspaceContext";

import type {
    WorkspaceState
} from "./types";

import type {
    ReactNode
} from "react";

interface Props {

    children: ReactNode;

}

const initialState: WorkspaceState = {

    step: "analysis",

    resume: null,

    jobDescription: "",

    atsScore: 0,

    role: "",

    experience: 0,

    matchedSkills: [],

    missingSkills: [],

    selectedSkills: [],

    optimizedFilename: "",

    previewBlocks: [],

    previewLayout: {}

};

const WorkspaceProvider = ({
    children
}: Props) => {

    const [state, setState] =
        useState<WorkspaceState>(initialState);

    return (

        <WorkspaceContext.Provider
            value={{
                state,
                setState
            }}
        >

            {children}

        </WorkspaceContext.Provider>

    );

};

export default WorkspaceProvider;