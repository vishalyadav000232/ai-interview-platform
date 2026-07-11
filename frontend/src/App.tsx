
import './App.css'
import { useAuthBootstrap } from './features/auth/hooks/useAuthBootstrap'
import { AuthProvider } from './providers/AuthProvider'
import { QueryProvider } from './providers/QueryProvider'
import { ToastProvider } from './providers/TostProvideer'
import AppRoutes from './routes/AppRoutes'

function App() {
  useAuthBootstrap();

  return(

    <QueryProvider>
      <AuthProvider>
      <ToastProvider/>
      <AppRoutes />

      </AuthProvider>

    </QueryProvider>
  )
}

export default App
