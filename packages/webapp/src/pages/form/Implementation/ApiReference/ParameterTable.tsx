interface Parameter {
  name: string
  type: string
  required: boolean
  description: string
  example?: any
}

interface ParameterTableProps {
  title: string
  parameters: Parameter[]
}

export default function ParameterTable({ title, parameters }: ParameterTableProps) {
  return (
    <div className="space-y-3">
      <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100">{title}</h4>
      <div className="overflow-hidden rounded-lg border border-slate-200 dark:border-slate-700">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-200 bg-slate-50 dark:border-slate-700 dark:bg-slate-800">
              <th className="px-4 py-2 text-left font-medium text-slate-700 dark:text-slate-300">
                Name
              </th>
              <th className="px-4 py-2 text-left font-medium text-slate-700 dark:text-slate-300">
                Type
              </th>
              <th className="px-4 py-2 text-left font-medium text-slate-700 dark:text-slate-300">
                Required
              </th>
              <th className="px-4 py-2 text-left font-medium text-slate-700 dark:text-slate-300">
                Description
              </th>
            </tr>
          </thead>
          <tbody>
            {parameters.map((param, index) => (
              <tr
                key={param.name}
                className={
                  index !== parameters.length - 1
                    ? 'border-b border-slate-200 dark:border-slate-700'
                    : ''
                }
              >
                <td className="px-4 py-3 font-mono text-xs text-slate-900 dark:text-slate-100">
                  {param.name}
                </td>
                <td className="px-4 py-3">
                  <code className="rounded bg-slate-100 px-1.5 py-0.5 text-xs text-slate-700 dark:bg-slate-800 dark:text-slate-300">
                    {param.type}
                  </code>
                </td>
                <td className="px-4 py-3">
                  {param.required ? (
                    <span className="text-xs font-medium text-red-600 dark:text-red-400">
                      Required
                    </span>
                  ) : (
                    <span className="text-xs text-slate-500 dark:text-slate-400">Optional</span>
                  )}
                </td>
                <td className="px-4 py-3 text-xs text-slate-600 dark:text-slate-400">
                  {param.description}
                  {param.example !== undefined && (
                    <div className="mt-1">
                      <span className="text-slate-500">Example: </span>
                      <code className="text-xs">{JSON.stringify(param.example)}</code>
                    </div>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
