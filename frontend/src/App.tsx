import "./App.css";

import { useAuthBootstrap } from "./features/auth/hooks/useAuthBootstrap";

import { QueryProvider } from "./providers/QueryProvider";
import { ToastProvider } from "./providers/ToastProvider";

import AppRoutes from "./routes/AppRoutes";

function AppBootstrap() {
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
      <AppBootstrap />
    </QueryProvider>
  );
}

export default App;
