# User Guide

Complete guide for using the Workshop Management System.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Creating an Account](#creating-an-account)
3. [Managing Workshops](#managing-workshops)
4. [Joining Workshops](#joining-workshops)
5. [Managing Participants](#managing-participants)
6. [Dashboard](#dashboard)
7. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Accessing the Application

1. Open your web browser
2. Navigate to `http://localhost:3000` (or your deployed URL)
3. You'll see the home page with options to sign in or sign up

### System Requirements

- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection
- JavaScript enabled

---

## Creating an Account

### Sign Up

1. Click **"Sign Up"** button on the home page
2. Fill in the registration form:
   - **Name**: Your full name (2-100 characters)
   - **Email**: Valid email address (must be unique)
   - **Password**: Must contain:
     - At least 8 characters
     - One uppercase letter
     - One lowercase letter
     - One number
     - One special character (!@#$%^&*)
   - **Confirm Password**: Must match password
3. Click **"Sign up"** button
4. You'll be automatically logged in and redirected to your dashboard

### Password Requirements

✅ **Good passwords**:
- `SecurePass123!`
- `MyWorkshop2024@`
- `Python#Learning99`

❌ **Bad passwords**:
- `password` (too simple)
- `12345678` (no letters)
- `Password` (no numbers or special chars)

### Sign In

1. Click **"Sign In"** button
2. Enter your email and password
3. Click **"Sign in"** button
4. You'll be redirected to your dashboard

### Forgot Password

Currently not implemented. Contact system administrator to reset your password.

---

## Managing Workshops

### Creating a Workshop

1. Go to your **Dashboard**
2. Click **"Create Workshop"** button
3. Fill in the workshop details:
   - **Title**: Workshop name (max 200 characters)
   - **Description**: Workshop details (max 1000 characters)
4. Click **"Create Workshop"**
5. Your workshop will appear in "My Workshops" section

**Example**:
```
Title: Introduction to Python Programming
Description: Learn Python basics including variables, loops, functions, and object-oriented programming. Suitable for beginners with no prior programming experience.
```

### Viewing Your Workshops

1. Go to **Dashboard**
2. See "My Workshops" section
3. Each workshop shows:
   - Title and description
   - Status badge (Pending/Ongoing/Completed)
   - Signup status (Open/Closed)
   - Manage and Delete buttons

### Editing a Workshop

1. Go to **Dashboard**
2. Click **"Manage"** on the workshop you want to edit
3. Click **"Edit"** button
4. Update title and/or description
5. Click **"Save"**

### Changing Workshop Status

1. Go to workshop detail page
2. Use the status dropdown to select:
   - **Pending**: Workshop not started yet
   - **Ongoing**: Workshop is currently running
   - **Completed**: Workshop has finished
3. Status updates immediately

### Enabling/Disabling Signup

1. Go to workshop detail page
2. Click **"Open Signup"** or **"Close Signup"** button
3. When signup is closed:
   - New users cannot join
   - Existing participants remain
   - Pending requests can still be processed

### Deleting a Workshop

⚠️ **Warning**: This action cannot be undone!

1. Go to **Dashboard**
2. Click **"Delete"** on the workshop
3. Confirm deletion in the dialog
4. Workshop and all participants will be removed

---

## Joining Workshops

### Browsing Workshops

1. Click **"All Workshops"** in navigation
2. Browse available workshops
3. Each workshop shows:
   - Title and description
   - Workshop status
   - Signup status
   - Your participation status (if applicable)

### Joining a Workshop

1. Find a workshop you want to join
2. Click **"Join"** button
3. Your request will be sent to the workshop owner
4. Status changes to **"Pending"**
5. Wait for owner approval

### Join Request Status

- **Pending** (Yellow): Waiting for owner approval
- **Joined** (Green): You're a participant
- **Rejected** (Red): Request was rejected
- **Waitlisted** (Orange): On waiting list

### Viewing Joined Workshops

1. Go to **Dashboard**
2. See "Joined Workshops" section
3. Shows all workshops you've joined or requested to join

### Leaving a Workshop

1. Go to **Dashboard**
2. Find the workshop in "Joined Workshops"
3. Click **"Leave"** button
4. Confirm in the dialog
5. Your participation will be removed

---

## Managing Participants

### Viewing Join Requests

1. Go to **Dashboard**
2. Click **"Manage"** on your workshop
3. See **"Pending Requests"** section
4. Each request shows:
   - User name and email
   - Request date
   - Approve and Reject buttons

### Approving a Join Request

1. Go to workshop detail page
2. Find the request in "Pending Requests"
3. Click **"Approve"** button
4. User moves to "Participants" section
5. User can now access workshop

### Rejecting a Join Request

1. Go to workshop detail page
2. Find the request in "Pending Requests"
3. Click **"Reject"** button
4. Confirm rejection
5. User moves to "Rejected" section

### Viewing Participants

1. Go to workshop detail page
2. See **"Participants"** section
3. Shows all approved participants with:
   - Name and email
   - Join date
   - Remove button

### Removing a Participant

1. Go to workshop detail page
2. Find participant in "Participants" section
3. Click **"Remove"** button
4. Confirm removal
5. Participant is removed from workshop

### Viewing Rejected/Waitlisted

1. Go to workshop detail page
2. Expand **"Other Requests"** section
3. See rejected and waitlisted users

---

## Dashboard

### Dashboard Overview

Your dashboard is your central hub showing:
- **My Workshops**: Workshops you created
- **Joined Workshops**: Workshops you've joined

### My Workshops Section

Shows workshops you own with:
- Workshop title and description
- Status badge
- Signup status indicator
- Quick actions (Manage, Delete)

### Joined Workshops Section

Shows workshops you've joined with:
- Workshop title and description
- Your participation status
- Workshop status
- Quick actions (View, Leave)

### Navigation

- **Dashboard**: Your personal dashboard
- **All Workshops**: Browse all workshops
- **User Menu**: Shows your name and logout button

---

## Troubleshooting

### Cannot Sign Up

**Problem**: "Email already exists" error

**Solution**: 
- Use a different email address
- If you forgot your password, contact administrator

---

**Problem**: "Password does not meet requirements"

**Solution**:
- Ensure password has at least 8 characters
- Include uppercase, lowercase, number, and special character
- Example: `MyPass123!`

---

### Cannot Sign In

**Problem**: "Invalid credentials" error

**Solution**:
- Check email spelling
- Check password (case-sensitive)
- Ensure Caps Lock is off
- Contact administrator if you forgot password

---

**Problem**: "Session expired" message

**Solution**:
- Your session expired after 30 minutes
- Sign in again to continue

---

### Cannot Join Workshop

**Problem**: "Already joined" error

**Solution**:
- You already have a pending or active request
- Check your "Joined Workshops" in dashboard

---

**Problem**: "Signup closed" button disabled

**Solution**:
- Workshop owner has closed signup
- Contact workshop owner to request access

---

**Problem**: "Owner cannot join" error

**Solution**:
- You cannot join your own workshops
- You're already the owner with full access

---

### Cannot Create Workshop

**Problem**: "Title is required" error

**Solution**:
- Enter a workshop title
- Title cannot be empty or only whitespace

---

**Problem**: "Description is required" error

**Solution**:
- Enter a workshop description
- Description cannot be empty or only whitespace

---

### Cannot Approve/Reject Requests

**Problem**: "Not workshop owner" error

**Solution**:
- Only workshop owners can approve/reject requests
- Ensure you're viewing your own workshop

---

**Problem**: "Participant not found" error

**Solution**:
- Participant may have left the workshop
- Refresh the page to see current participants

---

### General Issues

**Problem**: Page not loading

**Solution**:
- Check internet connection
- Refresh the page (F5 or Cmd+R)
- Clear browser cache
- Try a different browser

---

**Problem**: Changes not saving

**Solution**:
- Check internet connection
- Look for error messages
- Try again after a few seconds
- Contact support if problem persists

---

**Problem**: Logged out unexpectedly

**Solution**:
- Sessions expire after 30 minutes of inactivity
- Sign in again to continue
- Your data is saved

---

## Tips and Best Practices

### For Workshop Owners

1. **Clear Descriptions**: Write detailed workshop descriptions
2. **Timely Responses**: Review join requests promptly
3. **Status Updates**: Keep workshop status current
4. **Close Signup**: Close signup when workshop is full
5. **Communication**: Provide contact information in description

### For Participants

1. **Read Descriptions**: Understand workshop requirements before joining
2. **Be Patient**: Wait for owner approval
3. **Stay Active**: Participate once approved
4. **Leave Properly**: Use "Leave" button if you can't attend

### Security

1. **Strong Passwords**: Use unique, strong passwords
2. **Logout**: Always logout on shared computers
3. **Privacy**: Don't share your password
4. **Updates**: Keep your browser updated

---

## Keyboard Shortcuts

Currently not implemented. Future shortcuts may include:
- `Ctrl/Cmd + K`: Quick search
- `Ctrl/Cmd + N`: New workshop
- `Esc`: Close modals

---

## Mobile Usage

The application is responsive and works on mobile devices:
- All features available on mobile
- Touch-friendly buttons
- Responsive layout
- Works on iOS and Android browsers

---

## Getting Help

### Support Channels

1. **Documentation**: Check this guide and API documentation
2. **FAQ**: See common questions above
3. **Contact**: Email support@example.com
4. **Issues**: Report bugs on GitHub

### Providing Feedback

We welcome your feedback:
- Feature requests
- Bug reports
- Usability suggestions
- General comments

---

## Glossary

- **Workshop**: An event or course that users can join
- **Owner**: User who created the workshop
- **Participant**: User who has joined a workshop
- **Join Request**: Request to join a workshop
- **Pending**: Waiting for approval
- **Approved/Joined**: Request accepted
- **Rejected**: Request denied
- **Waitlisted**: On waiting list
- **Signup**: Process of joining a workshop
- **Dashboard**: Personal overview page

---

**Need more help?** Contact support or check the [API Documentation](API_DOCUMENTATION.md) for technical details.
