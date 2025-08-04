#!/bin/bash

# Database migration script to remove all payment-related fields and data

echo "Starting payment removal migration..."

# Run MongoDB commands through docker
docker exec framna-feedback-mongodb mongosh framna-feedback --eval '
// Remove payment fields from forms
print("Removing payment fields from forms...");
var formsWithPayment = db.forms.find({ "fields.kind": "payment" }).toArray();
print("Found " + formsWithPayment.length + " forms with payment fields");

formsWithPayment.forEach(function(form) {
    var updatedFields = form.fields.filter(function(field) {
        return field.kind !== "payment";
    });
    
    db.forms.updateOne(
        { _id: form._id },
        { 
            $set: { fields: updatedFields },
            $unset: { stripeAccount: "" }
        }
    );
    print("Updated form: " + form.name);
});

// Remove stripe account information from all forms
print("\nRemoving stripe account information from all forms...");
var stripeResult = db.forms.updateMany(
    { stripeAccount: { $exists: true } },
    { $unset: { stripeAccount: "" } }
);
print("Removed stripe account from " + stripeResult.modifiedCount + " forms");

// Remove payment answers from submissions
print("\nCleaning payment answers from submissions...");
var submissionsWithPayment = db.submissions.find({ "answers.kind": "payment" }).toArray();
print("Found " + submissionsWithPayment.length + " submissions with payment answers");

submissionsWithPayment.forEach(function(submission) {
    var updatedAnswers = submission.answers.filter(function(answer) {
        return answer.kind !== "payment";
    });
    
    db.submissions.updateOne(
        { _id: submission._id },
        { $set: { answers: updatedAnswers } }
    );
});

// Drop payment intents collection if it exists
print("\nChecking for payment intents collection...");
if (db.getCollectionNames().includes("paymentintents")) {
    db.paymentintents.drop();
    print("Dropped paymentintents collection");
} else {
    print("No paymentintents collection found");
}

print("\nMigration completed successfully!");
'

echo "Migration completed!"