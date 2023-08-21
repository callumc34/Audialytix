from djongo import models


class Song(models.Model):
    STEREO = "stereo"
    MONO = "mono"
    AUDIO_CHOICES = [
        (STEREO, "Stereo"),
        (MONO, "Mono"),
    ]

    artist = models.CharField(max_length=255)
    song_name = models.CharField(max_length=255)
    audio_type = models.CharField(max_length=10, choices=AUDIO_CHOICES)
    audio_points = models.JSONField()  # Assuming this stores an array of doubles

    onset_analysis = models.JSONField(
        blank=True, null=True
    )  # Optional array of doubles
    spectral_analysis = models.JSONField(
        blank=True, null=True
    )  # Optional array of doubles

    def __str__(self):
        return f"{self.artist} - {self.song_name}"
