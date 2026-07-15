import { createContext, useContext, useState } from "react";

type ResumeContextType = {
    resumeId: string;
    setResumeId: (id: string) => void;
};

const ResumeContext = createContext<ResumeContextType | null>(null);

export function ResumeProvider({
    children,
}: {
    children: React.ReactNode;
}) {

    const [resumeId, setResumeId] = useState("");

    return (
        <ResumeContext.Provider
            value={{
                resumeId,
                setResumeId,
            }}
        >
            {children}
        </ResumeContext.Provider>
    );
}

export function useResume() {

    const context = useContext(ResumeContext);

    if (!context) {
        throw new Error(
            "useResume must be used inside ResumeProvider"
        );
    }

    return context;
}