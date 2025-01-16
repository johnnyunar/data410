from django.core.management.base import BaseCommand
from django.core.cache import cache
from metrics.models import RequestLog


class Command(BaseCommand):
    help = (
        "Flush cached request counts to the database and add counts to existing logs."
    )

    cache_key = "request_counts"

    def add_arguments(self, parser):
        parser.add_argument(
            "--cache-key",
            type=str,
            default="request_counts",
            help="Specify a custom cache key (useful for testing).",
        )

    def handle(self, *args, **kwargs):
        self.cache_key = kwargs["cache_key"]
        counts = self.get_cached_counts()

        if not counts:
            self.stdout.write(self.style.SUCCESS("No request counts to flush."))
            return

        existing_logs, new_logs = self.prepare_logs(counts)

        self.update_existing_logs(existing_logs)
        self.create_new_logs(new_logs)

        self.clear_cache()

        self.stdout.write(self.style.SUCCESS("Request counts flushed to the database."))

    def get_cached_counts(self):
        """
        Retrieve cached request counts.
        """
        return cache.get(self.cache_key, {})

    def prepare_logs(self, counts):
        """
        Prepare logs for update and creation.
        Returns a tuple of (existing_logs, new_logs).
        """
        paths_to_update = counts.keys()
        existing_logs = RequestLog.objects.filter(path__in=paths_to_update)
        existing_logs_dict = {log.path: log for log in existing_logs}

        new_logs = []
        for path, data in counts.items():
            if path in existing_logs_dict:
                # Update existing log
                log = existing_logs_dict[path]
                log.user_count += data["users"]
                log.bot_count += data["bots"]
            else:
                # Prepare new log
                new_logs.append(
                    RequestLog(
                        path=path, user_count=data["users"], bot_count=data["bots"]
                    )
                )

        return existing_logs_dict.values(), new_logs

    def update_existing_logs(self, logs):
        """
        Update counts for existing logs in bulk.
        """
        if logs:
            RequestLog.objects.bulk_update(logs, ["user_count", "bot_count"])
            self.stdout.write(f"Updated {len(logs)} existing logs.")

    def create_new_logs(self, logs):
        """
        Create new logs in bulk.
        """
        if logs:
            RequestLog.objects.bulk_create(logs)
            self.stdout.write(f"Created {len(logs)} new logs.")

    def clear_cache(self):
        """
        Clear the cached request counts.
        """
        cache.delete(self.cache_key)
        self.stdout.write("Cleared request counts cache.")
