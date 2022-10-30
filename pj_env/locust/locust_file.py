from locust import HttpUser, task, between, TaskSet


class UserBehavior(TaskSet):
    @task(1)
    def users(self):
        response = self.client.post(
            "/predictions",
            json={"data": {"ndarray": [[1, 0.7998046875, 1, 263, 237, 1, 850]]}},
        )
        json_var = response.json()
        print(json_var)


class LocustUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(10, 20)
