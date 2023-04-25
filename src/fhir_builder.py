
import random


def insert_study_tag(study_id, payload):
    """
    Insert a tag with the study_id to a FHIR resource
    """
    payload["meta"] = {
        "tag": [
            {
                "code": study_id,
                "system": "urn:study_id",
                "display": study_id
            }
        ]
    }
    return payload


def patient(resource_id, study_id=None, gender=None):
    """
    Build a Patient FHIR resource
    """
    resource = {
        "resourceType": "Patient",
        "id": resource_id,
        "identifier": [
            {
                "use": "official",
                "system": "https://app.dewrangle.com/fhir",
                "value": resource_id
            }
        ]
    }
    if study_id:
        resource = insert_study_tag(study_id, resource)

    if not gender:
        gender = random.choice(["male", "female"])
        resource["gender"] = gender

    return resource


def specimen(resource_id, patient_id, study_id=None, composition=None, body_site=None):
    """
    Build a Specimen FHIR resource
    """
    resource = {
        "resourceType": "Specimen",
        "id": resource_id,
        "identifier": [
            {
                "use": "official",
                "system": "https://app.dewrangle.com/fhir",
                "value": resource_id
            }
        ],
        "subject": {
            "reference": f"Patient/{patient_id}"
        }
    }
    if study_id:
        resource = insert_study_tag(study_id, resource)

    if not composition:
        composition = random.choice(["Blood", "Saliva", "Tissue", "Unknown"])
        resource["type"] = {
            "text": composition,
        }

    if not body_site:
        body_site = random.choice(["Brain", "Tongue", "Arm", "Leg"])
        resource["collection"] = {
            "bodySite": {
                "text": body_site
            },
        }

    return resource
