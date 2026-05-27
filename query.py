
QUERY_STRING_TARGET = """
  query target($ensemblId: String!){
    target(ensemblId: $ensemblId){
      id
      approvedSymbol
      biotype
      tractability {
        label
        modality
        value
      }
      associatedDiseases {
        count
        rows {
          disease {
            id
            name
            phenotypes {
            rows {
              phenotypeHPO {
                id
                name
                description
                namespace
              }
              phenotypeEFO {
                id
                name
              }
            }              
          }
        }
      }
    }
  }
}  
"""

QUERY_STRING_DISEASE = """
  query disease($efoId: String!) {
    disease(efoId: $efoId) {
      id
      name
      phenotypes {
              rows {
                phenotypeHPO {
                  id
                  name
                  description
                  namespace
                }
                phenotypeEFO {
                  id
                  name
                }
              }              
            }
      associatedTargets {
        count
        rows {
          target {
            id
            biotype
            approvedSymbol
            tractability {
              label
              modality
              value
            }
          }
        }
      }
    }
  }
"""
QUERY_STRING_ASSOCIATION = """
query targetDiseaseEvidence($ensemblId: String!, $efoId: String!) {
  disease(efoId: $efoId) {
    id
    name
    phenotypes {
              rows {
                phenotypeHPO {
                  id
                  name
                  description
                  namespace
                }
                phenotypeEFO {
                  id
                  name
                }
              }              
            }
    evidences(ensemblIds: [$ensemblId]) {
      count
      rows {
        # Esto va para tus objetos Evidence
        id
        score
        datatypeId
        datasourceId
        target {
          id
          approvedSymbol
          biotype
          tractability {
            label
            modality
            value
          }
        }
      }
    }
  }
}
"""

QUERY_ONLY_TARGET = """
query targetAssociationsWithEvidences($ensemblId: String!) {
  target(ensemblId: $ensemblId) {
    id
    approvedSymbol
    biotype
    tractability {
      label
      modality
      value
    }
    associatedDiseases {
      count
      rows {
        disease {
          id
          name
          phenotypes {
            rows {
              phenotypeHPO {
                id
                name
                description
                namespace
              }
              phenotypeEFO {
                id
                name
              }
            }              
          }
          evidences(ensemblIds: [$ensemblId]) {
            rows {
              id
              score
              datatypeId
              datasourceId
            }
          }
        }
      }
    }
  }
}
"""

QUERY_ONLY_DISEASE = """query diseaseAssociationsWithEvidences($efoId: String!) {
  disease(efoId: $efoId) {
    id
    name
    phenotypes {
              rows {
                phenotypeHPO {
                  id
                  name
                  description
                  namespace
                }
                phenotypeEFO {
                  id
                  name
                }
              }              
            }
    associatedTargets {
      count
      rows {
        score
        target {
          id
          approvedSymbol
          biotype
          tractability {
              label
              modality
              value
            }
          evidences(efoIds: [$efoId]) {
            rows {
              id
              score
              datatypeId
              datasourceId
            }
          }
          
        }
      }
    }
  }
}
"""
