from disease import *
from target import *
from evidence import *
from association import *
from auxfunctions import *

def tabla_target(target_dict):
    try:
        lines_html = ""
        disease_filas = target_dict['data']['target']['associatedDiseases']['rows']
        disease_json_list = []
        for d in disease_filas:
            disease_dict = d["disease"]
            id_disease = disease_dict['id']
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
                disease = Disease(id_disease, name, phenotype_objects)
                lines_html += f"""
                <tr>
                    <td>{disease.id}</td>
                    <td>{disease.name}</td>
                    <td>{disease.phenotype_objects}</td>
                </tr>
                """
                disease_dict_json = {
                    "disease Id": disease.id,
                    "disease name": disease.name,
                    "disease phenotype_objects": disease.phenotype_objects
                }
                disease_json_list.append(disease_dict_json)
            else:
                continue
            disease_json = {"Diseases": disease_json_list}
        return lines_html, disease_json
    except:
        return "",{}
def tabla_disease(disease):
    try:
        lines_html = ""
        targets_filas = disease["data"]["disease"]["associatedTargets"]["rows"]
        targets_json_list = []
        for t in targets_filas:
            target_dict = t["target"]
            id = target_dict["id"]
            if id.startswith("ENSG"):
                approvedSymbol = target_dict["approvedSymbol"]
                biotype = target_dict["biotype"]
                tractability_item_lista = target_dict["tractability"]
                if tractability_item_lista:
                    tractability_item_dict = tractability_item_lista[0]
                    label_tractability_item = tractability_item_dict["label"]
                    modality_tractability_item = tractability_item_dict["modality"]
                    value_tractability_item = tractability_item_dict["value"]
                else:
                    label_tractability_item = "None"
                    modality_tractability_item = "None"
                    value_tractability_item = "None"
                tractability_item = TractabilityItem(label_tractability_item, modality_tractability_item, value_tractability_item)
                target = Target(id, approvedSymbol, biotype, tractability_item)
                lines_html += f"""
                <tr>
                    <td>{target.id}</td>
                    <td>{target.approvedSymbol}</td>
                    <td>{target.biotype}</td>
                    <td> 
                        label: {tractability_item.label}<br>
                        modality: {tractability_item.modality}<br>
                        value: {tractability_item.value}
                    </td>
                </tr>
                """
                dict_target_json = {
                "target id": target.id,
                "target symbol": target.approvedSymbol,
                "target biotype": target.biotype,
                "tractability":{
                    "label": tractability_item.label,
                    "modality":tractability_item.modality,
                    "value":tractability_item.value
                    }
                }
                targets_json_list.append(dict_target_json)           
            else:
                continue
            target_json = {"targets":targets_json_list}
        return lines_html, target_json
    except:
        return "", {}
def association_table(association, score):
    try:
        html_lines = f"""
                <tr>
                    <td>Target Id</td>
                    <td>Is druggable</td>
                    <td>Disease Id</td>
                    <td>Score</td>
                </tr>
                """    

        disease_dict = association["data"]["disease"]
        disease = instantiate_disease(disease_dict)
        
        target_dict = disease_dict["evidences"]["rows"][0]["target"]
        id_target = target_dict["id"]
        if id_target.startswith("ENSG"):
            approvedSymbol = target_dict["approvedSymbol"]
            biotype = target_dict["biotype"]
            tractability_item_objects =[]
            for item in target_dict["tractability"]:
                tractability_item = TractabilityItem(item["label"], item["modality"], item["value"])
                tractability_item_objects.append(tractability_item)
            target = Target(id_target, approvedSymbol, biotype, tractability_item_objects)
        
        evidence_lines = disease_dict["evidences"]["rows"]
        evidence_list = create_evidence_list(evidence_lines)
            
        associations = Association(target, disease, evidence_list)
        if score <= associations.get_total_score():
            html_lines += f"""
                    <tr>
                        <td>{associations.target.id}</td>
                        <td>{str(associations.target.is_druggable())}</td>
                        <td>{associations.disease.id}</td>
                        <td>{str(associations.get_total_score())}</td>
                    </tr>
                    """
            association_json = {"Association":
                {"Target id": associations.target.id,
                "Is druggable": str(associations.target.is_druggable()),
                "Disease Id": associations.disease.id,
                "Score": associations.get_total_score()
                }
            }
        else:
            html_lines = ""
        return html_lines, association_json
    except:
        return "",{}

