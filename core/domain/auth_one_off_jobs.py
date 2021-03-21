class AuditUserEmailsOneOffJob(jobs.BaseMapReduceOneOffJobManager):
    """One-off job to confirm whether every user has a unique email address."""

    @classmethod
    def entity_classes_to_map_over(cls):
        return [user_models.UserSettingsModel]

    @staticmethod
    def reduce(email, user_ids):
        if len(user_ids) > 1:
            yield (
                'ERROR: %s is a shared email' % email,
                # NOTE: These are only sorted to make unit tests simpler.
                ', '.join(sorted(user_ids)))