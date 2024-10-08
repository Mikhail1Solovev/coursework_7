from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

title = "Habit Tracker API"
description = "API documentation for the Habit Tracker application."
schema_view = get_schema_view(title=title, description=description)
include_docs_urls = include_docs_urls
