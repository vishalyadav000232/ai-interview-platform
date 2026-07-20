import { Check, LoaderCircle } from "lucide-react";

export const ProcessingResumeState = () => {
    return (
        <section className="min-h-full p-8 text-white">
            <div className="mx-auto max-w-3xl">
                <h1 className="text-2xl font-semibold">
                    Analyzing Your Resume
                </h1>

                <p className="mt-2 text-sm text-white/50">
                    Our AI is reviewing your resume. This may take a few seconds.
                </p>

                <div className="mt-8 space-y-3 rounded-xl border border-white/10 bg-[#0b0f17] p-5">
                    <div className="flex items-center gap-3">
                        <Check className="h-5 w-5 text-green-400" />
                        <span>Resume uploaded successfully</span>
                    </div>

                    <div className="flex items-center gap-3">
                        <LoaderCircle className="h-5 w-5 animate-spin text-violet-400" />
                        <span>Extracting text and analyzing skills</span>
                    </div>
                </div>
            </div>
        </section>
    );
};
