import {
    createContext,
    useContext,
    useState,
} from "react";

import type { ReactNode } from "react";

import type { AppState } from "../types/app";
import type { MatchResult } from "../types/match";
import type {
    JobDescriptionAnalysis,
    UploadResponse,
} from "../types/analysis";

type AppContextType = {

    state: AppState;
    setState: React.Dispatch<
        React.SetStateAction<AppState>
    >;

    resume: UploadResponse | null;
    setResume: React.Dispatch<
        React.SetStateAction<UploadResponse | null>
    >;

    jobDescription: string;
    setJobDescription: React.Dispatch<
        React.SetStateAction<string>
    >;

    jdAnalysis: JobDescriptionAnalysis | null;
    setJdAnalysis: React.Dispatch<
        React.SetStateAction<JobDescriptionAnalysis | null>
    >;

    matchResult: MatchResult | null;
    setMatchResult: React.Dispatch<
        React.SetStateAction<MatchResult | null>
    >;

    loading: boolean;
    setLoading: React.Dispatch<
        React.SetStateAction<boolean>
    >;

    error: string;
    setError: React.Dispatch<
        React.SetStateAction<string>
    >;

};

const AppContext =
    createContext<AppContextType | null>(null);

export function AppProvider({

    children,

}: {

    children: ReactNode;

}) {

    const [state, setState] =
        useState<AppState>("EMPTY");

    const [resume, setResume] =
        useState<UploadResponse | null>(null);

    const [jobDescription, setJobDescription] =
        useState("");

    const [jdAnalysis, setJdAnalysis] =
        useState<JobDescriptionAnalysis | null>(null);

    const [matchResult, setMatchResult] =
        useState<MatchResult | null>(null);

    const [loading, setLoading] =
        useState(false);

    const [error, setError] =
        useState("");

    return (

        <AppContext.Provider

            value={{

                state,
                setState,

                resume,
                setResume,

                jobDescription,
                setJobDescription,

                jdAnalysis,
                setJdAnalysis,

                matchResult,
                setMatchResult,

                loading,
                setLoading,

                error,
                setError,

            }}

        >

            {children}

        </AppContext.Provider>

    );

}

export function useApp() {

    const context =
        useContext(AppContext);

    if (!context) {

        throw new Error(
            "useApp must be used inside AppProvider"
        );

    }

    return context;

}