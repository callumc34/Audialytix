from django.db import models


class AudioFile(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class OnsetProcessResult(models.Model):
    audio_file = models.OneToOneField(
        AudioFile, on_delete=models.CASCADE, related_name="onset_result"
    )
    onset_data = models.JSONField()

    def __str__(self):
        return f"Onset Result for {self.audio_file.name}"


class SpectralProcessResult(models.Model):
    audio_file = models.OneToOneField(
        AudioFile,
        on_delete=models.CASCADE,
        related_name="spectral_result",
    )
    spectral_data = models.JSONField()

    def __str__(self):
        return f"Spectral Result for {self.audio_file.name}"
