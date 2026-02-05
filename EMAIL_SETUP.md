# Email Setup Guide

This guide covers complete self-hosted email setup with Postfix + OpenDKIM for Django projects. Includes:
- **Transactional emails** from `noreply@mail.yourdomain.com` (DKIM-signed)
- **Email forwarding** from `hello@yourdomain.com`, `contact@`, etc. to your personal inbox

## Quick Overview

| Email Type | Address | Purpose |
|------------|---------|---------|
| Outgoing (noreply) | `noreply@mail.yourdomain.com` | Transactional emails (signup, password reset) |
| Forwarding | `hello@yourdomain.com` | Receives mail, forwards to personal inbox |
| Forwarding | `contact@yourdomain.com` | Receives mail, forwards to personal inbox |
| Forwarding | `support@yourdomain.com` | Receives mail, forwards to personal inbox |

## Prerequisites

- Ubuntu server (20.04+)
- Domain with DNS control
- Server IP address
- Personal email for forwarding (e.g., `john@nader.mx`)

---

## Development Setup

For local development, use Django's console backend:

```python
# config.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

---

## Production Setup

### Step 1: Run the Ansible Playbook

The easiest way to set up email is using the provided Ansible playbook.

**Edit the playbook variables** in `ansible/setup_email.yml`:

```yaml
vars:
  mail_domain: "mail.yourdomain.com"      # Sending domain
  base_domain: "yourdomain.com"           # Main domain
  forward_email: "your@personal.email"    # Where to forward hello@, contact@, etc.
```

**Run the playbook:**

```bash
cd ansible
ansible-playbook -i servers setup_email.yml
```

The playbook will:
1. Install Postfix and OpenDKIM
2. Configure DKIM signing for `mail.yourdomain.com`
3. Set up virtual aliases for email forwarding
4. Output the DNS records you need to add

### Step 2: Add DNS Records

After running the playbook, add these DNS records:

#### A Record (mail subdomain)
```
Type: A
Name: mail
Value: YOUR_SERVER_IP
TTL: 3600
```

#### MX Record (for receiving mail)
```
Type: MX
Name: @
Priority: 10
Value: mail.yourdomain.com
TTL: 3600
```

#### SPF Record (authorize server to send)
```
Type: TXT
Name: @
Value: v=spf1 ip4:YOUR_SERVER_IP a mx ~all
TTL: 3600
```

#### DMARC Record (email policy)
```
Type: TXT
Name: _dmarc
Value: v=DMARC1; p=quarantine; rua=mailto:your@personal.email
TTL: 3600
```

#### DKIM Record (signature verification)

Get the DKIM public key from the playbook output, or run:
```bash
sudo cat /etc/opendkim/keys/mail.yourdomain.com/mail.txt
```

```
Type: TXT
Name: mail._domainkey.mail
Value: v=DKIM1; h=sha256; k=rsa; p=YOUR_LONG_PUBLIC_KEY...
TTL: 3600
```

### Step 3: Update Django Configuration

Update `config.py` on your production server:

```python
# Email Configuration (SMTP via local Postfix)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_USE_TLS = False   # TLS handled by Postfix
EMAIL_USE_SSL = False
EMAIL_HOST_USER = ''    # Leave empty for local Postfix
EMAIL_HOST_PASSWORD = ''

# IMPORTANT: Use mail. subdomain for DKIM signing
DEFAULT_FROM_EMAIL = 'YourProject <noreply@mail.yourdomain.com>'
SERVER_EMAIL = 'noreply@mail.yourdomain.com'
```

### Step 4: Test Email Sending

```python
# Django shell
python manage.py shell

>>> from django.core.mail import send_mail
>>> import config
>>> send_mail(
...     'Test Email Subject',
...     'This is a test email from Django.',
...     config.DEFAULT_FROM_EMAIL,
...     ['your@personal.email'],
... )
1
```

Check the mail logs for DKIM signing:
```bash
sudo tail -20 /var/log/mail.log
# Look for: "DKIM-Signature field added"
```

---

## Ansible Playbook

Create `ansible/setup_email.yml`:

```yaml
---
# Email System Setup - Postfix + OpenDKIM with Forwarding
# Run: ansible-playbook -i servers setup_email.yml

