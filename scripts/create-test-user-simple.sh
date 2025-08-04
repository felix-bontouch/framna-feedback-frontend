#!/bin/bash

echo "🔧 Creating test user for Framna Feedback..."

# Pre-computed bcrypt hash for "Test123!" with salt 10
# This was generated using: bcrypt.hashSync('Test123!', 10)
HASH='$2b$10$6X.uy6M0TYJzm3GCWD2CeuAjjHx4aUqDu/h2U.FKzOUKqYLKLRZ0y'

# Create MongoDB script
cat > /tmp/create-test-user.js << EOF
const existingUser = db.users.findOne({ email: "test@example.com" });

if (existingUser) {
  print("❌ Test user already exists!");
  print("Email: test@example.com");
  print("ID: " + existingUser._id);
} else {
  const result = db.users.insertOne({
    name: "Test User",
    email: "test@example.com",
    password: "$HASH",
    avatar: "https://www.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0?d=identicon",
    lang: "en",
    isEmailVerified: true,
    isDeletionScheduled: false,
    createdAt: new Date(),
    updatedAt: new Date()
  });
  
  print("✅ Test user created successfully!");
  print("");
  print("📧 Login credentials:");
  print("   Email: test@example.com");
  print("   Password: Test123!");
  print("");
  print("🌐 Login URL: http://localhost:3000/login");
}
EOF

# Execute the script in MongoDB
docker exec -i framna-feedback-mongodb mongosh framna-feedback --quiet < /tmp/create-test-user.js

# Clean up
rm /tmp/create-test-user.js

echo ""
echo "🎉 Done! You can now login with:"
echo "   Email: test@example.com"
echo "   Password: Test123!"
echo "   URL: http://localhost:3000/login"