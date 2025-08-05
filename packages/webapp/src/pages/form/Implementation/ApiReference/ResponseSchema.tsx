import { IconChevronDown, IconChevronRight } from '@tabler/icons-react'
import { useState } from 'react'

interface SchemaField {
  name: string
  type: string
  description: string
  required?: boolean
  children?: SchemaField[]
  example?: any
}

interface ResponseSchemaProps {
  title: string
  fields: SchemaField[]
}

function SchemaFieldRow({ field, depth = 0 }: { field: SchemaField; depth?: number }) {
  const [expanded, setExpanded] = useState(false)
  const hasChildren = field.children && field.children.length > 0

  return (
    <>
      <div
        className={`border-b border-slate-200 dark:border-slate-700 ${
          hasChildren ? 'cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-800' : ''
        }`}
        onClick={() => hasChildren && setExpanded(!expanded)}
      >
        <div className="flex items-start px-4 py-3" style={{ paddingLeft: `${16 + depth * 24}px` }}>
          {hasChildren && (
            <button className="mr-2 mt-0.5 flex-shrink-0">
              {expanded ? (
                <IconChevronDown className="h-4 w-4 text-slate-400" />
              ) : (
                <IconChevronRight className="h-4 w-4 text-slate-400" />
              )}
            </button>
          )}
          <div className="grid flex-1 grid-cols-12 gap-4">
            <div className="col-span-4">
              <code className="font-mono text-xs text-slate-900 dark:text-slate-100">
                {field.name}
              </code>
              {field.required && (
                <span className="ml-2 text-xs text-red-600 dark:text-red-400">*</span>
              )}
            </div>
            <div className="col-span-3">
              <code className="rounded bg-slate-100 px-1.5 py-0.5 text-xs text-slate-700 dark:bg-slate-800 dark:text-slate-300">
                {field.type}
              </code>
            </div>
            <div className="col-span-5 text-xs text-slate-600 dark:text-slate-400">
              {field.description}
              {field.example !== undefined && (
                <div className="mt-1">
                  <span className="text-slate-500">Example: </span>
                  <code className="text-xs">{JSON.stringify(field.example)}</code>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
      {hasChildren && expanded && (
        <>
          {field.children!.map(child => (
            <SchemaFieldRow key={`${field.name}.${child.name}`} field={child} depth={depth + 1} />
          ))}
        </>
      )}
    </>
  )
}

export default function ResponseSchema({ title, fields }: ResponseSchemaProps) {
  return (
    <div className="space-y-3">
      <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100">{title}</h4>
      <div className="overflow-hidden rounded-lg border border-slate-200 dark:border-slate-700">
        <div className="border-b border-slate-200 bg-slate-50 dark:border-slate-700 dark:bg-slate-800">
          <div className="grid grid-cols-12 gap-4 px-4 py-2 text-xs font-medium text-slate-700 dark:text-slate-300">
            <div className="col-span-4">Field</div>
            <div className="col-span-3">Type</div>
            <div className="col-span-5">Description</div>
          </div>
        </div>
        <div>
          {fields.map(field => (
            <SchemaFieldRow key={field.name} field={field} />
          ))}
        </div>
      </div>
    </div>
  )
}
