import flask_excel as excel
import pika
from flask import Flask, request

from application.models import WorkflowModel
from application.validations import validate_body_structure, validate_fields_format


def create_app():
    app = Flask(__name__)

    config_module = f"application.config.Config"

    app.config.from_object(config_module)

    from application.models import db, migrate

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/workflows', methods=['POST'])
    def create_workflow():
        if request.is_json:
            data = request.get_json()

            not_allowed_fields, missing_fields = validate_body_structure(data)
            if not_allowed_fields:
                return {"error": f"The fields {not_allowed_fields} are not allowed for the workflow object"}, 400

            if missing_fields:
                return {"error": f"The fields {missing_fields} are required for the workflow object"}, 400

            invalid_format_fields = validate_fields_format(data)
            if invalid_format_fields:
                return {"error": f"The fields {invalid_format_fields} are invalid"}, 400

            new_workflow = WorkflowModel(
                status=data['status'],
                data=data['data'],
                steps=data['steps']
            )

            db.session.add(new_workflow)
            db.session.commit()

            connection = pika.BlockingConnection(pika.ConnectionParameters(host='development_rabbitmq_1'))
            channel = connection.channel()
            channel.queue_declare(queue='workflow_queue', durable=True)
            channel.basic_publish(
                exchange='',
                routing_key='workflow_queue',
                body=str(new_workflow.UUID),
                properties=pika.BasicProperties(delivery_mode=2)
            )
            connection.close()

            return {
                "message": f"The workflow has been created successfully.",
                "workflow": {
                    "uuid": new_workflow.UUID,
                    "data": new_workflow.data,
                    "steps": new_workflow.steps,
                    "status": new_workflow.status
                }
            }

        else:
            return {"error": "The request payload is not in JSON format"}, 400

    @app.route('/workflows', methods=['GET'])
    def retrieve_workflows():
        workflows = WorkflowModel.query.all()
        results = [
            {
                "uuid": workflow.UUID,
                "data": workflow.data,
                "steps": workflow.steps,
                "status": workflow.status
            } for workflow in workflows]

        return {"count": len(results), "workflows": results}

    @app.route('/workflows/<workflow_id>', methods=['PATCH'])
    def update_workflow(workflow_id):
        workflow = WorkflowModel.query.get_or_404(workflow_id)

        data = request.get_json()

        not_allowed_fields, _ = validate_body_structure(data)
        if not_allowed_fields:
            return {"error": f"The fields {not_allowed_fields} are not allowed for the workflow object"}, 400

        invalid_format_fields = validate_fields_format(data)
        if invalid_format_fields:
            return {"error": f"The fields {invalid_format_fields} are invalid"}, 400

        if 'data' in data.keys() or 'steps' in data.keys():
            return {"error": f"You can update only the workflow status"}, 400

        workflow.status = data['status']

        db.session.add(workflow)
        db.session.commit()

        return {"message": f"The workflow {workflow.UUID} was successfully updated"}

    @app.route('/workflows/consume', methods=['GET'])
    def update_workflows():

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='development_rabbitmq_1'))
        channel = connection.channel()
        channel.queue_declare(queue='workflow_queue', durable=True)

        channel.basic_qos(prefetch_count=1)

        method, properties, body = channel.basic_get(queue='workflow_queue', auto_ack=True)

        if method is None:
            return {"message": "There is no workflow to consume"}
        else:
            uuid_recovered = body.decode()

        return {
            "message": f"The workflow {uuid_recovered} was successfully consumed. "
                       f"Download the csv file from http://localhost:5000/workflows/download/{uuid_recovered}"
        }

    @app.route('/workflows/download/<workflow_id>', methods=['GET'])
    def download_workflow_csv(workflow_id):

        workflow = WorkflowModel.query.get_or_404(workflow_id)

        excel.init_excel(app)
        extension_type = "csv"
        filename = workflow_id + "." + extension_type

        return excel.make_response_from_dict(workflow.data, file_type=extension_type, file_name=filename)

    return app
