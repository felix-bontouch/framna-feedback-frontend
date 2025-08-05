# Mobile API - Form Sharing

## Overview
This document extends the main Mobile API documentation with specific guidance for implementing form sharing in mobile applications.

## Form Sharing Endpoints

### Get Form Share Information
Retrieve comprehensive sharing information and metadata for a form.

**Endpoint:** `GET /api/mobile/forms/:formId/share`

**Response:**
```json
{
  "shareUrl": "https://app.framna.com/form/abc123",
  "isPublished": true,
  "isActive": true,
  "metadata": {
    "title": "Customer Feedback Survey",
    "description": "5 questions, 2 mins to complete",
    "ogImageUrl": "https://cdn.framna.com/og/form123.jpg",
    "questionCount": 5,
    "estimatedTime": 2
  },
  "accessControl": {
    "requiresPassword": false,
    "hasIpLimit": true,
    "hasTimeLimit": false,
    "expiresAt": null
  }
}
```

### Update Form Settings
Update form metadata settings (requires authentication in production).

**Endpoint:** `PUT /api/mobile/forms/:formId/settings`

**Request Body:**
```json
{
  "metaTitle": "Updated Survey Title",
  "metaDescription": "Take our quick survey to help us improve",
  "metaOGImageUrl": "https://example.com/new-og-image.jpg"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Settings updated successfully",
  "updates": {
    "settings.metaTitle": "Updated Survey Title",
    "settings.metaDescription": "Take our quick survey to help us improve",
    "settings.metaOGImageUrl": "https://example.com/new-og-image.jpg"
  }
}
```

## Native Share Integration

### iOS Implementation (Swift)

```swift
import UIKit

class FormShareController {
    private let mobileAPI = MobileFormAPI()
    
    func shareForm(formId: String) async {
        do {
            // Show loading indicator
            showLoading()
            
            // Fetch share information
            let shareInfo = try await mobileAPI.getFormShareInfo(formId: formId)
            
            // Hide loading
            hideLoading()
            
            // Check if form is shareable
            guard shareInfo.isActive && shareInfo.isPublished else {
                showAlert("This form is not available for sharing")
                return
            }
            
            // Create share items
            var items: [Any] = [shareInfo.shareUrl]
            
            // Add custom message
            let message = """
            \(shareInfo.metadata.title)
            \(shareInfo.metadata.description)
            
            Fill out this form: \(shareInfo.shareUrl)
            """
            items.append(message)
            
            // Add image if available
            if let imageUrl = shareInfo.metadata.ogImageUrl,
               let url = URL(string: imageUrl),
               let data = try? Data(contentsOf: url),
               let image = UIImage(data: data) {
                items.append(image)
            }
            
            // Configure activity controller
            let activityController = UIActivityViewController(
                activityItems: items,
                applicationActivities: nil
            )
            
            // Exclude certain activities
            activityController.excludedActivityTypes = [
                .addToReadingList,
                .assignToContact,
                .saveToCameraRoll,
                .openInIBooks
            ]
            
            // Handle completion
            activityController.completionWithItemsHandler = { activity, success, items, error in
                if success {
                    self.trackShareEvent(formId: formId, activity: activity?.rawValue)
                }
            }
            
            // Present on iPad
            if let popover = activityController.popoverPresentationController {
                popover.sourceView = shareButton
                popover.sourceRect = shareButton.bounds
            }
            
            present(activityController, animated: true)
            
        } catch {
            hideLoading()
            showError("Failed to share form: \(error.localizedDescription)")
        }
    }
    
    private func trackShareEvent(formId: String, activity: String?) {
        Analytics.track("form_shared", properties: [
            "form_id": formId,
            "share_method": "native_sheet",
            "activity_type": activity ?? "unknown"
        ])
    }
}
```

### Android Implementation (Kotlin)

