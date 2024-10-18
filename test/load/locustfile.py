from locust import HttpUser, task


class LoadPaymentReceiveService(HttpUser):
    @task
    def payment_receipt(self):
        self.client.get("/api/payment_receipt")
