import { AuthProvider } from '../contexts/AuthContext'
import { Providers } from '../components/Providers'
import '../styles/globals.css'

export const metadata = {
  title: 'CV Builder - AI-Powered Resume Generator',
  description: 'Generate professional, tailored resumes using AI technology',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body suppressHydrationWarning={true}>
        <Providers>
          <AuthProvider>
            {children}
          </AuthProvider>
        </Providers>
      </body>
    </html>
  )
}