```kotlin
import android.content.Intent
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import kotlinx.coroutines.launch
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class FormShareActivity : AppCompatActivity() {
    private val mobileAPI = MobileFormAPI()
    
    fun shareForm(formId: String) {
        lifecycleScope.launch {
            try {
                // Show loading
                showProgressBar(true)
                
                // Fetch share information
                val shareInfo = withContext(Dispatchers.IO) {
                    mobileAPI.getFormShareInfo(formId)
                }
                
                // Hide loading
                showProgressBar(false)
                
                // Check if form is shareable
                if (!shareInfo.isActive || !shareInfo.isPublished) {
                    Toast.makeText(
                        this@FormShareActivity,
                        "This form is not available for sharing",
                        Toast.LENGTH_SHORT
                    ).show()
                    return@launch
                }
                
                // Create share intent
                val shareIntent = Intent(Intent.ACTION_SEND).apply {
                    type = "text/plain"
                    
                    // Set content
                    putExtra(Intent.EXTRA_TEXT, buildShareText(shareInfo))
                    putExtra(Intent.EXTRA_SUBJECT, shareInfo.metadata.title)
                    
                    // Add flag for new document
                    addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                }
                
                // Create chooser with custom title
                val chooserIntent = Intent.createChooser(
                    shareIntent,
                    "Share form via..."
                )
                
                // Track share initiation
                trackShareEvent(formId, "initiated")
                
                // Launch share dialog
                startActivityForResult(chooserIntent, SHARE_REQUEST_CODE)
                
            } catch (e: Exception) {
                showProgressBar(false)
                Toast.makeText(
                    this@FormShareActivity,
                    "Failed to share: ${e.message}",
                    Toast.LENGTH_LONG
                ).show()
            }
        }
    }
    
    private fun buildShareText(shareInfo: FormShareInfo): String {
        return """
        ${shareInfo.metadata.title}
        ${shareInfo.metadata.description}
        
        Fill out this form: ${shareInfo.shareUrl}
        """.trimIndent()
    }
    
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        
        if (requestCode == SHARE_REQUEST_CODE) {
            // Track completion (Android doesn't provide share destination)
            trackShareEvent(lastSharedFormId, "completed")
        }
    }
    
    private fun trackShareEvent(formId: String, action: String) {
        Analytics.track("form_share_$action", mapOf(
            "form_id" to formId,
            "share_method" to "native_intent"
        ))
    }
    
    companion object {
        private const val SHARE_REQUEST_CODE = 1001
    }
}
```

### React Native Implementation

```javascript
import React, { useState } from 'react';
import { 
  Share, 
  Platform, 
  Alert, 
  ActivityIndicator,
  View 
} from 'react-native';
import analytics from '@react-native-firebase/analytics';

const FormShareComponent = ({ formId }) => {
  const [loading, setLoading] = useState(false);
  
  const shareForm = async () => {
    try {
      setLoading(true);
      
      // Fetch share information
      const shareInfo = await MobileAPI.getFormShareInfo(formId);
      
      setLoading(false);
      
      // Check if form is shareable
      if (!shareInfo.isActive || !shareInfo.isPublished) {
        Alert.alert(
          'Form Unavailable',
          'This form is not available for sharing.'
        );
        return;
      }
      
      // Build share content
      const shareContent = {
        message: Platform.select({
          ios: shareInfo.metadata.title,
          android: `${shareInfo.metadata.title}\n${shareInfo.metadata.description}\n\nFill out this form: ${shareInfo.shareUrl}`
        }),
        url: Platform.OS === 'ios' ? shareInfo.shareUrl : undefined,
        title: shareInfo.metadata.title,
      };
      
      // Track share initiation
      await analytics().logEvent('form_share_initiated', {
        form_id: formId,
        platform: Platform.OS
      });
      
      // Open native share dialog
      const result = await Share.share(shareContent);
      
      // Handle result
      if (result.action === Share.sharedAction) {
        // Track successful share
        await analytics().logEvent('form_shared', {
          form_id: formId,
          platform: Platform.OS,
          activity_type: result.activityType || 'unknown'
        });
        
        // Show success message
        if (Platform.OS === 'android') {
          Alert.alert('Success', 'Form shared successfully!');
        }
      }
      
    } catch (error) {
      setLoading(false);
      Alert.alert(
        'Share Failed',
        error.message || 'Unable to share this form'
      );
    }
  };
  
  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" />
      </View>
    );
  }
  
  return (
    <TouchableOpacity onPress={shareForm} style={styles.shareButton}>
      <Icon name="share" size={24} color="#007AFF" />
      <Text style={styles.shareText}>Share Form</Text>
    </TouchableOpacity>
  );
};
```

## Deep Linking Setup

### iOS Configuration

1. **Info.plist:**
```xml
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleURLSchemes</key>
        <array>
            <string>framna</string>
        </array>
    </dict>
</array>
```

2. **Associated Domains (for Universal Links):**
```xml
<key>com.apple.developer.associated-domains</key>
<array>
    <string>applinks:app.framna.com</string>
</array>
```