- hosts: all
  become: yes
  vars:
    mail_domain: "mail.yourdomain.com"
    base_domain: "yourdomain.com"
    forward_email: "john@nader.mx"

  tasks:
    - name: Install Postfix and OpenDKIM
      apt:
        name:
          - postfix
          - opendkim
          - opendkim-tools
          - mailutils
        state: present
        update_cache: yes

    - name: Configure Postfix main.cf
      copy:
        dest: /etc/postfix/main.cf
        content: |
          # Basic Settings
          smtpd_banner = $myhostname ESMTP $mail_name
          biff = no
          append_dot_mydomain = no
          readme_directory = no
          compatibility_level = 2

          # TLS parameters
          smtpd_tls_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem
          smtpd_tls_key_file=/etc/ssl/private/ssl-cert-snakeoil.key
          smtpd_tls_security_level=may
          smtp_tls_CApath=/etc/ssl/certs
          smtp_tls_security_level=may
          smtp_tls_session_cache_database = btree:${data_directory}/smtp_scache

          # Network settings
          myhostname = {{ mail_domain }}
          mydomain = {{ base_domain }}
          myorigin = {{ mail_domain }}
          mydestination = localhost, {{ base_domain }}, {{ mail_domain }}
          relayhost =
          mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128
          mailbox_size_limit = 0
          recipient_delimiter = +
          inet_interfaces = all
          inet_protocols = all

          # Virtual aliases for forwarding
          virtual_alias_domains = {{ base_domain }}
          virtual_alias_maps = hash:/etc/postfix/virtual

          # OpenDKIM milter
          milter_protocol = 6
          milter_default_action = accept
          smtpd_milters = inet:localhost:8891
          non_smtpd_milters = inet:localhost:8891
        mode: '0644'
      notify: Restart Postfix

    - name: Configure virtual aliases for forwarding
      copy:
        dest: /etc/postfix/virtual
        content: |
          # Forwarding addresses for {{ base_domain }}
          hello@{{ base_domain }} {{ forward_email }}
          contact@{{ base_domain }} {{ forward_email }}
          support@{{ base_domain }} {{ forward_email }}
          info@{{ base_domain }} {{ forward_email }}
        mode: '0644'
      notify: Rebuild virtual aliases

    - name: Create OpenDKIM directories
      file:
        path: "{{ item }}"
        state: directory
        owner: opendkim
        group: opendkim
        mode: '0750'
      loop:
        - /etc/opendkim
        - /etc/opendkim/keys
        - /etc/opendkim/keys/{{ mail_domain }}

    - name: Configure OpenDKIM
      copy:
        dest: /etc/opendkim.conf
        content: |
          Syslog                  yes
          SyslogSuccess           yes
          LogWhy                  yes
          Canonicalization        relaxed/simple
          Mode                    sv
          SubDomains              no
          OversignHeaders         From

          AutoRestart             yes
          AutoRestartRate         10/1M
          Background              yes
          DNSTimeout              5
          SignatureAlgorithm      rsa-sha256

          UserID                  opendkim
          UMask                   007

          Socket                  inet:8891@localhost
          PidFile                 /run/opendkim/opendkim.pid

          KeyTable                /etc/opendkim/KeyTable
          SigningTable            refile:/etc/opendkim/SigningTable
          ExternalIgnoreList      /etc/opendkim/TrustedHosts
          InternalHosts           /etc/opendkim/TrustedHosts
        mode: '0644'
      notify: Restart OpenDKIM

    - name: Generate DKIM keys
      command: opendkim-genkey -b 2048 -d {{ mail_domain }} -D /etc/opendkim/keys/{{ mail_domain }} -s mail -v
      args:
        creates: /etc/opendkim/keys/{{ mail_domain }}/mail.private

    - name: Set DKIM key permissions
      file:
        path: /etc/opendkim/keys/{{ mail_domain }}/mail.private
        owner: opendkim
        group: opendkim
        mode: '0600'

    - name: Configure OpenDKIM KeyTable
      copy:
        dest: /etc/opendkim/KeyTable
        content: |
          mail._domainkey.{{ mail_domain }} {{ mail_domain }}:mail:/etc/opendkim/keys/{{ mail_domain }}/mail.private
        mode: '0644'
      notify: Restart OpenDKIM

    - name: Configure OpenDKIM SigningTable
      copy:
        dest: /etc/opendkim/SigningTable
        content: |
          *@{{ mail_domain }} mail._domainkey.{{ mail_domain }}
        mode: '0644'
      notify: Restart OpenDKIM

    - name: Configure OpenDKIM TrustedHosts
      copy:
        dest: /etc/opendkim/TrustedHosts
        content: |
          127.0.0.1
          localhost
          {{ mail_domain }}
          {{ base_domain }}
        mode: '0644'
      notify: Restart OpenDKIM

    - name: Enable and start services
      systemd:
        name: "{{ item }}"
        enabled: yes
        state: started
      loop:
        - postfix
        - opendkim

    - name: Get DKIM public key
      command: cat /etc/opendkim/keys/{{ mail_domain }}/mail.txt
      register: dkim_key
      changed_when: false

    - name: Display DNS records needed
      debug:
        msg: |
          ============================================
          DNS RECORDS REQUIRED FOR EMAIL
          ============================================

          Add these records to your DNS:

          1. A RECORD:
             Name: mail
             Value: YOUR_SERVER_IP

          2. MX RECORD:
             Name: @
             Priority: 10
             Value: mail.{{ base_domain }}

          3. SPF RECORD (TXT):
             Name: @
             Value: "v=spf1 ip4:YOUR_SERVER_IP a mx ~all"

          4. DMARC RECORD (TXT):
             Name: _dmarc
             Value: "v=DMARC1; p=quarantine; rua=mailto:{{ forward_email }}"

          5. DKIM RECORD (TXT):
             Name: mail._domainkey.mail
             {{ dkim_key.stdout }}

          ============================================

  handlers:
    - name: Restart Postfix
      systemd:
        name: postfix
        state: restarted

    - name: Restart OpenDKIM
      systemd:
        name: opendkim
        state: restarted

    - name: Rebuild virtual aliases
      command: postmap /etc/postfix/virtual
      notify: Restart Postfix
