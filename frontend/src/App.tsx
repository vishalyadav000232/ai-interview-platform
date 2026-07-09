
import './App.css'
import { QueryProvider } from './providers/QueryProvider'
import { ToastProvider } from './providers/TostProvideer'
import AppRoutes from './routes/AppRoutes'

function App() {


  return(

    <QueryProvider>
      <ToastProvider/>
      <AppRoutes />

    </QueryProvider>
  )
}

export default App
