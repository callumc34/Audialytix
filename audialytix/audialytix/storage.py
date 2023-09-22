from django.core.files.storage import get_storage_class
from storages.backends.gcloud import GoogleCloudStorage


class CachedCloudStorage(GoogleCloudStorage):
    """
    Google cloud storage backend that saves the files locally, too.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage"
        )()

    def save(self, name, content):
        self.local_storage.save(name, content)
        super().save(name, self.local_storage._open(name))
        return name