```

---

## Testing Checklist

### 1. Verify DNS Records
```bash
# Check each record (may take up to 48 hours to propagate)
dig A mail.yourdomain.com +short
dig MX yourdomain.com +short
dig TXT yourdomain.com +short           # SPF
dig TXT _dmarc.yourdomain.com +short    # DMARC
dig TXT mail._domainkey.mail.yourdomain.com +short  # DKIM
```

### 2. Test DKIM Key
```bash
sudo opendkim-testkey -d mail.yourdomain.com -s mail -vvv
```

### 3. Test Email Sending (Transactional)
```python
# Django shell
from django.core.mail import send_mail
import config

# Send from noreply@mail.yourdomain.com
send_mail(
    'Test Transactional Email',
    'This email should be DKIM-signed.',
    config.DEFAULT_FROM_EMAIL,
    ['your@personal.email'],
)
```

Check logs:
```bash
sudo tail -30 /var/log/mail.log
# Look for: "DKIM-Signature field added"
# Look for: "status=sent"
```

### 4. Test Email Forwarding
Send an email to `hello@yourdomain.com` from an external account (Gmail, etc.).
It should arrive in your forwarding inbox (e.g., `john@nader.mx`).

### 5. Test Deliverability Score
1. Visit https://www.mail-tester.com/
2. Send a test email to the provided address
3. Aim for 8+/10 score

---

## Django Email Templates

Create email templates in `templates/email/`:

### Base Template (`templates/email/base.html`)
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% endblock %}</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; padding: 20px 0; border-bottom: 1px solid #eee; }
        .content { padding: 30px 0; }
        .footer { text-align: center; padding: 20px 0; border-top: 1px solid #eee; font-size: 12px; color: #888; }
        .btn { display: inline-block; padding: 12px 24px; background: #333; color: #fff; text-decoration: none; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ project_name }}</h1>
        </div>
        <div class="content">
            {% block content %}{% endblock %}
        </div>
        <div class="footer">
            <p>&copy; {{ year }} {{ project_name }}. All rights reserved.</p>
            <p>This email was sent to {{ recipient_email }}</p>
        </div>
    </div>
</body>
</html>
```

