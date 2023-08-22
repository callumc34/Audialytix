from djongo import models


class AudioFile(models.Model):
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

    def __str__(self):
        return f"{self.author} - {self.name}"

    def is_stereo(self):
        return self.analysis_type == self.STEREO


class OnsetData(models.Model):
    onset_analysis = models.JSONField()

    analysis = models.OneToOneField(
        AudioFile, on_delete=models.CASCADE, primary_key=True
    )

    def __str__(self):
        return str(self.analysis)


class SpectralData(models.Model):
    spectral_analysis = models.JSONField()

    analysis = models.OneToOneField(
        AudioFile, on_delete=models.CASCADE, primary_key=True
    )

    def __str__(self):
        return str(self.analysis)
