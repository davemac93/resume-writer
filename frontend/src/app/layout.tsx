import QueryProvider from "../components/providers/query-provider";
import "../styles/globals.css";

export const metadata = {
  title: 'Resume Writer',
  description: 'AI-powered resume generator',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <QueryProvider>
          {children}
        </QueryProvider>
      </body>
    </html>
  )
}
