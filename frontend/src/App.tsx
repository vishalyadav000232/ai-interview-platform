import "./App.css";

import { useAuthBootstrap } from "./features/auth/hooks/useAuthBootstrap";

import { AuthProvider } from "./providers/AuthProvider";
import { QueryProvider } from "./providers/QueryProvider";
import { ToastProvider } from "./providers/ToastProvider";

import AppRoutes from "./routes/AppRoutes";

function AppContent() {
  useAuthBootstrap();

  return (
    <>
      <ToastProvider />
      <AppRoutes />
    </>
  );
}

function App() {
  return (
    <QueryProvider>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </QueryProvider>
  );
}

export default App;
