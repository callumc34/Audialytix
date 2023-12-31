from django.db import models
from django.utils import timezone

STALE_ERROR = "There was an error processing this file."


class AudioFile(models.Model):
    STEREO = "stereo"
    MONO = "mono"
    AUDIO_CHOICES = [
        (STEREO, "Stereo"),
        (MONO, "Mono"),
    ]

    created_at = models.DateTimeField(auto_now_add=True)

    error = models.CharField(max_length=255, blank=True, null=True)

    author = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    analysis_type = models.CharField(max_length=10, choices=AUDIO_CHOICES)

    def __str__(self):
        return f"{self.author} - {self.name}"

    def _stale(self):
        if not self.fulfilled():
            time_difference = timezone.now() - self.created_at
            return time_difference > timezone.timedelta(minutes=5)

        return False

    def analysis_items(self):
        items = []
        if hasattr(self, "onsetdata"):
            items.append("onset")
        if hasattr(self, "spectraldata"):
            items.append("spectral")

        return items

    def is_stereo(self):
        return self.analysis_type == self.STEREO

    def fulfilled(self):
        return hasattr(self, "onsetdata") or hasattr(self, "spectraldata")

    def failed(self):
        if self.fulfilled():
            return False

        if self.error:
            return self.error

        if self._stale():
            return STALE_ERROR

        return False


class OnsetData(models.Model):
    data = models.JSONField()

    file = models.OneToOneField(AudioFile, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return str(self.analysis)


class SpectralData(models.Model):
    data = models.JSONField()

    file = models.OneToOneField(AudioFile, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return str(self.analysis)
