from django.db import models

class PlayLog(models.Model):
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        fs = self.payload.get("final_score")
        return f"GameLog #{self.pk} (final_score={fs})"
