# from django.core.management.base import (
#     BaseCommand,
#     CommandError,
#     CommandParser,
# )

# from proactive_analysis.suspicious_domain_analyser import DomainAnalyser


# class Command(BaseCommand):
#     help = "Analyses the given domain"

#     def add_arguments(self, parser: CommandParser) -> None:
#         parser.add_argument("domain", type=str)

#     def handle(self, *args, **options) -> None:
#         domain: str = options["domain"]

#         results = DomainAnalyser(domain).analyse()

#         self.stdout.write(str(results))
