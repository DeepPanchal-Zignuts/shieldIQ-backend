from uuid import UUID
from django.db.models import Sum

from apps.campaigns.repositories.campaign_repository import CampaignRepository
from apps.events.models.campaign_events_model import CampaignEvents
from apps.users.models.user_model import Users
from common.constants.constants import CampaignEventsEnum


class CampaignStatsService:
    # ──────────────────────────────────────────────
    # 1. AVERAGE SCORE
    # The average of score_impact sum per user for this campaign.
    # Each user's campaign score = sum of all their score_impacts in this campaign.
    # We then average that across all users who were targeted.
    # ──────────────────────────────────────────────
    @staticmethod
    def get_average_score(campaign_id: int) -> float:
        """
        Returns the average security score impact across all targeted users
        for a given campaign.

        Step 1: For each user, sum their score_impact across all events in this campaign.
        Step 2: Average those sums across all users.
        """
        # Aggregate score per user first, then average across users
        per_user_scores = (
            CampaignEvents.objects.filter(campaign_id=campaign_id)
            .values("user_id")  # group by user
            .annotate(user_total_impact=Sum("score_impact"))  # sum per user
        )

        if not per_user_scores.exists():
            return 0.0

        total = sum(u["user_total_impact"] for u in per_user_scores)
        return round(total / per_user_scores.count(), 2)

    # ──────────────────────────────────────────────
    # 2. CLICK RATE
    # % of targeted users who clicked on at least one phishing email.
    # Only counts emails where is_phishing=True.
    # One user clicking multiple times still counts as 1.
    # ──────────────────────────────────────────────
    @staticmethod
    def get_click_rate(campaign_id: int) -> float:
        """
        Returns the click rate as a percentage (0-100).

        Numerator:   distinct users who have a LINK_CLICKED event
                     on a phishing email in this campaign.
        Denominator: distinct users who were sent any email in this campaign.
        """
        total_targeted = (
            CampaignEvents.objects.filter(
                campaign_id=campaign_id,
                event_type=CampaignEventsEnum.SENT,
            )
            .values("user_id")
            .distinct()
            .count()
        )

        if total_targeted == 0:
            return 0.0

        users_who_clicked = (
            CampaignEvents.objects.filter(
                campaign_id=campaign_id,
                event_type=CampaignEventsEnum.LINK_CLICKED,
                campaign_email__is_phishing=True,  # only phishing emails count
            )
            .values("user_id")
            .distinct()
            .count()
        )

        return round((users_who_clicked / total_targeted) * 100, 2)

    # ──────────────────────────────────────────────
    # 3. REPORT RATE
    # % of targeted users who reported at least one phishing email.
    # Reporting a safe email (false positive) does NOT count here.
    # ──────────────────────────────────────────────
    @staticmethod
    def get_report_rate(campaign_id: int) -> float:
        """
        Returns the report rate as a percentage (0-100).

        Numerator:   distinct users who REPORTED a phishing email
                     (is_phishing=True) in this campaign.
        Denominator: distinct users who were sent any email in this campaign.

        NOTE: Reporting a safe/decoy email is a false positive — excluded here.
        """
        total_targeted = (
            CampaignEvents.objects.filter(
                campaign_id=campaign_id,
                event_type=CampaignEventsEnum.SENT,
            )
            .values("user_id")
            .distinct()
            .count()
        )

        if total_targeted == 0:
            return 0.0

        users_who_reported = (
            CampaignEvents.objects.filter(
                campaign_id=campaign_id,
                event_type=CampaignEventsEnum.REPORTED,
                campaign_email__is_phishing=True,  # only true phishing reports count
            )
            .values("user_id")
            .distinct()
            .count()
        )

        return round((users_who_reported / total_targeted) * 100, 2)

    # ──────────────────────────────────────────────
    # 4. ACTIVE USERS
    # Total number of active (non-deleted) users in the system.
    # Not campaign-specific — this is a global org metric.
    # ──────────────────────────────────────────────
    @staticmethod
    def get_active_users() -> int:
        """
        Returns total count of active, non-deleted users.
        Used for the admin dashboard org-wide stat card.
        """
        return Users.objects.filter(
            is_active=True,
            is_deleted=False,
        ).count()

    # ──────────────────────────────────────────────
    # 5. PROGRESS
    # How many users have interacted with at least one email
    # out of total users targeted by this campaign.
    # "Interacted" = any event beyond SENT (OPENED, CLICKED, REPORTED)
    # ──────────────────────────────────────────────
    @staticmethod
    def get_progress(campaign_id: int) -> dict:
        """
        Returns a dict with interacted count and total targeted count.
        e.g. {"interacted": 18, "total": 25}

        "Interacted" means the user performed at least one action
        beyond just being sent the email (OPENED, LINK_CLICKED, REPORTED).

        Frontend can display this as "18 / 25" or as a percentage.
        """
        total_targeted = (
            CampaignEvents.objects.filter(
                campaign_id=campaign_id,
                event_type=CampaignEventsEnum.SENT,
            )
            .values("user_id")
            .distinct()
            .count()
        )

        users_interacted = (
            CampaignEvents.objects.filter(
                campaign_id=campaign_id,
                event_type__in=[
                    CampaignEventsEnum.OPENED,
                    CampaignEventsEnum.LINK_CLICKED,
                    CampaignEventsEnum.REPORTED,
                ],
            )
            .values("user_id")
            .distinct()
            .count()
        )

        return {
            "interacted": users_interacted,
            "total": total_targeted,
            "percentage": round(
                (users_interacted / total_targeted * 100) if total_targeted else 0, 2
            ),
        }

    # ──────────────────────────────────────────────
    # COMBINED — Get all stats for one campaign in one call
    # Use this in the campaign list/detail API to avoid
    # 5 separate service calls per campaign.
    # ──────────────────────────────────────────────
    @classmethod
    def get_campaign_stats(cls, campaign_id: int) -> dict:
        """
        Returns all stats for a single campaign in one call.
        Use this for the campaign list and campaign detail endpoints.
        """
        return {
            "average_score": cls.get_average_score(campaign_id),
            "click_rate": cls.get_click_rate(campaign_id),
            "report_rate": cls.get_report_rate(campaign_id),
            "active_users": cls.get_active_users(),
            "progress": cls.get_progress(campaign_id),
        }

    # ──────────────────────────────────────────────
    # ADMIN DASHBOARD — All campaigns aggregated
    # Each metric is ONE DB query, no loops, no N+1.
    # ──────────────────────────────────────────────

    @staticmethod
    def get_dashboard_average_score() -> float:
        """
        Average score impact per user across ALL campaigns.

        Step 1: Sum score_impact per user across all events (no campaign filter).
        Step 2: Average those sums across all users who appear in events.

        This reflects the org-wide average security posture.
        """
        per_user_scores = CampaignEvents.objects.values(
            "user_id"
        ).annotate(  # group by user, no campaign filter
            user_total_impact=Sum("score_impact")
        )  # sum all impacts per user

        if not per_user_scores.exists():
            return 0.0

        total = sum(u["user_total_impact"] for u in per_user_scores)
        return round(total / per_user_scores.count(), 2)

    @staticmethod
    def get_dashboard_click_rate() -> float:
        """
        % of targeted users who clicked at least one phishing email
        across ALL campaigns.

        Numerator:   distinct users with a LINK_CLICKED event on is_phishing=True
        Denominator: distinct users who received a SENT event (across all campaigns)

        NOTE: A user targeted in 3 campaigns still counts as 1 in the denominator
        because we're measuring unique users, not campaign-user pairs.
        """
        total_targeted = (
            CampaignEvents.objects.filter(event_type=CampaignEventsEnum.SENT)
            .values("user_id")
            .distinct()
            .count()
        )

        if total_targeted == 0:
            return 0.0

        users_who_clicked = (
            CampaignEvents.objects.filter(
                event_type=CampaignEventsEnum.LINK_CLICKED,
                campaign_email__is_phishing=True,
            )
            .values("user_id")
            .distinct()
            .count()
        )

        return round((users_who_clicked / total_targeted) * 100, 2)

    @staticmethod
    def get_dashboard_report_rate() -> float:
        """
        % of targeted users who correctly reported at least one phishing email
        across ALL campaigns.

        Numerator:   distinct users with a REPORTED event on is_phishing=True
        Denominator: distinct users who received a SENT event (across all campaigns)
        """
        total_targeted = (
            CampaignEvents.objects.filter(event_type=CampaignEventsEnum.SENT)
            .values("user_id")
            .distinct()
            .count()
        )

        if total_targeted == 0:
            return 0.0

        users_who_reported = (
            CampaignEvents.objects.filter(
                event_type=CampaignEventsEnum.REPORTED,
                campaign_email__is_phishing=True,
            )
            .values("user_id")
            .distinct()
            .count()
        )

        return round((users_who_reported / total_targeted) * 100, 2)

    @staticmethod
    def get_dashboard_progress() -> dict:
        """
        Org-wide progress across ALL campaigns.

        total:       distinct users who were sent at least one email
        interacted:  distinct users who performed any action beyond SENT

        Returns the same shape as get_progress() so the frontend
        handles both identically.
        """
        total_targeted = (
            CampaignEvents.objects.filter(event_type=CampaignEventsEnum.SENT)
            .values("user_id")
            .distinct()
            .count()
        )

        users_interacted = (
            CampaignEvents.objects.filter(
                event_type__in=[
                    CampaignEventsEnum.OPENED,
                    CampaignEventsEnum.LINK_CLICKED,
                    CampaignEventsEnum.REPORTED,
                ]
            )
            .values("user_id")
            .distinct()
            .count()
        )

        return {
            "interacted": users_interacted,
            "total": total_targeted,
            "percentage": round(
                (users_interacted / total_targeted * 100) if total_targeted else 0, 2
            ),
        }

    @classmethod
    def get_admin_dashboard(cls) -> dict:
        """
        Returns all org-wide stats in one call using exactly 5 DB queries,
        regardless of how many campaigns exist.

        Used by GET /api/v1/admin/stats/
        """
        return {
            "average_score": cls.get_dashboard_average_score(),  # query 1
            "click_rate": cls.get_dashboard_click_rate(),  # query 2 + 3
            "report_rate": cls.get_dashboard_report_rate(),  # query 4 + 5 (shares denominator)
            "active_users": cls.get_active_users(),  # query 6
            "progress": cls.get_dashboard_progress(),  # query 7 + 8
        }
