import { BrowserRouter as Router } from 'react-router-dom'
import { Provider } from 'react-redux'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { store } from '@/shared/store/store'

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
})

function App() {
  return (
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>
        <Router>
          <div className="min-h-screen bg-background">
            <div className="container mx-auto p-8">
              <h1 className="text-4xl font-bold text-primary mb-4">
                NTT Data Regulatory Reporting System
              </h1>
              <p className="text-muted-foreground">
                AI-Powered Regulatory Compliance Automation Platform
              </p>
              <div className="mt-8 p-6 border rounded-lg">
                <h2 className="text-2xl font-semibold mb-4">Welcome</h2>
                <p>
                  The application is being set up. Please run the backend with{' '}
                  <code className="bg-muted px-2 py-1 rounded">python app.py</code>
                </p>
              </div>
            </div>
          </div>
        </Router>
      </QueryClientProvider>
    </Provider>
  )
}

export default App
