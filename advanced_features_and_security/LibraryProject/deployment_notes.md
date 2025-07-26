# Deployment Notes: Enforcing HTTPS and Secure Headers in Django

## Overview
To ensure secure communication between users and the Django web application, HTTPS has been enforced and additional security settings have been implemented. This document outlines the steps taken in Django and the deployment server to secure the application.

---

## 1. Django Settings Configuration

The following security-related settings were added to `settings.py`:

### 🔐 HTTPS Enforcement

```python
SECURE_SSL_REDIRECT = True
