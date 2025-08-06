# Form Publishing Fix - Test Guide

## What was changed

1. **FormActions.tsx**: Updated to use the proper `FormService.publishForm()` method instead of `FormService.update()`
2. **usePublishForm hook**: Created a reusable hook for form publishing logic
3. **Builder NavBar**: Updated to use the same hook for consistency
4. **Loading states**: Added proper loading states when form drafts are being fetched
5. **Error handling**: Added comprehensive error messages and tooltips

## How to test

1. **Create a new form**:
   - Navigate to a project
   - Click "Create Form"
   - Add some fields to the form

2. **Save the form**:
   - The form should auto-save as you add fields
   - You should see the "Publish" button become enabled

3. **Publish the form**:
   - Click the "Publish" button
   - You should see a loading state
   - Once published, the button should change to "Published" and be disabled
   - You should see a success toast message

4. **Verify the form is published**:
   - Navigate to the form's share page
   - The form should be accessible via its public URL
   - Test submitting a response to ensure it works

5. **Test error cases**:
   - Try publishing a form with no fields (should show error)
   - Test with network disconnected (should show error)

## What to look for

- ✅ Publish button shows proper loading state
- ✅ Success message appears after publishing
- ✅ Button changes to "Published" state
- ✅ Form is accessible via public URL
- ✅ Tooltips show when hovering over disabled button
- ✅ Error messages are clear and helpful

## Rollback instructions

If issues occur, revert the following files:
- `/packages/webapp/src/pages/form/views/FormNavbar/FormActions.tsx`
- `/packages/webapp/src/pages/form/Builder/NavBar.tsx`
- Delete `/packages/webapp/src/hooks/usePublishForm.ts`
- Delete `/packages/webapp/src/hooks/index.ts`
