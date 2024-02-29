from typing import Any

from .domains_finder import (
    DOMAIN_FINDER,
    DomainFinder,
)


class DomainAnalyser:
    def __init__(self, domain: str) -> None:
        self.domain = domain

    def analyse(self) -> list[Any]:
        similar_domains = DOMAIN_FINDER.find(self.domain)

        findings: list[Any] = []

        for domain in similar_domains:
            findings.append(self._check_domain(domain))

        return findings

    def _check_domain(self, domain: str) -> Any: ...
