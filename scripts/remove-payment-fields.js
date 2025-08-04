#!/usr/bin/env node

/**
 * Database migration script to remove all payment-related fields and data
 * This script will:
 * 1. Remove payment fields from all forms
 * 2. Remove stripe account information from forms
 * 3. Clean up any payment-related submissions
 */

const { MongoClient } = require('mongodb')

// MongoDB connection URL - default to local Docker instance
const MONGODB_URL = process.env.MONGODB_URL || 'mongodb://localhost:27017/framna-feedback'

async function migrateDatabase() {
  const client = new MongoClient(MONGODB_URL)

  try {
    await client.connect()
    console.log('Connected to MongoDB')

    const db = client.db()

    // 1. Remove payment fields from forms
    console.log('Removing payment fields from forms...')
    const formsCollection = db.collection('forms')

    // Find all forms with payment fields
    const formsWithPayment = await formsCollection
      .find({
        'fields.kind': 'payment'
      })
      .toArray()

    console.log(`Found ${formsWithPayment.length} forms with payment fields`)

    for (const form of formsWithPayment) {
      // Filter out payment fields
      const updatedFields = form.fields.filter(field => field.kind !== 'payment')

      await formsCollection.updateOne(
        { _id: form._id },
        {
          $set: { fields: updatedFields },
          $unset: { stripeAccount: '' }
        }
      )

      console.log(`Updated form: ${form.name} (${form._id})`)
    }

    // 2. Remove stripe account information from all forms
    console.log('\nRemoving stripe account information from all forms...')
    const stripeUpdateResult = await formsCollection.updateMany(
      { stripeAccount: { $exists: true } },
      { $unset: { stripeAccount: '' } }
    )

    console.log(`Removed stripe account from ${stripeUpdateResult.modifiedCount} forms`)

    // 3. Remove payment-related answers from submissions
    console.log('\nCleaning payment answers from submissions...')
    const submissionsCollection = db.collection('submissions')

    // Find submissions with payment answers
    const submissionsWithPayment = await submissionsCollection
      .find({
        'answers.kind': 'payment'
      })
      .toArray()

    console.log(`Found ${submissionsWithPayment.length} submissions with payment answers`)

    for (const submission of submissionsWithPayment) {
      // Filter out payment answers
      const updatedAnswers = submission.answers.filter(answer => answer.kind !== 'payment')

      await submissionsCollection.updateOne(
        { _id: submission._id },
        { $set: { answers: updatedAnswers } }
      )
    }

    // 4. Remove payment intents collection if it exists
    console.log('\nChecking for payment intents collection...')
    const collections = await db.listCollections().toArray()
    const hasPaymentIntents = collections.some(col => col.name === 'paymentintents')

    if (hasPaymentIntents) {
      await db.collection('paymentintents').drop()
      console.log('Dropped paymentintents collection')
    } else {
      console.log('No paymentintents collection found')
    }

    console.log('\nMigration completed successfully!')
  } catch (error) {
    console.error('Migration failed:', error)
    process.exit(1)
  } finally {
    await client.close()
  }
}

// Run the migration
migrateDatabase()
