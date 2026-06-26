from background_jobs.job_queue import job_queue


class BookingProducer:

    @staticmethod
    def submit_job(job_type, payload):

        job = {
            "type": job_type,
            "payload": payload
        }

        job_queue.put(job)

        return True
