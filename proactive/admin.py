from django.contrib import admin
from .models import SimilarDomain


# Register your models here.
@admin.register(SimilarDomain)
class SimilarDomainAdmin(admin.ModelAdmin):
    list_display = ["name"]
    readonly_fields = (
        "name",
        "found_date",
        "original_domain",
        "creation_date",
        "updated_date",
        "expiration_date",
        "tld_country",
        "ip_countries",
        "is_certificate_tls",
        "tls_certificate_ca",
        "tls_certificate_creation_date",
        "tls_certificate_oldest_date",
        "final_url",
        "is_redirect_same_domain",
        "has_redirect_special_chars",
        "internal_links",
        "external_links",
        "is_original_domain",
        "is_login_form",
        "bad_links",
        "visual_similarity",
        "paas_tools",
        "is_phishing",
        "total_weight",
        "last_analysis_date",
        "next_analysis_date",
    )
