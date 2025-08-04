#!/bin/bash

echo "🔧 Setting all users as email verified..."

# MongoDB command to update all users
cat > /tmp/verify-users.js << 'EOF'
const result = db.users.updateMany(
  { isEmailVerified: { $ne: true } },
  { $set: { isEmailVerified: true } }
);

print("✅ Updated " + result.modifiedCount + " users to verified status");
print("");

// Show current user status
const users = db.users.find({}, { email: 1, isEmailVerified: 1 }).toArray();
print("Current users:");
users.forEach(user => {
  print("  " + user.email + " - Verified: " + (user.isEmailVerified ? "Yes" : "No"));
});
EOF

# Execute the script in MongoDB
docker exec -i framna-feedback-mongodb mongosh framna-feedback --quiet < /tmp/verify-users.js

# Clean up
rm /tmp/verify-users.js

echo ""
echo "🎉 All users are now verified!"
echo "Email verification check has been disabled in the frontend."