### Verification Email (`templates/email/verification.html`)
```html
{% extends "email/base.html" %}
{% block title %}Verify Your Email{% endblock %}
{% block content %}
<h2>Welcome, {{ user.first_name }}!</h2>
<p>Please verify your email address by clicking the button below:</p>
<p style="text-align: center; margin: 30px 0;">
    <a href="{{ verification_url }}" class="btn">Verify Email</a>
</p>
<p>Or copy this link: {{ verification_url }}</p>
<p>This link expires in 24 hours.</p>
{% endblock %}
```

### Password Reset (`templates/email/password-reset.html`)
```html
{% extends "email/base.html" %}
{% block title %}Reset Your Password{% endblock %}
{% block content %}
<h2>Password Reset Request</h2>
<p>We received a request to reset your password. Click the button below:</p>
<p style="text-align: center; margin: 30px 0;">
    <a href="{{ reset_url }}" class="btn">Reset Password</a>
</p>
<p>If you didn't request this, you can safely ignore this email.</p>
<p>This link expires in 1 hour.</p>
{% endblock %}
```

---

## Email Utility Function

In `app/utils.py`:

```python
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import config


def send_email(recipients, subject, template, data=None, sender=None):
    """
    Send HTML email using Django templates.

    Args:
        recipients: List of email addresses
        subject: Email subject
        template: Template name (without .html extension)
        data: Context data for template
        sender: Optional sender (defaults to DEFAULT_FROM_EMAIL)

    Returns:
        Number of emails sent successfully
    """
    if data is None:
        data = {}

    # Add common context
    data.update({
        'project_name': config.PROJECT_NAME,
        'year': datetime.now().year,
        'recipient_email': recipients[0] if recipients else '',
    })

    # Render template
    html_content = render_to_string(f'email/{template}.html', data)
    text_content = strip_tags(html_content)

    # Send email
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=sender or config.DEFAULT_FROM_EMAIL,
        to=recipients,
    )
    msg.attach_alternative(html_content, "text/html")

    return msg.send()
```

Usage:
```python
from app.utils import send_email

send_email(
    recipients=['user@example.com'],
    subject='Welcome to Our App!',
    template='verification',
    data={
        'user': user,
        'verification_url': 'https://yourdomain.com/verify?token=xxx',
    }
)
```

---

## Troubleshooting

### Email Not Sending
```bash
# Check Postfix status
sudo systemctl status postfix

# Check mail queue
mailq

# Force delivery
sudo postqueue -f

# Check logs
sudo tail -f /var/log/mail.log
```

### Email Goes to Spam
1. Verify DKIM is signing: Check for "DKIM-Signature field added" in logs
2. Test SPF: `dig TXT yourdomain.com +short`
3. Test with mail-tester.com
4. Ensure you're sending from `@mail.yourdomain.com` (not `@yourdomain.com`)

### DKIM Not Signing
```bash
# Check OpenDKIM is running
sudo systemctl status opendkim

# Test DKIM key
sudo opendkim-testkey -d mail.yourdomain.com -s mail -vvv

# Check permissions
ls -la /etc/opendkim/keys/mail.yourdomain.com/
```

### Email Forwarding Not Working
```bash
# Check virtual aliases
cat /etc/postfix/virtual

# Rebuild after changes
sudo postmap /etc/postfix/virtual
sudo systemctl restart postfix

# Check logs for incoming mail
sudo grep "hello@" /var/log/mail.log
```

---

## Security Considerations

1. **Never send from the root domain** - Always use `noreply@mail.yourdomain.com`
2. **Keep DKIM keys secure** - Permissions should be `600` for private key
3. **Monitor email logs** - Watch for abuse or delivery issues
4. **Use DMARC** - Start with `p=none` for monitoring, then move to `p=quarantine`
5. **Rate limiting** - Consider implementing email rate limiting in your app

---

## Quick Reference

| Task | Command |
|------|---------|
| Check mail queue | `mailq` |
| Force deliver queue | `sudo postqueue -f` |
| View mail logs | `sudo tail -f /var/log/mail.log` |
| Test DKIM | `sudo opendkim-testkey -d mail.yourdomain.com -s mail -vvv` |
| Restart services | `sudo systemctl restart postfix opendkim` |
| Check DNS records | `dig TXT yourdomain.com +short` |
