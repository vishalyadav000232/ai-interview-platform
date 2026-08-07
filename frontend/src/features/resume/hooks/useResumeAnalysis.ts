import { useQuery } from "@tanstack/react-query";
import { getResumeAnalysis } from "../api/resume.api";


export const useResumeAnalysis = (
    resumeId?: string,
    enabled: boolean = false,
) => {

    return useQuery({

        queryKey: [
            "resume-analysis",
            resumeId,
        ],


        queryFn: () =>
            getResumeAnalysis(resumeId!),


        enabled:
            Boolean(resumeId) &&
            enabled,


        staleTime: 1000 * 60 * 5,


    });

};
