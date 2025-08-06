# Debugging Guide for AI Form Creation

This guide helps you debug the `create-form-with-ai.resolver.ts` endpoint step by step.

## Prerequisites

1. **Docker services running**: MongoDB and Redis must be running
   ```bash
   docker ps  # Check if services are running
   ./scripts/start-local.sh  # Start services if needed
   ```

2. **Valid user account**: You need a test user to authenticate
   ```bash
   ./scripts/create-test-user-simple.sh  # Create a test user
   ```

3. **Project ID**: You need a valid project ID
   ```bash
   ./scripts/get-project-id.sh  # Get project IDs from database
   ```

## Step-by-Step Debugging Process

### 1. Start Server in Debug Mode

**Option A: Using VS Code (Recommended)**
1. Open VS Code
2. Press `Cmd+Shift+D` to open Debug panel
3. Select "Debug Backend (NestJS)" from dropdown
4. Click the green play button or press `F5`
5. Wait for "Application is running" in terminal

**Option B: Manual Start + Attach**
```bash
cd packages/server
pnpm debug
```
Then attach debugger:
1. In VS Code Debug panel, select "Attach to Backend"
2. Click play button

### 2. Set Breakpoints

Click in the left margin (gutter) to set breakpoints at these key locations in `create-form-with-ai.resolver.ts`:

- **Line 30**: Entry point - logs input parameters
- **Line 41**: Before AI service call
- **Line 43**: After AI service returns
- **Line 77**: Before form creation
- **Line 107**: Success point
- **Line 111**: Error handling

### 3. Test the Endpoint

**Using the test script:**
```bash
# Set your project ID first
export PROJECT_ID="YOUR_PROJECT_ID_HERE"

# Run the test
./scripts/test-ai-form-creation.sh
```

**Using Postman:**
1. Import `postman/AI-Form-Creation-Debug.postman_collection.json`
2. Update the `projectId` variable in collection settings
3. Run requests in order:
   - Login (saves session cookie)
   - Create Form with AI

**Using cURL manually:**
```bash
# 1. Login first
curl -c cookies.txt -X POST http://localhost:9157/graphql \
  -H "Content-Type: application/json" \
  -H "X-Device-Id: test-device-123" \
  -d '{
    "query": "query login($input: LoginInput!) { login(input: $input) }",
    "variables": {
      "input": {
        "email": "test@example.com",
        "password": "password123"
      }
    }
  }'

# 2. Create form with AI
curl -b cookies.txt -X POST http://localhost:9157/graphql \
  -H "Content-Type: application/json" \
  -H "X-Device-Id: test-device-123" \
  -d '{
    "query": "mutation createFormWithAI($input: CreateFormWithAIInput!) { createFormWithAI(input: $input) }",
    "variables": {
      "input": {
        "projectId": "YOUR_PROJECT_ID_HERE",
        "topic": "Customer satisfaction survey",
        "reference": "Include rating questions"
      }
    }
  }'
```

### 4. Debug Navigation

When breakpoint hits:
- **F10**: Step Over (execute current line)
- **F11**: Step Into (go into function calls)
- **Shift+F11**: Step Out (exit current function)
- **F5**: Continue (run to next breakpoint)

### 5. Inspect Variables

In VS Code Debug panel:
- **Variables**: See local and closure variables
- **Watch**: Add expressions to monitor
- **Call Stack**: See execution path
- **Debug Console**: Execute code in current context

### 6. Console Logs

The resolver includes debug logs that will appear in terminal:
- 🔍 Entry point with parameters
- 🔍 AI service calls
- 🔍 Form creation details
- ❌ Error details

### 7. Common Issues

**"Unbound breakpoint" error:**
- Rebuild: `cd packages/server && pnpm build`
- Restart VS Code
- Check that source maps are enabled in tsconfig.json

**Authentication errors:**
- Ensure you're using the session cookie
- Check X-Device-Id header matches
- Verify user exists and is not suspended

**Project not found:**
- Run `./scripts/get-project-id.sh` to get valid IDs
- Ensure the project belongs to the user's team

**AI service errors:**
- Check if OpenAI API key is configured in .env
- Monitor console for specific error messages

## Tips for Effective Debugging

1. **Use conditional breakpoints**: Right-click breakpoint → Edit Breakpoint → Add condition
2. **Log points**: Instead of breakpoint, right-click → Add Logpoint to log without stopping
3. **Exception breakpoints**: In Debug panel, check "Uncaught Exceptions" to break on errors
4. **Watch expressions**: Add `input.topic`, `team.id`, etc. to Watch panel

## Troubleshooting

If debugging doesn't work:
1. Kill all Node processes: `pkill -f node`
2. Clear dist folder: `rm -rf packages/server/dist`
3. Rebuild: `cd packages/server && pnpm build`
4. Restart VS Code
5. Try "Attach to Backend" instead of launching

For more help, check the server logs or run with verbose logging:
```bash
DEBUG=* pnpm dev:server
```