import { useMutation } from "@tanstack/react-query";
import { downloadResume } from "../api/resume.api";

export const useDownloadResume = () => {

    return useMutation({

        mutationFn: downloadResume,

    });

};
