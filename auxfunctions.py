from disease import *
from target import *
from evidence import *
from association import *

def order_associations(associations_list):
    num_asociation = len(associations_list)
    for i in range (num_asociation):
        for j in range(num_asociation-1):
            actual_association = associations_list[j]
            next_association = associations_list[j+1]
            if actual_association.__lt__(next_association):
                t = associations_list[j]
                associations_list[j] = associations_list[j+1]
                associations_list[j+1]=t
                
def instantiate_disease(disease_dict):
    id_disease = disease_dict["id"]
    if id_disease.startswith("EFO_"):
        name = disease_dict['name']
        phenotype_objects = []
        phenotype_objects_dict = disease_dict["phenotypes"]
        phenotype_objects_rows = phenotype_objects_dict["rows"]
        for p in phenotype_objects_rows:
            hpo = p["phenotypeHPO"]
            if hpo != None:
                name = hpo["name"]
                phenotype_objects.append(name)
        disease = Disease(id_disease,name, phenotype_objects)
    return disease

def instantiate_target(target_dict):
    id_target = target_dict["id"]
    if id_target.startswith("ENSG"):
        approvedSymbol = target_dict["approvedSymbol"]
        biotype = target_dict["biotype"]
        tractability_item_objects = []
        for item in target_dict["tractability"]:
            tractability_item = TractabilityItem(item["label"], item["modality"], item["value"])
            tractability_item_objects.append(tractability_item)
    target = Target(id_target, approvedSymbol, biotype, tractability_item_objects)
    return target

def create_evidence_list(evidence_lines):
    genetic_datatype = ["genetic_association", "somatic_mutation", "genetic_literature"]
    indirect_datatype =["animal_model", "literature", "rna_expression", "affected_pathwat", "ot_genetics_portal", "cell_line_expression"]
    evidence_list = []
    for e in evidence_lines:
        score_evidence = e["score"]
        id_evidence = e["id"]
        datatype_evidence = e["datatypeId"]
        if datatype_evidence in genetic_datatype:
            sourceId = e["datasourceId"]
            evidence = GeneticEvidence(id_evidence,score_evidence,datatype_evidence, sourceId)
        elif datatype_evidence in indirect_datatype:
            evidence = IndirectEvidence(id_evidence, score_evidence, datatype_evidence)
        else: 
            evidence = Evidence(id_evidence, score_evidence, datatype_evidence)
        evidence_list.append(evidence)
    return evidence_list

