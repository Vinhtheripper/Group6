from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    logo = models.ImageField(upload_to="suppliers/", null=True, blank=True)

    def __str__(self):
        return self.name


class Certification(models.Model):
    STYLE_CHOICES = [
        ("pill-green", "Green"),
        ("pill-orange", "Orange"),
        ("pill-blue", "Blue"),
    ]

    name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    issued_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    document = models.FileField(upload_to="certifications/", null=True, blank=True)
    style_class = models.CharField(
        max_length=50,
        choices=STYLE_CHOICES,
        default="pill-green"
    )

    def __str__(self):
        return self.name

    @property
    def style_colors(self):
        """Trả về 3 màu: nền, chữ, viền"""
        mapping = {
            "pill-green": {
                "bg": "#eef7e8",
                "text": "#2d5b1a",
                "border": "#d8eac9",
            },
            "pill-orange": {
                "bg": "#fff3d9",
                "text": "#7a4200",
                "border": "#ffd390",
            },
            "pill-blue": {
                "bg": "#e6f0ff",
                "text": "#003366",
                "border": "#99c2ff",
            },
        }
        return mapping.get(self.style_class, mapping["pill-green"])