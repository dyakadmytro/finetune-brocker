import openai
import finetune_service_pb2
import finetune_service_pb2_grpc
import grpc
from concurrent import futures

openai.api_key = "YOUR_OPENAI_API_KEY"

class FineTuneServiceServicer(finetune_service_pb2_grpc.FineTuneServiceServicer):

    def FineTuneModel(self, request, context):
        # Upload the file to OpenAI
        with open(request.file_path, 'rb') as f:
            response = openai.File.create(file=f, purpose='fine-tune')

        # Fine-tune the model
        model_id = "ft:gpt-3.5-turbo:my-org:" + request.model_suffix + ":id"
        openai.FineTuningJob.create(training_file=response.id, model="gpt-3.5-turbo")

        return finetune_service_pb2.FineTuneResponse(model_id=model_id, status="Fine-tuning started")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    finetune_service_pb2_grpc.add_FineTuneServiceServicer_to_server(FineTuneServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
