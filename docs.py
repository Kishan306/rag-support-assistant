# docs.py
# Expanded documentation for "NovaSaaS" — a project management tool
# In a real product these would be loaded from .md files, a database, or a CMS

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
Starter does not include API access, integrations, or team members.

The Pro plan costs rupees 799 per month and supports unlimited projects
and up to 10 users. It includes API access, all integrations, priority
support with 4 hour response time, and unlimited data export in CSV and
JSON formats. Pro users can generate API keys from Settings Developer API Keys.
Pro also includes custom fields, recurring tasks, and the Gantt chart view.

The Enterprise plan costs rupees 2999 per month with unlimited users.
It includes everything in Pro plus SSO login, a dedicated account manager,
1 hour support response time, webhook support, an emergency hotline
for critical production issues, audit logs, and custom data residency options.
Enterprise is suited for large organizations with security and compliance
requirements.

All paid plans include a 14 day free trial with no credit card required.
You can switch between monthly and annual billing at any time from
Settings then Billing then Change Billing Cycle. Annual billing gives a
2 month discount compared to paying monthly.

Refund Policy
NovaSaaS offers a 14 day money back guarantee for all new subscriptions.
To request a refund go to Settings then Billing then Request Refund.
Refunds are processed within 5 to 7 business days back to your original
payment method. Refunds are not available after 14 days or if your account
has been suspended for policy violations. Annual plan refunds are prorated
based on unused months remaining in your billing cycle. Enterprise plan
refunds for custom contracts follow the terms in your signed agreement
rather than the standard 14 day policy.

Payment Methods
NovaSaaS accepts all major credit and debit cards including Visa, Mastercard,
and American Express. Indian users can also pay via UPI and net banking.
All payments are processed securely via Stripe. NovaSaaS does not store
your card details on our servers. For GST invoices, add your GSTIN from
Settings then Billing then Tax Information before your next billing cycle.
Enterprise customers can request invoice-based billing with net-30 payment
terms by contacting your account manager.

Upgrading and Downgrading
You can upgrade your plan at any time from Settings then Billing then
Change Plan. Upgrades take effect immediately and you are charged a
prorated amount for the remainder of the billing cycle. Downgrades take
effect at the end of the current billing cycle, so you keep access to
your current plan's features until then. Downgrading from Pro or Enterprise
to Starter will archive any projects beyond the Starter plan's limit of 3;
archived projects are not deleted and can be restored by upgrading again.

Failed Payments
If a payment fails, NovaSaaS retries the charge automatically after 3 days,
then again after 7 days. You will receive an email notification after each
failed attempt. If payment continues to fail after 14 days, your account
is downgraded to the Starter plan automatically, and any data beyond
Starter limits is archived, not deleted."""
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
from the admin panel under Settings then Security then Require 2FA.

Adding Team Members
To add a team member go to Settings then Team then Invite Member.
Enter their email address and select their role as Viewer, Editor, or Admin.
Viewers can only read projects. Editors can create and edit tasks.
Admins have full access including billing and team management.
Invitations expire after 48 hours. You can resend from Settings then
Team then Pending Invites. On the Starter plan you cannot add team members
and must upgrade to Pro or Enterprise first.

Roles and Permissions
NovaSaaS has four permission levels. Owner is the account creator and has
full control including the ability to delete the entire workspace and
transfer ownership. Admin can manage billing, team members, and all
projects but cannot delete the workspace. Editor can create, edit, and
delete tasks and comments within projects they are added to, but cannot
manage billing or team members. Viewer has read-only access to projects
they are added to. Permissions can be changed at any time from Settings
then Team then click on a member's current role.

Transferring Ownership
To transfer account ownership, go to Settings then Team then find the
member you want to make the new owner, then click Transfer Ownership.
The new owner must accept the transfer via an email confirmation link
within 24 hours. Once accepted, the previous owner is automatically
downgraded to Admin role. Ownership transfer cannot be undone except by
the new owner transferring it back.

Deleting Your Account
To delete your account go to Settings then Account then Delete Account.
This action is permanent and cannot be undone. All your projects, tasks,
and data will be deleted immediately. If you are on a paid plan your
subscription will be cancelled and a prorated refund issued if within
the 14 day guarantee window. Export your data before deleting from
Settings then Data then Export. Only the account Owner can delete the
entire workspace; Admins can only remove their own individual user account.

Session Management
NovaSaaS keeps you logged in for 30 days by default. You can view all
active sessions and devices from Settings then Security then Active
Sessions, and revoke access to any device remotely. Enterprise accounts
can configure a shorter maximum session length for compliance purposes
from the admin panel."""
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
in client side code or public repositories. API keys can be rotated
at any time from the same settings page; the old key stops working
immediately once a new one is generated.

Webhooks
Enterprise users can configure webhooks from Settings then Developer
then Webhooks. Webhooks can be triggered on task creation, task
completion, comment added, and project archived events. Each webhook
delivery includes a signature header so you can verify the payload
came from NovaSaaS. Failed webhook deliveries are retried up to 5 times
with exponential backoff before being marked as failed permanently.

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

