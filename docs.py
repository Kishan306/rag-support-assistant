# docs.py
# Fake documentation for "NovaSaaS" — a project management tool
# In a real product these would be loaded from .md files, a database, or a CMS

DOCS = [
    {
        "id": "billing-001",
        "title": "Refund Policy",
        "content": """NovaSaaS offers a 14-day money-back guarantee for all new subscriptions.
        To request a refund, go to Settings → Billing → Request Refund.
        Refunds are processed within 5-7 business days back to your original payment method.
        Refunds are not available after 14 days or if your account has been suspended for policy violations.
        Annual plan refunds are prorated based on unused months."""
    },
    {
        "id": "billing-002",
        "title": "Subscription Plans",
        "content": """NovaSaaS has three plans: Starter, Pro, and Enterprise.
        Starter is free forever with up to 3 projects and 1 user.
        Pro costs ₹799 per month and supports unlimited projects and up to 10 users.
        Enterprise costs ₹2999 per month with unlimited users, SSO, and a dedicated account manager.
        All paid plans include a 14-day free trial. No credit card required for trial."""
    },
    {
        "id": "account-001",
        "title": "Password Reset",
        "content": """To reset your password, click Forgot Password on the login page.
        Enter your registered email address and you will receive a reset link within 2 minutes.
        The reset link expires after 30 minutes.
        If you don't receive the email, check your spam folder or contact support@novasaas.com.
        For SSO users, password reset must be done through your identity provider, not NovaSaaS."""
    },
    {
        "id": "account-002",
        "title": "Adding Team Members",
        "content": """To add a team member, go to Settings → Team → Invite Member.
        Enter their email address and select their role: Viewer, Editor, or Admin.
        Viewers can only read projects. Editors can create and edit tasks. Admins have full access.
        Invitations expire after 48 hours. You can resend from Settings → Team → Pending Invites.
        On the Starter plan, you cannot add team members. Upgrade to Pro or Enterprise first."""
    },
    {
        "id": "technical-001",
        "title": "Exporting Data",
        "content": """NovaSaaS supports exporting your data in CSV and JSON formats.
        To export, go to Settings → Data → Export.
        You can export all projects, or select specific ones.
        Large exports are processed in the background and emailed to you when ready.
        Exports include tasks, comments, attachments metadata, and project history.
        The free Starter plan only supports CSV export of up to 100 tasks."""
    },
    {
        "id": "technical-002",
        "title": "API Access",
        "content": """NovaSaaS provides a REST API for Pro and Enterprise users.
        Generate your API key from Settings → Developer → API Keys.
        The API supports all CRUD operations on projects, tasks, and users.
        Rate limit is 1000 requests per hour on Pro, 10000 on Enterprise.
        API documentation is available at docs.novasaas.com/api.
        Webhook support is available on Enterprise plan only."""
    },
    {
        "id": "technical-003",
        "title": "Integrations",
        "content": """NovaSaaS integrates with Slack, Google Drive, GitHub, and Zapier.
        To connect an integration, go to Settings → Integrations and click Connect.
        Slack integration sends task notifications to your chosen channel.
        GitHub integration links commits and PRs to tasks automatically.
        Google Drive lets you attach Drive files directly to tasks.
        All integrations are available on Pro and Enterprise plans only."""
    },
    {
        "id": "general-001",
        "title": "Contacting Support",
        "content": """NovaSaaS support is available Monday to Friday, 9am to 6pm IST.
        You can reach support via email at support@novasaas.com or live chat in the app.
        Pro users get a response within 4 hours. Enterprise users get a response within 1 hour.
        Starter users get community support only via forum.novasaas.com.
        For critical production issues on Enterprise, call the emergency hotline in your welcome email."""
    },
]