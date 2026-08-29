from locust import HttpUser, task, between


class LedgerCoreUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def ping(self):
        self.client.get("/ping")