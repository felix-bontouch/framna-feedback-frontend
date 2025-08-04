# Debugging Guide for Framna Feedback

This guide helps you debug login/signup issues and set up proper debugging for the full-stack application.

## Quick Diagnosis

If login/signup is spinning indefinitely, run:
```bash
./scripts/debug-login.sh
```

This will test:
1. GraphQL endpoint connectivity
2. Login mutation functionality
3. Cookie handling
4. Frontend proxy configuration

## VS Code Debugging

### 1. Debug Backend (NestJS)

Start the backend in debug mode:
```bash
cd packages/server
pnpm debug
```

Or use VS Code:
1. Open VS Code
2. Go to Run and Debug (Ctrl+Shift+D)
3. Select "Debug Backend (NestJS)"
4. Press F5

Set breakpoints in:
- `packages/server/src/resolver/auth/login.resolver.ts`
- `packages/server/src/resolver/auth/sign-up.resolver.ts`
- `packages/server/src/service/auth.service.ts`

### 2. Debug Frontend (Chrome)

1. Make sure the app is running (`pnpm dev:webapp`)
2. In VS Code, select "Debug Frontend (Chrome)"
3. Press F5
4. Chrome will open with debugging enabled

Set breakpoints in:
- `packages/webapp/src/services/auth.ts`
- `packages/webapp/src/pages/auth/Login.tsx`
- `packages/webapp/src/pages/auth/SignUp.tsx`

### 3. Debug Full Stack

Select "Debug Full Stack" to debug both frontend and backend simultaneously.

## Browser Console Commands

Open browser DevTools (F12) and use these commands:

```javascript
// Enable verbose logging
framnaDebug.enableVerbose()

// Clear all authentication data
framnaDebug.clearAuth()

// Disable verbose logging
framnaDebug.disableVerbose()
```

## Common Issues and Solutions

### 1. Login/Signup Spinning

**Symptoms**: Button keeps spinning, no error message

**Check**:
```bash
# 1. Verify services are running
docker ps | grep -E "mongo|redis"

# 2. Test backend directly
curl -X POST http://localhost:9157/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __typename }"}'

# 3. Check frontend proxy
curl -X POST http://localhost:3000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __typename }"}'
```

**Common causes**:
- Backend not running
- MongoDB/Redis not connected
- Frontend proxy misconfigured
- CORS issues

### 2. Authentication Errors

**Check server logs**:
```bash
# In the terminal running pnpm dev:server
# Look for error messages
```

**MongoDB connection**:
```bash
./scripts/mongodb-utils.sh shell
db.users.find({ email: "test@example.com" })
```

### 3. Cookie Issues

**In browser console**:
```javascript
// Check cookies
document.cookie

// Check device ID
localStorage.getItem('deviceId')
```

## Network Debugging

### GraphQL Requests

1. Open Network tab in DevTools
2. Filter by "graphql"
3. Check:
   - Request headers (especially x-device-id)
   - Response status
   - Response body for errors

### Common GraphQL Errors

```json
{
  "errors": [{
    "message": "The password does not match",
    "extensions": {
      "code": "BAD_REQUEST"
    }
  }]
}
```

## Step-by-Step Debugging Process

1. **Start with the debug script**:
   ```bash
   ./scripts/debug-login.sh
   ```

2. **Check browser console**:
   - Open DevTools (F12)
   - Look for red errors
   - Check Network tab for failed requests

3. **Enable verbose logging**:
   ```javascript
   framnaDebug.enableVerbose()
   ```
   Then try to login again

4. **Set breakpoints**:
   - Frontend: `AuthService.login()` method
   - Backend: `LoginResolver.login()` method

5. **Check environment variables**:
   ```bash
   cat packages/server/.env | grep -E "MONGO|REDIS|SESSION"
   ```

## Debugging Checklist

- [ ] MongoDB is running (`docker ps | grep mongo`)
- [ ] Redis is running (`docker ps | grep redis`)
- [ ] Backend is running on port 9157
- [ ] Frontend is running on port 3000
- [ ] Test user exists in database
- [ ] Environment variables are set correctly
- [ ] No CORS errors in browser console
- [ ] GraphQL endpoint responds to test query
- [ ] Cookies are being set properly
- [ ] Device ID is present in localStorage

## Advanced Debugging

### Enable NestJS Debug Logs

Add to `.env`:
```
DEBUG=true
```

### MongoDB Query Logs

```javascript
// In MongoDB shell
db.setProfilingLevel(2)
db.system.profile.find().limit(5).sort({ ts: -1 }).pretty()
```

### Redis Monitor

```bash
docker exec -it framna-feedback-redis redis-cli MONITOR
```

## Need Help?

1. Run the debug script first
2. Check browser console for errors
3. Use VS Code debugger with breakpoints
4. Check server logs for detailed errors
5. Verify all services are running properly