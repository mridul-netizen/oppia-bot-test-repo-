"""Main package for URL routing and the index page."""

from __future__ import absolute_import  # pylint: disable=import-only-modules
from __future__ import unicode_literals  # pylint: disable=import-only-modules

from core.controllers import cron
from core.platform import models
import feconf
import main

import webapp2


transaction_services = models.Registry.import_transaction_services()

# Register the URLs with the classes responsible for handling them.
URLS = [
    main.get_redirect_route(
        r'/cron/mail/admin/job_status', cron.JobStatusMailerHandler),
    main.get_redirect_route(
        r'/cron/users/dashboard_stats', cron.CronDashboardStatsHandler),
    main.get_redirect_route(
        r'/cron/users/user_deletion', cron.CronUserDeletionHandler),
    main.get_redirect_route(
        r'/cron/users/fully_complete_user_deletion',
        cron.CronFullyCompleteUserDeletionHandler),
    main.get_redirect_route(
        r'/cron/explorations/recommendations',
        cron.CronExplorationRecommendationsHandler),
    main.get_redirect_route(
        r'/cron/explorations/search_rank',
        cron.CronActivitySearchRankHandler),
    main.get_redirect_route(
        r'/cron/jobs/cleanup', cron.CronMapreduceCleanupHandler),
    main.get_redirect_route(
        r'/cron/models/cleanup', cron.CronModelsCleanupHandler),
    main.get_redirect_route(
        r'/cron/mail/admins/contributor_dashboard_bottlenecks',
        cron.CronMailAdminContributorDashboardBottlenecksHandler),
    main.get_redirect_route(
        r'/cron/mail/reviewers/contributor_dashboard_suggestions',
        cron.CronMailReviewersContributorDashboardSuggestionsHandler),
]

app = transaction_services.toplevel_wrapper(  # pylint: disable=invalid-name
    webapp2.WSGIApplication(URLS, debug=feconf.DEBUG))
