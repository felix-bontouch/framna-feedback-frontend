// Debug utilities for development
const DEBUG = process.env.NODE_ENV === 'development'

export const debugLog = {
  auth: (message: string, data?: any) => {
    if (DEBUG) {
      console.log(`🔐 [AUTH] ${message}`, data || '')
    }
  },

  graphql: (message: string, data?: any) => {
    if (DEBUG) {
      console.log(`📡 [GRAPHQL] ${message}`, data || '')
    }
  },

  error: (message: string, error?: any) => {
    if (DEBUG) {
      console.error(`❌ [ERROR] ${message}`, error || '')
    }
  },

  network: (message: string, data?: any) => {
    if (DEBUG) {
      console.log(`🌐 [NETWORK] ${message}`, data || '')
    }
  }
}

// Add request/response interceptor for debugging
export function setupDebugInterceptors() {
  if (!DEBUG) return

  // Log all GraphQL operations
  console.log('🔧 Debug mode enabled - logging all GraphQL operations')

  // Add to window for easy access in console
  ;(window as any).framnaDebug = {
    enableVerbose: () => {
      localStorage.setItem('debug_verbose', 'true')
      console.log('Verbose logging enabled')
    },
    disableVerbose: () => {
      localStorage.removeItem('debug_verbose')
      console.log('Verbose logging disabled')
    },
    clearAuth: () => {
      document.cookie.split(';').forEach(c => {
        document.cookie = c
          .replace(/^ +/, '')
          .replace(/=.*/, '=;expires=' + new Date().toUTCString() + ';path=/')
      })
      localStorage.clear()
      sessionStorage.clear()
      console.log('Auth cleared - refresh the page')
    }
  }

  console.log('Debug commands available:')
  console.log('- framnaDebug.enableVerbose()')
  console.log('- framnaDebug.disableVerbose()')
  console.log('- framnaDebug.clearAuth()')
}
