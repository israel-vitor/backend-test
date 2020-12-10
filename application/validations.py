from typing import Dict, Any, Tuple, List

from application.models import WorkflowModel


def validate_body_structure(body: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """
    Check if the request body has only the necessary fields and if any are missing for the workflow creation process.

    :param body: a dictionary with the body content of the request
    :type body: Dict[str, Any]

    :return: a tuple with a list of the not allowed fields found if they exist and a list of the missing fields if they
        exists
    :rtype: Tuple[bool, List[str], List[str]]
    """
    workflow_structure = WorkflowModel.__dict__
    workflow_fields = [field for field in workflow_structure.keys() if '_' not in field and 'UUID' not in field]

    body_fields = body.keys()

    not_allowed_fields = [field for field in body_fields if field not in workflow_fields]
    missing_fields = [field for field in workflow_fields if field not in body_fields]

    return not_allowed_fields, missing_fields


def validate_fields_format(body: Dict[str, Any]) -> List[str]:
    """
    Check if the fields from the defined request body are in the valid format.

    :param body: a dictionary with the body content of the request
    :type body: Dict[str, Any]

    :return: a list with the name of the fields that are in an invalid format
    :rtype: List[str]
    """

    invalid_fields = []

    status = body.get('status')
    if status and status not in ['inserted', 'consumed']:
        invalid_fields.append('status')

    data = body.get('data')
    if data and not isinstance(data, dict):
        invalid_fields.append('data')

    steps = body.get('steps')
    if steps and not isinstance(steps, list):
        invalid_fields.append('steps')

    return invalid_fields
