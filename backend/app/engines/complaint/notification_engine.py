from app.engines.base.base_engine import BaseEngine


class NotificationEngine(BaseEngine):
    """
    Handles complaint notifications.
    """

    def notify(self, complaint):
        """
        Send notification after complaint registration.

        TODO:
        - SMS
        - Email
        - WhatsApp
        - Push Notification
        """
        return self.send(complaint)

    def send(self, complaint):
        """
        Actual notification sending layer.

        Currently this is a placeholder.
        """
        return True


notification_engine = NotificationEngine()
