from djongo import models


class AudioAnalysis(models.Model):
    STEREO = "stereo"
    MONO = "mono"
    AUDIO_CHOICES = [
        (STEREO, "Stereo"),
        (MONO, "Mono"),
    ]

    error = models.CharField(max_length=255, blank=True, null=True)

    author = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    analysis_type = models.CharField(max_length=10, choices=AUDIO_CHOICES)
    audio_points = models.JSONField(
        blank=True, default=[], null=True
    )  # Assuming this stores an array of doubles

    onset_analysis = models.JSONField(
        blank=True, default=[], null=True
    )  # Optional array of doubles
    spectral_analysis = models.JSONField(
        blank=True, default=[], null=True
    )  # Optional array of doubles

    def __str__(self):
        return f"{self.author} - {self.name}"
