class JobStatusMailerHandler(base.BaseHandler):
    """Handler for mailing admin about job failures."""

    @acl_decorators.can_perform_cron_tasks
    def get(self):
        """Handles GET requests."""
        # TODO(sll): Get the 50 most recent failed shards, not all of them.
        failed_jobs = cron_services.get_stuck_jobs(TWENTY_FIVE_HOURS_IN_MSECS)
        if failed_jobs:
            email_subject = 'MapReduce failure alert'
            email_message = (
                '%s jobs have failed in the past 25 hours. More information '
                '(about at most %s jobs; to see more, please check the logs):'
            ) % (len(failed_jobs), MAX_JOBS_TO_REPORT_ON)

            for job in failed_jobs[:MAX_JOBS_TO_REPORT_ON]:
                email_message += '\n'
                email_message += '-----------------------------------'
                email_message += '\n'
                email_message += (
                    'Job with mapreduce ID %s (key name %s) failed. '
                    'More info:\n\n'
                    '  counters_map: %s\n'
                    '  shard_retries: %s\n'
                    '  slice_retries: %s\n'
                    '  last_update_time: %s\n'
                    '  last_work_item: %s\n'
                ) % (
                    job.mapreduce_id, job.key().name(), job.counters_map,
                    job.retries, job.slice_retries, job.update_time,
                    job.last_work_item
                )
        else:
            email_subject = 'MapReduce status report'
            email_message = 'All MapReduce jobs are running fine.'

        email_manager.send_mail_to_admin(email_subject, email_message)