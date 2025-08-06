import { gql } from '@apollo/client'

export const BULK_UPDATE_FORMS_GQL = gql`
  mutation bulkUpdateForms($input: BulkUpdateFormsInput!) {
    bulkUpdateForms(input: $input)
  }
`
