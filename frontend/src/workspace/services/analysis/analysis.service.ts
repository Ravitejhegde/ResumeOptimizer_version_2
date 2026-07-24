import api from "../api/client";

import type {

    AnalysisRequest,

    AnalysisResponse

} from "./analysis.types";

export const analyzeResume = async (

    data: AnalysisRequest

): Promise<AnalysisResponse> => {

    const response = await api.post(

        "/analysis/match",

        data

    );

    return response.data;

};