queries = [
    # APPLICATION_QUERY
    """
    {
      allFactSheets(
        after: "{{ end_cursor }}"
        first: {{ page_size}}
        filter: {
          facetFilters: [{ facetKey: "FactSheetTypes", keys: ["Application"] }]
        }
      ) {
        edges {
          node {
            ... on Application {
              type
              displayName
              name
              description
              category
              completion {
                percentage
                sectionCompletions {
                  name
                  percentage
                }
              }
              id
              fullName
              type
              tags {
                id
                name
                color
                description
                tagGroup {
                  id
                  shortName
                  mode
                  name
                  mandatory
                }
              }
              subscriptions {
                edges {
                  node {
                    id
                    user {
                      id
                      firstName
                      lastName
                      displayName
                      email
                      technicalUser
                      permission {
                        role
                        status
                      }
                    }
                    type
                    roles {
                      id
                      name
                      description
                      comment
                      subscriptionType
                      restrictToFactSheetTypes
                    }
                    createdAt
                  }
                }
              }
              status
              level
              createdAt
              updatedAt
              lxState
              qualitySeal
              ApplicationLifecycle: lifecycle {
                asString
                phases {
                  phase
                  startDate
                  milestoneId
                }
              }
              functionalSuitabilityDescription
              technicalSuitabilityDescription
              functionalSuitability
              technicalSuitability
              businessCriticality
              release
              businessCriticalityDescription
              alias
              orderingState
              processingPurpose
              legalBasis
              legalBasisDescription
              TOMDescription
              Broker
              aggregatedObsolescenceRisk
              BusinessConfidentialityCriticality
              BusinessIntegrityConfidentiality
              lxCatalogStatus
              lxProductCategory
              lxHostingType
              lxHostingDescription
              lxSsoProvider
              lxStatusSSO
              externalId {
                externalId
                comment
                externalUrl
                status
              }
              signavioGlossaryItemId {
                externalId
                comment
                externalUrl
                status
              }
              lxSiId {
                externalId
                comment
                externalUrl
                status
              }
              lxCatalogId {
                externalId
                comment
                externalUrl
                status
              }
              relApplicationToITComponent {
                edges {
                    node {
                        factSheet {
                            id
                        }
                    }
                }
              }
              relApplicationToBusinessCapability {
                edges {
                    node {
                        factSheet {
                            id
                        }
                    }
                }
              }
              documents {
                edges {
                  node {
                    name
                    url
                    documentType
                  }
                }
              }
            }
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
        totalCount
      }
    }
    """,

    # PROVIDER_QUERY
    """
    {
      allFactSheets(
        after: "{{ end_cursor }}"
        first: {{ page_size}}
        filter: {
          facetFilters: [{ facetKey: "FactSheetTypes", keys: ["Provider"] }]
        }
      ) {
        edges {
          node {
            ... on Provider {
              id
              type
              displayName
              relProviderToITComponent {
                edges {
                  node {
                    factSheet {
                    id
                    }
                  }
                }
              }
            }
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
        totalCount
      }
    }
    """,

    # COMPONENT_QUERY
    """
    {
      allFactSheets(
        after: "{{ end_cursor }}"
        first: {{ page_size}}
        filter: {
          facetFilters: [{ facetKey: "FactSheetTypes", keys: ["ITComponent"] }]
        }
      ) {
        edges {
          node {
            ... on ITComponent {
              alias
              displayName
              type
              description
              id
              subscriptions {
                edges {
                  node {
                    user {
                      id
                      userName
                      email
                      firstName
                      lastName
                      displayName
                      technicalUser
                      status
                      role
                    }
                    roles {
                      id
                      name
                      description
                      comment
                      subscriptionType
                      restrictToFactSheetTypes
                    }
                  }
                }
              }
              documents {
                edges {
                  node {
                    name
                    url
                    documentType
                  }
                }
              }
              tags {
                id
                name
                description
                color
                status
                factSheetCount
                deletable
              }
            }
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
        totalCount
      }
    }
    """,

    # BUSINESS_CAPABILITY
    """
    {
      allFactSheets(
        after: "{{ end_cursor }}"
        first: {{ page_size}}
        filter: {
          facetFilters: [{ facetKey: "FactSheetTypes", keys: ["BusinessCapability"] }]
        }
      ) {
        edges {
          node {
            ... on BusinessCapability {
                id
                level
                relBusinessCapabilityToApplication {
                    edges {
                        node {
                            factSheet {
                                id
                                tags {
                                    id
                                    name
                                    description
                                    color
                                    status
                                    factSheetCount
                                    deletable
                                }
                            }
                        }
                    }
                }
                relToParent {
                    edges {
                        node {
                            factSheet {
                                id
                            }
                        }
                    }
                }
                displayName
                type
                description
                subscriptions {
                    edges {
                        node {
                            user {
                                email
                            }
                            roles {
                                name
                            }
                        }
                    }
                }
                tags {
                    id
                    name
                    description
                    color
                    status
                    factSheetCount
                    deletable
                }
            }
        }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
        totalCount
      }
    }
    """
]