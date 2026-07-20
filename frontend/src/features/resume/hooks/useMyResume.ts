import { useQuery } from "@tanstack/react-query";

import { getMyResume } from "../api/resume.api";

export const useMyResume = () => {
    return useQuery({
        queryKey: ["my-resume"],
        queryFn: getMyResume,

        refetchInterval: (query) => {
            const latestResume = query.state.data?.data?.[0];

            if (
                latestResume?.status === "queued" ||
                latestResume?.status === "processing"
            ) {
                return 1000;
            }

            return false;
        },
    });
};
