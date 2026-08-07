import { useState } from "react";

import { EmptyResumeState } from "../components/EmptyResumeState";
import { ProcessingResumeState } from "../components/ProcessingResumeState";
import { ResumeAnalysis } from "../components/ResumeAnalysis";
import { UploadResumeModal } from "../components/UploadResumeModal";

import { useMyResume } from "../hooks/useMyResume";
import { useUploadResume } from "../hooks/useUpload";
import { useResumeAnalysis } from "../hooks/useResumeAnalysis";


export const ResumePage = () => {


    const [
        isUploadModalOpen,
        setIsUploadModalOpen
    ] = useState(false);



    const uploadResumeMutation =
        useUploadResume();



    const {
        data,
        isLoading,
        isError,
        error,
    } = useMyResume();




    const latestResume =
        data?.data?.[0];



    const resumeId =
        latestResume?.id;



    const resumeStatus =
        latestResume?.status?.toLowerCase();





    const {
        data: analysisResponse,
        isLoading: analysisLoading,
        isError: analysisError,
    } = useResumeAnalysis(
        resumeId,
        resumeStatus === "analyzed"
    );



    const analysis =
        analysisResponse;

        console.log(analysis)






    const handleResumeUpload = (
        file: File
    ) => {


        uploadResumeMutation.mutate(
            file,
            {

                onSuccess: (response) => {

                    console.log(
                        "Resume uploaded successfully:",
                        response
                    );


                    setIsUploadModalOpen(false);

                },


                onError: (error) => {

                    console.error(
                        "Resume upload failed:",
                        error
                    );

                },

            }
        );

    };






    if (isLoading) {

        return (

            <section
                className="
                flex
                min-h-full
                items-center
                justify-center
                p-8
                text-white
                "
            >

                <p className="
                    text-sm
                    text-white/50
                ">

                    Loading resume...

                </p>


            </section>

        );

    }







    if (isError) {


        console.error(
            error
        );


        return (

            <section
                className="
                flex
                min-h-full
                items-center
                justify-center
                p-8
                "
            >

                <div
                    className="
                    rounded-xl
                    border
                    border-red-500/20
                    bg-red-500/10
                    p-5
                    "
                >

                    <h2
                        className="
                        font-semibold
                        text-red-400
                        "
                    >

                        Unable to load resume

                    </h2>


                </div>


            </section>

        );

    }







    let content;






    if (
        resumeStatus === "uploaded" ||
        resumeStatus === "queued" ||
        resumeStatus === "processing"
    ) {

        content = (

            <ProcessingResumeState />

        );

    }






    else if (
        resumeStatus === "analyzed"
    ) {



        if (
            analysisLoading
        ) {

            content = (

                <section
                    className="
                    p-8
                    text-white
                    "
                >

                    Loading analysis...


                </section>

            );

        }



        else if (
            analysisError ||
            !analysis
        ) {

            content = (

                <section
                    className="
                    p-8
                    text-white
                    "
                >

                    <div
                        className="
                        rounded-xl
                        border
                        border-red-500/20
                        bg-red-500/10
                        p-5
                        "
                    >

                        Unable to load resume analysis.


                    </div>


                </section>

            );


        }



        else {


            content = (

                <section
                    className="
                    min-h-full
                    text-white
                    "
                >


                    <ResumeAnalysis

                        analysis={
                            analysis
                        }


                        resume={
                            latestResume
                        }

                    />



                    <div
                        className="
                        mt-8
                        flex
                        justify-center
                        "
                    >

                        <button

                            type="button"

                            onClick={() =>
                                setIsUploadModalOpen(true)
                            }

                            className="
                            rounded-xl
                            bg-violet-600
                            px-5
                            py-2.5
                            text-sm
                            font-medium
                            text-white
                            transition
                            hover:bg-violet-500
                            "
                        >

                            Upload New Resume


                        </button>


                    </div>


                </section>

            );


        }


    }







    else if (
        resumeStatus === "failed"
    ) {
        content = (
            <section
                className="
                min-h-full
                text-white
                "
            >

                <div
                    className="
                    mx-auto
                    max-w-3xl
                    rounded-2xl
                    border
                    border-red-500/20
                    bg-[#0b0f17]
                    p-6
                    "
                >

                    <h1
                        className="
                        text-xl
                        font-semibold
                        text-red-400
                        "
                    >

                        Resume analysis failed

                    </h1>



                    <p
                        className="
                        mt-2
                        text-sm
                        text-white/50
                        "
                    >

                        Please upload your resume again.


                    </p>




                    {
                        latestResume?.failure_reason && (

                            <p
                                className="
                                mt-4
                                rounded-xl
                                bg-red-500/10
                                p-4
                                text-sm
                                text-red-300
                                "
                            >

                                {
                                    latestResume.failure_reason
                                }


                            </p>

                        )
                    }



                    <button

                        onClick={() =>
                            setIsUploadModalOpen(true)
                        }


                        className="
                        mt-6
                        rounded-xl
                        bg-violet-600
                        px-5
                        py-2.5
                        text-sm
                        font-medium
                        text-white
                        hover:bg-violet-500
                        "
                    >

                        Upload Resume Again


                    </button>


                </div>


            </section>

        );


    }






    else {


        content = (

            <EmptyResumeState

                onUploadClick={() =>
                    setIsUploadModalOpen(true)
                }

            />

        );


    }







    return (

        <>


            {content}



            <UploadResumeModal

                open={
                    isUploadModalOpen
                }


                onClose={() =>
                    setIsUploadModalOpen(false)
                }


                onUpload={
                    handleResumeUpload
                }


                isUploading={
                    uploadResumeMutation.isPending
                }

            />


        </>


    );

};