Single Sign-On (SSO)
Enterprise customers can configure SSO using SAML 2.0 or OpenID Connect.
Supported identity providers include Okta, Azure AD, Google Workspace,
and OneLogin. To set up SSO, contact your account manager, who will
provide a configuration guide specific to your identity provider.
Once SSO is enabled, all team members must log in through the identity
provider; password-based login is disabled for that workspace.

Performance and Uptime
NovaSaaS maintains 99.9 percent uptime SLA for Pro and Enterprise users.
Scheduled maintenance windows are announced 48 hours in advance via email
and status.novasaas.com. For real time status updates and incident history
visit status.novasaas.com. Enterprise users receive direct incident
notifications via their account manager.

Data Residency and Compliance
By default, NovaSaaS stores all data in servers located in the United
States. Enterprise customers can request data residency in the European
Union or India for an additional fee. NovaSaaS is SOC 2 Type II certified
and GDPR compliant. A Data Processing Agreement (DPA) is available for
Enterprise customers upon request from your account manager.

Audit Logs
Enterprise accounts have access to audit logs showing every significant
action taken in the workspace, including logins, permission changes,
project deletions, and billing changes. Audit logs can be viewed from
Settings then Security then Audit Log, and exported as CSV for compliance
reviews. Audit logs are retained for 12 months."""
    },
    {
        "id": "getting-started",
        "title": "Getting Started",
        "content": """NovaSaaS Getting Started Guide

Creating Your First Project
After signing up, click Create Project on the dashboard. Give your project
a name and choose a template, or start from a blank project. Templates
include Software Sprint, Marketing Campaign, and Simple To-Do List, each
pre-populated with common task structures you can customize.

Creating Tasks
Within a project, click Add Task to create a new task. Each task has a
title, description, assignee, due date, priority, and status. Tasks can
be organized into sections or lists within a project. You can create
sub-tasks by clicking the sub-task icon within any task, useful for
breaking larger work into smaller steps.

Views: List, Board, Calendar, and Gantt
NovaSaaS offers four ways to view your project. List view shows tasks
as a simple sortable table. Board view (Kanban) organizes tasks into
columns like To Do, In Progress, and Done, which you can customize.
Calendar view shows tasks on the dates they are due. Gantt view, available
on Pro and Enterprise, shows task timelines and dependencies visually.
Switch between views using the tabs at the top of any project.

Assigning and Notifying
Assign a task to a team member by clicking the assignee field and
selecting their name. The assignee receives an email and in-app
notification. You can mention any team member in a comment using the
@ symbol followed by their name, which sends them a direct notification
regardless of whether they are assigned to the task.

Onboarding Checklist
New workspaces see a getting-started checklist on the dashboard covering:
inviting your first team member, creating your first project, connecting
an integration, and setting your notification preferences. This checklist
can be dismissed at any time and does not affect account functionality.

Migrating From Another Tool
NovaSaaS supports importing data from Trello, Asana, and Jira via
Settings then Data then Import. Uploads must be in CSV format matching
the template provided on that page, or you can use the native Trello
and Asana one-click importers which map projects, tasks, and assignees
automatically. Imports typically take under 10 minutes for workspaces
with fewer than 5000 tasks."""
    },
    {
        "id": "task-features",
        "title": "Task Features and Organization",
        "content": """NovaSaaS Task Features Guide

Custom Fields
Pro and Enterprise plans support custom fields, letting you add extra
structured data to tasks beyond the defaults. Supported field types are
text, number, dropdown, checkbox, and date. Create custom fields from
Settings then Project Settings then Custom Fields. Custom fields appear
as additional columns in List view and as tags in Board view.

Recurring Tasks
To make a task repeat, open the task and click Set Recurrence. Choose
daily, weekly, monthly, or a custom interval. When a recurring task is
marked complete, the next occurrence is automatically created based on
the schedule. Recurring tasks are available on Pro and Enterprise plans.

Task Dependencies
You can mark one task as blocked by another using the Dependencies field
within a task. Blocked tasks are visually flagged in List and Gantt views.
Dependencies are informational only in List and Board view but affect
scheduling calculations in Gantt view, where a delay to a blocking task
automatically shifts the dependent task's suggested dates.

Comments and Collaboration
Every task has a comment thread where team members can discuss progress,
attach files, and use @ mentions to notify specific people. Comments
support basic formatting and can be edited or deleted by their author
within 15 minutes of posting. Deleted comments are not recoverable.

File Attachments
Files can be attached directly to tasks by dragging and dropping, or by
linking a Google Drive file if that integration is connected. Maximum
file size for direct uploads is 25 MB on Starter and Pro, and 250 MB on
Enterprise. Total storage included is 5 GB on Starter, 100 GB on Pro,
and unlimited on Enterprise.

Task Templates
Frequently repeated task structures can be saved as templates from any
task's menu by selecting Save as Template. Templates can then be applied
to new tasks from the Create Task dialog, pre-filling the description,
sub-tasks, and custom field values.

