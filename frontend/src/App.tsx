
import './App.css'
import { AuthProvider } from './providers/AuthProvider'
import { QueryProvider } from './providers/QueryProvider'
import { ToastProvider } from './providers/TostProvideer'
import AppRoutes from './routes/AppRoutes'

function App() {


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