def table_targets_asociated(targets, score):
    try:
        html_lines = """ 
                <thead>
                    <tr>
                        <th>Target ID</th>
                        <th>Target ApprovedSymbol</th>
                        <th>Target biotype</th>
                        <th>Is druggable</th>
                        <th>Score</th>
                    </tr>
                </thead>
            """
        disease_dict = targets["data"]["disease"]
        disease = instantiate_disease(disease_dict)
        
        targets_lines = disease_dict["associatedTargets"]["rows"]
        association_list = []
        for t in targets_lines:
            target_dict = t["target"]
            target = instantiate_target(target_dict)
            
            evidence_lines = target_dict["evidences"]["rows"]
            evidence_list = create_evidence_list(evidence_lines)
                        
            association = Association(target, disease, evidence_list)
            association_list.append(association)    
        order_associations(association_list)
        association_json_list = []
        for a in association_list:
            association_score = a.get_total_score()
            if score <= association_score:
                is_druggable = str(a.target.is_druggable())
                html_lines+=f"""
                    <tbody>
                        <tr>
                            <td>{a.target.id}</td>
                            <td>{a.target.approvedSymbol}</td>
                            <td>{a.target.biotype}</td>
                            <td>{is_druggable}</td>
                            <td>{str(association_score)}</td>
                        </tr>
                    </tbody>
                    """
                dict_association_json = {
                "target id": a.target.id,
                "target symbol": a.target.approvedSymbol,
                "target biotype": a.target.biotype,
                "is druggable": is_druggable,
                "score": association_score   
                }
                association_json_list.append(dict_association_json)
            else:
                continue
        
        association_json = {"associations":association_json_list}
        return html_lines, association_json
    except:
        return "", {}

def table_diseases_associated(diseases, score):
    try:
        html_lines = """ 
        <thead>
            <tr>
                <td>Disease ID</td>
                <td>Disease Name</td>
                <td>Disease Phenotypes</td>
                <td>Score</td>
            </tr>
        </thead>
            """

        target_dict = diseases["data"]["target"]
        target = instantiate_target(target_dict)
        diseases_lines =target_dict["associatedDiseases"]["rows"]
        association_list = []
        for d in diseases_lines:
            disease_dict = d["disease"]
            id_disease = disease_dict["id"]
            if id_disease.startswith("EFO_"):
                name = disease_dict['name']
                phenotype_objects = []
                phenotype_objects_dict = disease_dict["phenotypes"]
                phenotype_objects_rows = phenotype_objects_dict["rows"]
                for p in phenotype_objects_rows:
                    hpo = p["phenotypeHPO"]
                    if hpo != None:
                        name_hpo = hpo["name"]
                        phenotype_objects.append(name_hpo)
                disease = Disease(id_disease,name, phenotype_objects)
            else: 
                continue
            evidence_lines = disease_dict["evidences"]["rows"]
            evidence_list = create_evidence_list(evidence_lines)
            
            association = Association(target, disease, evidence_list)
            association_list.append(association)
        order_associations(association_list)
        association_json_list = []
        for a in association_list:
            association_score = a.get_total_score()
            if score <= association_score:
                html_lines+=f"""
                <tbody>
                    <tr>
                        <td>{a.disease.id}</td>
                        <td>{a.disease.name}</td>
                        <td>{a.disease.phenotype_objects}</td>
                        <td>{str(association_score)}</td>
                    </tr>
                </tbody>
                """
                dict_association_json = {
                "disease id": a.disease.id,
                "disease name": a.disease.name,
                "disease phenoype objects": a.disease.phenotype_objects,
                "score": association_score   
                }
                association_json_list.append(dict_association_json)  
            else:
                continue
        association_json = {"associations":association_json_list}
            
        return html_lines, association_json
    except:
        return "", {}