import { IconCheck, IconCopy } from '@tabler/icons-react'
import { useState } from 'react'

import { Button } from '@/components'

interface CodeExampleProps {
  title: string
  code: string
  language?: string
}

export default function CodeExample({ title, code }: CodeExampleProps) {
  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    navigator.clipboard.writeText(code)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="overflow-hidden rounded-lg border border-slate-200 dark:border-slate-700">
      <div className="flex items-center justify-between bg-slate-50 px-4 py-2 dark:bg-slate-800">
        <span className="text-sm font-medium text-slate-700 dark:text-slate-300">{title}</span>
        <Button size="sm" iconOnly onClick={handleCopy} className="!h-7 !w-7">
          {copied ? <IconCheck className="h-4 w-4" /> : <IconCopy className="h-4 w-4" />}
        </Button>
      </div>
      <div className="overflow-x-auto bg-slate-900 p-4 dark:bg-slate-950">
        <pre className="text-xs text-slate-100">
          <code>{code}</code>
        </pre>
      </div>
    </div>
  )
}
