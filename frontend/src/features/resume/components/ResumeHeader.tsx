import { Download } from "lucide-react";


interface ResumeHeaderProps {
    resume: any;
}


export const ResumeHeader = ({
    resume,
}: ResumeHeaderProps) => {


    const uploadedDate = resume?.created_at
        ? new Date(resume.created_at).toLocaleDateString()
        : "";



    return (

        <div className="
            flex
            items-start
            justify-between
            gap-4
        ">


            <div>

                <h1 className="
                    text-2xl
                    font-semibold
                    text-white
                ">
                    Resume Analysis
                </h1>



                <div className="
                    mt-2
                    flex
                    flex-wrap
                    items-center
                    gap-3
                    text-sm
                    text-white/60
                ">


                    <span>
                        {resume?.original_file_name ?? "Resume.pdf"}
                    </span>



                    <span className="
                        rounded-full
                        bg-green-500/10
                        px-2.5
                        py-1
                        text-xs
                        font-medium
                        text-green-400
                    ">

                        {
                            resume?.status ?? "Active"
                        }

                    </span>



                    <span>

                        Uploaded {uploadedDate}

                    </span>



                </div>


            </div>




            <button
                type="button"
                className="
                inline-flex
                items-center
                justify-center
                gap-2
                rounded-xl
                border
                border-white/10
                bg-white/5
                px-4
                py-2
                text-sm
                font-medium
                text-white
                transition
                hover:bg-white/10
                "
            >

                <Download className="h-4 w-4" />

                Download Report


            </button>



        </div>

    );
};
