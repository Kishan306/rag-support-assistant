# docs.py
# Realistic NovaSaaS documentation — longer, messier, like real docs

DOCS = [
    {
        "id": "billing",
        "title": "Billing and Payments",
        "content": """NovaSaaS Billing and Payments Guide

Subscription Plans
NovaSaaS offers three subscription tiers designed for teams of all sizes.

The Starter plan is free forever and includes up to 3 projects and 1 user. 
It supports basic task management and CSV export of up to 100 tasks. 
Starter users receive community support only via forum.novasaas.com.

The Pro plan costs rupees 799 per month and supports unlimited projects 
and up to 10 users. It includes API access, all integrations, priority 
support with 4 hour response time, and unlimited data export in CSV and 
JSON formats. Pro users can generate API keys from Settings Developer API Keys.

The Enterprise plan costs rupees 2999 per month with unlimited users. 
It includes everything in Pro plus SSO login, a dedicated account manager, 
1 hour support response time, webhook support, and an emergency hotline 
for critical production issues. Enterprise is suited for large organizations 
with security and compliance requirements.

All paid plans include a 14 day free trial with no credit card required.

Refund Policy
NovaSaaS offers a 14 day money back guarantee for all new subscriptions.
To request a refund go to Settings then Billing then Request Refund.
Refunds are processed within 5 to 7 business days back to your original 
payment method. Refunds are not available after 14 days or if your account 
has been suspended for policy violations. Annual plan refunds are prorated 
based on unused months remaining in your billing cycle.

Payment Methods
NovaSaaS accepts all major credit and debit cards including Visa, Mastercard, 
and American Express. Indian users can also pay via UPI and net banking.
All payments are processed securely via Stripe. NovaSaaS does not store 
your card details on our servers. For GST invoices, add your GSTIN from 
Settings then Billing then Tax Information before your next billing cycle."""
    },
    {
        "id": "account",
        "title": "Account Management",
        "content": """NovaSaaS Account Management Guide

Password Reset
To reset your password click Forgot Password on the login page.
Enter your registered email address and you will receive a reset link 
within 2 minutes. The reset link expires after 30 minutes. If you do 
not receive the email check your spam folder or contact support at 
support@novasaas.com. For SSO users password reset must be done through 
your identity provider and not through NovaSaaS directly.

Two Factor Authentication
NovaSaaS supports two factor authentication via authenticator apps such 
as Google Authenticator and Authy. To enable 2FA go to Settings then 
Security then Enable Two Factor Authentication. Scan the QR code with 
your authenticator app and enter the 6 digit code to confirm. 
Recovery codes are provided during setup and should be stored safely. 
If you lose access to your authenticator app contact support with your 
recovery code. Enterprise users can enforce 2FA for all team members 
from the admin panel.

Adding Team Members
To add a team member go to Settings then Team then Invite Member.
Enter their email address and select their role as Viewer, Editor, or Admin.
Viewers can only read projects. Editors can create and edit tasks. 
Admins have full access including billing and team management.
Invitations expire after 48 hours. You can resend from Settings then 
Team then Pending Invites. On the Starter plan you cannot add team members 
and must upgrade to Pro or Enterprise first.

Deleting Your Account
To delete your account go to Settings then Account then Delete Account.
This action is permanent and cannot be undone. All your projects, tasks, 
and data will be deleted immediately. If you are on a paid plan your 
subscription will be cancelled and a prorated refund issued if within 
the 14 day guarantee window. Export your data before deleting from 
Settings then Data then Export."""
    },
    {
        "id": "technical",
        "title": "Technical and Integrations",
        "content": """NovaSaaS Technical Guide

API Access
NovaSaaS provides a REST API for Pro and Enterprise users.
Generate your API key from Settings then Developer then API Keys.
The API supports all CRUD operations on projects, tasks, and users.
Rate limit is 1000 requests per hour on Pro and 10000 on Enterprise.
Full API documentation is available at docs.novasaas.com/api.
Webhook support for real time event notifications is available on 
Enterprise plan only. API keys should be kept secret and never exposed 
in client side code or public repositories.

Data Export
NovaSaaS supports exporting your data in CSV and JSON formats.
To export go to Settings then Data then Export.
You can export all projects or select specific ones.
Large exports are processed in the background and emailed when ready.
Exports include tasks, comments, attachment metadata, and project history.
The free Starter plan only supports CSV export of up to 100 tasks.

Integrations
NovaSaaS integrates with Slack, Google Drive, GitHub, and Zapier.
To connect an integration go to Settings then Integrations and click Connect.
Slack integration sends task notifications and mentions to your chosen channel.
GitHub integration links commits and pull requests to tasks automatically 
by including the task ID in your commit message.
Google Drive lets you attach Drive files directly to tasks and see previews.
Zapier integration allows connecting NovaSaaS to over 5000 other apps.
All integrations are available on Pro and Enterprise plans only.

Performance and Uptime
NovaSaaS maintains 99.9 percent uptime SLA for Pro and Enterprise users.
Scheduled maintenance windows are announced 48 hours in advance via email 
and status.novasaas.com. For real time status updates and incident history 
visit status.novasaas.com. Enterprise users receive direct incident 
notifications via their account manager."""
    }
]