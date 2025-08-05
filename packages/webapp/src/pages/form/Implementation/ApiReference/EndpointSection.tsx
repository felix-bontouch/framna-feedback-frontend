import { ReactNode } from 'react'

import { httpMethods } from './utils'

interface EndpointSectionProps {
  method: 'GET' | 'POST' | 'PUT' | 'DELETE'
  path: string
  description: string
  children: ReactNode
  examples: ReactNode
}

export default function EndpointSection({
  method,
  path,
  description,
  children,
  examples
}: EndpointSectionProps) {
  const methodStyles = httpMethods[method]

  return (
    <div className="border-b border-slate-200 last:border-b-0 dark:border-slate-700">
      <div className="grid grid-cols-1 divide-y divide-slate-200 lg:grid-cols-2 lg:divide-x lg:divide-y-0 dark:divide-slate-700">
        {/* Left side - API Details */}
        <div className="p-6 lg:p-8">
          <div className="space-y-6">
            {/* Endpoint header */}
            <div>
              <div className="mb-3 flex items-center gap-3">
                <span
                  className={`inline-flex items-center rounded-md border px-2.5 py-1 text-xs font-semibold ${methodStyles.color} ${methodStyles.darkColor}`}
                >
                  {method}
                </span>
                <code className="font-mono text-sm text-slate-700 dark:text-slate-300">{path}</code>
              </div>
              <p className="text-sm text-slate-600 dark:text-slate-400">{description}</p>
            </div>

            {/* API details content */}
            {children}
          </div>
        </div>

        {/* Right side - Examples */}
        <div className="bg-slate-50/50 p-6 lg:p-8 dark:bg-slate-900/20">
          <div className="space-y-4">{examples}</div>
        </div>
      </div>
    </div>
  )
}