3. **AppDelegate.swift:**
```swift
func application(_ app: UIApplication, open url: URL, options: [UIApplication.OpenURLOptionsKey : Any] = [:]) -> Bool {
    // Handle framna:// URLs
    if url.scheme == "framna" {
        handleFormDeepLink(url)
        return true
    }
    return false
}

func application(_ application: UIApplication, continue userActivity: NSUserActivity, restorationHandler: @escaping ([UIUserActivityRestoring]?) -> Void) -> Bool {
    // Handle https://app.framna.com URLs
    if userActivity.activityType == NSUserActivityTypeBrowsingWeb,
       let url = userActivity.webpageURL,
       url.host == "app.framna.com" {
        handleFormDeepLink(url)
        return true
    }
    return false
}

private func handleFormDeepLink(_ url: URL) {
    // Extract form ID from URL
    let pathComponents = url.pathComponents
    if pathComponents.count >= 2 && pathComponents[1] == "form" {
        let formId = pathComponents[2]
        // Navigate to form
        navigateToForm(formId: formId)
    }
}
```

### Android Configuration

1. **AndroidManifest.xml:**
```xml
<activity android:name=".MainActivity">
    <!-- App Links -->
    <intent-filter android:autoVerify="true">
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data
            android:scheme="https"
            android:host="app.framna.com"
            android:pathPrefix="/form/" />
    </intent-filter>
    
    <!-- Custom Scheme -->
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:scheme="framna" />
    </intent-filter>
</activity>
```

2. **MainActivity.kt:**
```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    handleIntent(intent)
}

override fun onNewIntent(intent: Intent) {
    super.onNewIntent(intent)
    handleIntent(intent)
}

private fun handleIntent(intent: Intent) {
    val data = intent.data ?: return
    
    when {
        // Handle https://app.framna.com/form/[formId]
        data.scheme == "https" && data.host == "app.framna.com" -> {
            val pathSegments = data.pathSegments
            if (pathSegments.size >= 2 && pathSegments[0] == "form") {
                val formId = pathSegments[1]
                navigateToForm(formId)
            }
        }
        
        // Handle framna://form/[formId]
        data.scheme == "framna" -> {
            val formId = data.lastPathSegment
            formId?.let { navigateToForm(it) }
        }
    }
}
```

## Share Analytics Best Practices

### Event Tracking
```javascript
// Track share button tap
analytics.track('form_share_button_tapped', {
  form_id: formId,
  form_title: formTitle,
  question_count: questionCount
});

// Track share dialog opened
analytics.track('form_share_dialog_opened', {
  form_id: formId,
  available_options: shareOptions
});

// Track successful share
analytics.track('form_shared', {
  form_id: formId,
  share_destination: activityType, // iOS only
  share_method: 'native',
  form_status: isPublished ? 'published' : 'draft'
});

// Track share errors
analytics.track('form_share_error', {
  form_id: formId,
  error_type: error.code,
  error_message: error.message
});
```

### Performance Monitoring
```javascript
// Monitor share API performance
const startTime = Date.now();
const shareInfo = await MobileAPI.getFormShareInfo(formId);
const loadTime = Date.now() - startTime;

analytics.track('form_share_api_performance', {
  form_id: formId,
  load_time_ms: loadTime,
  cache_hit: shareInfo.fromCache || false
});
```

## Error Handling

### Common Error Scenarios
1. **Form Not Published**: Show clear message that draft forms cannot be shared
2. **Network Error**: Offer retry option or show cached share URL if available
3. **Form Deleted**: Handle 404 errors gracefully
4. **Access Restricted**: Inform user if form requires authentication

### Error Messages
```javascript
const ERROR_MESSAGES = {
  FORM_NOT_FOUND: "This form no longer exists",
  FORM_NOT_PUBLISHED: "This form must be published before sharing",
  FORM_INACTIVE: "This form is currently closed",
  NETWORK_ERROR: "Unable to load share information. Please check your connection.",
  PERMISSION_DENIED: "You don't have permission to share this form"
};
```

## Caching Strategy

```javascript
class FormShareCache {
  constructor() {
    this.cache = new Map();
    this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
  }
  
  async getShareInfo(formId) {
    const cached = this.cache.get(formId);
    
    if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
      return { ...cached.data, fromCache: true };
    }
    
    try {
      const data = await MobileAPI.getFormShareInfo(formId);
      this.cache.set(formId, {
        data,
        timestamp: Date.now()
      });
      return data;
    } catch (error) {
      // Return cached data if available, even if expired
      if (cached) {
        return { ...cached.data, fromCache: true, stale: true };
      }
      throw error;
    }
  }
  
  invalidate(formId) {
    this.cache.delete(formId);
  }
}
```