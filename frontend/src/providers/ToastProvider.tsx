import { Toaster } from "sonner";

export function ToastProvider() {
    return (
        <Toaster
            position="top-center"
            richColors
            closeButton
            duration={4000}
            visibleToasts={3}
            expand={false}
            toastOptions={{
                className: "text-sm",
            }}
        />
    );
}
