/// <reference lib="dom" />

// Declare global types that the @jsr/openai__openai package expects
// These are normally available in browser environments but not in Node.js

declare global {
  // Re-export DOM types to global scope for the OpenAI package
  const Headers: typeof globalThis.Headers
  const Request: typeof globalThis.Request
  const Response: typeof globalThis.Response
  const FormData: typeof globalThis.FormData
  const Blob: typeof globalThis.Blob
  const File: typeof globalThis.File
  const URL: typeof globalThis.URL
  const URLSearchParams: typeof globalThis.URLSearchParams
  const AbortController: typeof globalThis.AbortController
  const AbortSignal: typeof globalThis.AbortSignal
  const ReadableStream: typeof globalThis.ReadableStream
  const TextEncoder: typeof globalThis.TextEncoder
  const TextDecoder: typeof globalThis.TextDecoder

  // Crypto API
  const crypto: typeof globalThis.crypto

  // Base64 functions
  function btoa(data: string): string
  function atob(data: string): string

  // Fetch API
  function fetch(input: RequestInfo | URL, init?: RequestInit): Promise<Response>
}

// Extend Headers interface to include entries method
interface Headers {
  entries(): IterableIterator<[string, string]>
}

export {}