Search and Filters
The global search bar, accessible from any page, searches across task
titles, descriptions, and comments in projects you have access to.
Advanced filters let you narrow results by assignee, due date range,
priority, status, and custom field values. Saved filters can be pinned
to your sidebar for quick access.

Time Tracking
Pro and Enterprise users can log time against tasks using the built-in
timer or by manually entering hours. Time reports can be viewed per
project, per person, or per date range from the Reports tab, and
exported as CSV for invoicing or payroll purposes."""
    },
    {
        "id": "notifications",
        "title": "Notifications and Preferences",
        "content": """NovaSaaS Notifications Guide

Notification Channels
NovaSaaS can notify you via in-app notifications, email, and a mobile
push notification if you have the mobile app installed. Configure which
events trigger which channels from Settings then Notifications.

Default Notification Events
By default you are notified when: you are assigned a task, someone
mentions you in a comment, a due date is approaching within 24 hours,
or someone comments on a task you are following. You automatically
follow any task you create or are assigned to; you can manually follow
or unfollow any task using the bell icon on the task.

Digest Emails
Instead of individual emails for every event, you can switch to a daily
or weekly digest from Settings then Notifications then Email Frequency.
Digests summarize all activity across your projects since the last digest
was sent, reducing email volume for busy workspaces.

Do Not Disturb
You can set quiet hours during which push and email notifications are
paused, from Settings then Notifications then Do Not Disturb. In-app
notifications still appear in your notification center regardless of
quiet hours settings; only external pushes and emails are paused.

Project-Level Notification Overrides
Within any project, click the bell icon at the top to override your
global notification settings just for that project — useful for muting
a project you're only occasionally involved in without changing your
notification preferences everywhere else."""
    },
    {
        "id": "mobile-and-offline",
        "title": "Mobile App and Offline Mode",
        "content": """NovaSaaS Mobile App Guide

Availability
The NovaSaaS mobile app is available for iOS 14 and above, and Android
9 and above, downloadable from the App Store and Google Play. The mobile
app is included free with every plan, including Starter.

Feature Parity
The mobile app supports viewing and editing tasks, adding comments,
receiving push notifications, and Board view. Gantt view and time
tracking reports are currently desktop and web only, though time can
still be logged from mobile using the quick-log timer.

Offline Mode
The mobile app caches your most recently viewed projects for offline
access. You can view, and create new tasks, while offline; changes sync
automatically once your device reconnects to the internet. If the same
task was edited by someone else while you were offline, NovaSaaS will
prompt you to choose which version to keep, or merge changes manually.

Biometric Login
The mobile app supports Face ID and fingerprint login as a fast
alternative to entering your password each time, once you have logged
in with your normal credentials at least once on that device. Biometric
login can be disabled from the app's Settings then Security menu.

Dark Mode
NovaSaaS supports dark mode on both mobile and web. On mobile it follows
your device's system setting by default, or can be forced on or off from
Settings then Appearance. On web, toggle dark mode from the icon in the
top right of any page."""
    },
    {
        "id": "support-and-troubleshooting",
        "title": "Support and Troubleshooting",
        "content": """NovaSaaS Support Guide

Contacting Support
NovaSaaS support is available Monday to Friday, 9am to 6pm IST.
You can reach support via email at support@novasaas.com or live chat in the app.
Pro users get a response within 4 hours. Enterprise users get a response within 1 hour.
Starter users get community support only via forum.novasaas.com.
For critical production issues on Enterprise, call the emergency hotline in your welcome email.

Support Tiers Summary
Starter: community forum only, no guaranteed response time.
Pro: email and live chat, 4 hour response time during business hours.
Enterprise: email, live chat, dedicated account manager, 1 hour response
time, and a 24/7 emergency hotline for critical production incidents only.

Common Issue: Tasks Not Syncing
If tasks appear out of date across devices, first check your internet
connection, then try a manual refresh by pulling down on the task list.
If the issue persists, log out and back in. If tasks still fail to sync,
contact support with your workspace ID, found in Settings then Account.

Common Issue: Emails Not Arriving
If you are not receiving notification or invitation emails, check your
spam folder first, and verify your email address is correct in Settings
then Account then Profile. Some corporate email systems block automated
emails; ask your IT department to allowlist the domain novasaas.com.

Common Issue: Slow Loading
If NovaSaaS is loading slowly, check status.novasaas.com for any ongoing
incidents first. Clearing your browser cache and disabling browser
extensions can also resolve slow loading caused by local conflicts.
Projects with more than 10,000 tasks may load more slowly in List view;
using filters to narrow the visible task count improves performance.

Reporting a Bug
To report a bug, use the Report a Problem option in the in-app help menu,
which automatically attaches diagnostic information about your browser
and recent actions to help support investigate faster. Screenshots or
screen recordings can be attached directly to the report.

Feature Requests
Feature requests can be submitted through the in-app feedback form or
posted on forum.novasaas.com where other users can upvote them. The
product team reviews the most upvoted requests each quarter, though
submitting a request does not guarantee it will be built."""
    },
]