import { useCallback, useState } from "react";
import { FileText, UploadCloud, X } from "lucide-react";
import { useDropzone } from "react-dropzone";

type UploadResumeModalProps = {
    open: boolean;
    onClose: () => void;
    onUpload: (file: File) => void;
    isUploading : boolean
};

const MAX_FILE_SIZE = 5 * 1024 * 1024;

const acceptedFileTypes = {
    "application/pdf": [".pdf"],
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [
        ".docx",
    ],
};

export const UploadResumeModal = ({
    open,
    onClose,
    onUpload,
    isUploading
}: UploadResumeModalProps) => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [errorMessage, setErrorMessage] = useState("");

    const onDrop = useCallback((acceptedFiles: File[]) => {
        const file = acceptedFiles[0];

        if (!file) {
            return;
        }

        setSelectedFile(file);
        setErrorMessage("");
    }, []);

    const onDropRejected = useCallback(() => {
        setSelectedFile(null);
        setErrorMessage("Only PDF or DOCX files up to 5MB are supported.");
    }, []);

    const {
        getRootProps,
        getInputProps,
        isDragActive,
        open: openFilePicker,
    } = useDropzone({
        onDrop,
        onDropRejected,
        accept: acceptedFileTypes,
        maxSize: MAX_FILE_SIZE,
        maxFiles: 1,
        multiple: false,
        noClick: true,
        noKeyboard: true,
    });

    const handleRemoveFile = () => {
        setSelectedFile(null);
        setErrorMessage("");
    };

    const handleClose = () => {
        if(isUploading){
            return
        }
        setSelectedFile(null);
        setErrorMessage("");
        onClose();
    };

    const handleUpload = () => {
        if (!selectedFile) {
            setErrorMessage("Please select a resume first.");
            return;
        }

        onUpload(selectedFile);
    };

    if (!open) {
        return null;
    }

    return (
        <div
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4 backdrop-blur-sm"
            role="dialog"
            aria-modal="true"
            aria-labelledby="upload-resume-title"
        >
            <div className="w-full max-w-xl overflow-hidden rounded-2xl border border-white/10 bg-[#0b0f17] shadow-2xl">

                <header className="flex items-start justify-between border-b border-white/10 px-6 py-5">
                    <div>
                        <h2
                            id="upload-resume-title"
                            className="text-lg font-semibold text-white"
                        >
                            Upload Resume
                        </h2>

                        <p className="mt-1 text-sm text-slate-400">
                            Upload your resume to start the AI analysis.
                        </p>
                    </div>

                    <button
                        type="button"
                        onClick={handleClose}
                        disabled={isUploading}
                        className="flex h-9 w-9 items-center justify-center rounded-lg text-slate-400 transition-colors hover:bg-white/5 hover:text-white disabled:cursor-not-allowed disabled:opacity-40"
                    >
                        <X className="h-5 w-5" />
                    </button>
                </header>

                <div className="space-y-5 p-6">
                    {!selectedFile ? (
                        <div
                            {...getRootProps()}
                            className={`flex min-h-[280px] flex-col items-center justify-center rounded-2xl border border-dashed px-6 py-10 text-center transition-colors ${isDragActive
                                    ? "border-violet-400 bg-violet-500/10"
                                    : "border-white/15 bg-white/[0.02]"
                                }`}
                        >
                            <input {...getInputProps()} />

                            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-violet-500/10 text-violet-400">
                                <UploadCloud className="h-8 w-8" />
                            </div>

                            <h3 className="mt-5 text-base font-semibold text-white">
                                {isDragActive
                                    ? "Drop your resume here"
                                    : "Drag and drop your resume"}
                            </h3>

                            <p className="mt-2 text-sm text-slate-400">
                                You can also choose a file from your device.
                            </p>

                            <button
                                type="button"
                                onClick={openFilePicker}
                                className="mt-5 rounded-xl border border-white/10 bg-white/5 px-5 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-white/10"
                            >
                                Browse Files
                            </button>

                            <p className="mt-4 text-xs text-slate-500">
                                PDF or DOCX · Maximum file size 5MB
                            </p>
                        </div>
                    ) : (
                        <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
                            <div className="flex items-center gap-4">
                                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-violet-500/10 text-violet-400">
                                    <FileText className="h-6 w-6" />
                                </div>

                                <div className="min-w-0 flex-1">
                                    <p className="truncate text-sm font-semibold text-white">
                                        {selectedFile.name}
                                    </p>

                                    <p className="mt-1 text-xs text-slate-400">
                                        {formatFileSize(selectedFile.size)}
                                    </p>
                                </div>

                                <button
                                    type="button"
                                    onClick={handleRemoveFile}
                                    className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg text-slate-400 transition-colors hover:bg-red-500/10 hover:text-red-400"
                                    aria-label="Remove selected resume"
                                >
                                    <X className="h-5 w-5" />
                                </button>
                            </div>

                            <div className="mt-4 rounded-xl bg-emerald-500/10 px-4 py-3 text-sm text-emerald-400">
                                Resume is ready to upload.
                            </div>
                        </div>
                    )}

                    {errorMessage && (
                        <p
                            className="rounded-xl border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-400"
                            role="alert"
                        >
                            {errorMessage}
                        </p>
                    )}
                </div>


                <footer className="flex flex-col-reverse gap-3 border-t border-white/10 px-6 py-5 sm:flex-row sm:justify-end">
                    <button
                        type="button"
                        onClick={handleClose}
                        disabled={isUploading}
                        className="rounded-xl border border-white/10 px-5 py-2.5 text-sm font-semibold text-slate-300 transition-colors hover:bg-white/5 hover:text-white disabled:cursor-not-allowed disabled:opacity-40"
                    >
                        Cancel
                    </button>

                    <button
                        type="button"
                        onClick={handleUpload}
                        disabled={!selectedFile || isUploading}
                        className="inline-flex items-center justify-center gap-2 rounded-xl bg-violet-600 px-5 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-violet-500 disabled:cursor-not-allowed disabled:bg-violet-600/30 disabled:text-white/40"
                    >
                        {isUploading ? (
                            <>
                                <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                                Uploading...
                            </>
                        ) : (
                            <>
                                <UploadCloud className="h-4 w-4" />
                                Upload & Analyze
                            </>
                        )}
                    </button>
                </footer>
            </div>
        </div>
    );
};

const formatFileSize = (sizeInBytes: number) => {
    const sizeInMB = sizeInBytes / (1024 * 1024);

    if (sizeInMB < 1) {
        return `${Math.round(sizeInBytes / 1024)} KB`;
    }

    return `${sizeInMB.toFixed(2)} MB`;
};
