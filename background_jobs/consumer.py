import threading
import time

from background_jobs.job_queue import job_queue


class BackgroundConsumer:

    @staticmethod
    def process_job(job):

        print(f"[BACKGROUND JOB] Processing: {job}")

        # Simulate heavy computation
        time.sleep(2)

        print("[BACKGROUND JOB] Completed")

    @classmethod
    def worker(cls):

        while True:

            job = job_queue.get()

            try:
                cls.process_job(job)

            except Exception as e:
                print("Consumer Error:", e)

            finally:
                job_queue.task_done()

    @classmethod
    def start_consumer(cls):

        thread = threading.Thread(
            target=cls.worker,
            daemon=True
        )

        thread.start()

        print("Background consumer started")
