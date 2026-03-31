# FHCB Finance

AI-powered financial dashboard for community organizations.

## Structure

```
├── backend/          # Django + DRF API
│   ├── accounts/     # Org management + auth
│   ├── transactions/ # Uploads, parsing, categorization
│   ├── reports/      # Summary, P&L, monthly breakdowns
│   ├── chat/         # AI assistant (OpenAI proxy)
│   └── config/       # Django settings
└── frontend/         # Dashboard UI
    └── index.html
```

## API (RESTful, /api/v1/)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/login/ | Authenticate |
| GET | /orgs/ | List orgs (admin) |
| POST | /orgs/ | Create org (admin) |
| GET | /orgs/{slug}/ | Get org |
| PATCH | /orgs/{slug}/ | Update org |
| GET | /orgs/{slug}/transactions/ | List transactions |
| POST | /orgs/{slug}/transactions/ | Create transaction |
| GET | /orgs/{slug}/transactions/{id}/ | Get transaction |
| PATCH | /orgs/{slug}/transactions/{id}/ | Update transaction |
| DELETE | /orgs/{slug}/transactions/{id}/ | Delete transaction |
| POST | /orgs/{slug}/uploads/ | Upload CSV |
| GET | /orgs/{slug}/reports/summary/ | P&L summary |
| GET | /orgs/{slug}/reports/monthly/ | Monthly breakdown |
| GET | /orgs/{slug}/reports/categories/ | Category breakdown |
| POST | /orgs/{slug}/chat/ | AI assistant |
