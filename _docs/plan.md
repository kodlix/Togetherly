# Shared Household Chores SaaS — MVP Specification

## 1. Product scope

A multi-household SaaS application for managing shared household chores.

A user can belong to multiple households. Each household has isolated members, roles, chores, categories, and history.

The MVP focuses on simple, explicit chore management rather than automation or notifications.

## 2. Roles

Each household has exactly one Owner and at most one Admin.

### Owner
- Manage household membership
- Assign, replace, or remove the Admin
- Transfer ownership
- Archive the household
- View household data
- Does **not** inherit Admin chore-management permissions

### Admin
- Create chores
- Assign chores
- Edit chores
- Soft-delete chores
- Create/manage categories
- Remove members

### Member
- View all household chores
- Update the status of chores assigned to them
- Leave the household

## 3. Household lifecycle

- Users can create multiple households and belong to multiple households.
- Members can join through an invitation link or join code.
- A member may leave voluntarily.
- An Admin may remove another member.
- When a member leaves/is removed, their Pending/In Progress chores become unassigned; completed chores remain in history.
- The Owner cannot leave unless an Admin exists.
- If the Owner leaves, the Admin automatically becomes Owner.
- The Owner can archive the household; archived households are permanently inactive but retained for historical purposes.

## 4. Chores

MVP fields:
- Title — required
- Description — optional
- Assignee — exactly one household member
- Due date — required
- Due time — required
- Priority — Low, Medium, High, Urgent
- Category — optional, zero or one
- Status — Pending, In Progress, Completed
- Created by / created at / updated at
- Completed by / completed at
- Soft-deleted timestamp/flag

### Status lifecycle
`Pending → In Progress → Completed`

The assigned member changes the status. Completion records who completed it and when. The Admin can edit the chore and reopen a completed chore.

### Assignment
Only the Admin can assign chores. A chore can have exactly one assignee, who must belong to the household.

### Visibility
All household members can see all chores.

### Deletion
Only the Admin can delete chores. Deletion is soft deletion: the chore disappears from normal active views, remains in retained records, is excluded from normal completed history, and cannot be restored through the application.

## 5. Reusing chores

Reuse means **duplicate an existing/completed chore into a new chore**.

The duplicate gets a new identity, starts as Pending, and can receive a new assignee and due date. Useful fields such as title, description, priority, and category can be copied.

Reason: each execution needs its own history and completion record.

## 6. Categories

Admins can create custom categories. A chore may have zero or one category.

Reason: categorization improves organization without forcing unnecessary data entry.

## 7. Dashboard

The dashboard shows:
- Active chores
- Completed chore history
- Simple statistics such as completed chores per member

Deleted chores are excluded from normal history.

Reason: this gives useful accountability without introducing complex analytics.

## 8. Chore browsing

Primary view: list.

Supported filters:
- Status
- Assignee
- Priority

Supported sorting:
- Due date
- Priority
- Assignee

## 9. Notifications

No notifications in the MVP.

Reason: notifications add infrastructure and product complexity without being necessary for the core workflow.

## 10. Explicit MVP exclusions

- Automatic assignment
- Recurring chores
- Notifications
- Multiple assignees
- Calendar view
- Chore restoration
- Custom statuses
- Complex analytics
- Attachments
- Comments/chat
- Gamification
- Payments/subscriptions
- Household automation

## 11. Recommended technical requirements

- Enforce multi-tenant isolation by household on every household-owned record.
- Enforce role-based authorization server-side.
- Validate that an assignee belongs to the target household.
- Exclude soft-deleted chores from normal queries by default.
- Audit important membership and role changes.
- Use database constraints where practical for one Owner and at most one Admin per household.

## 12. Permission matrix

| Action | Owner | Admin | Member |
|---|---:|---:|---:|
| View all chores | Yes | Yes | Yes |
| Create chore | No | Yes | No |
| Assign chore | No | Yes | No |
| Edit chore | No | Yes | No |
| Delete chore | No | Yes | No |
| Update assigned chore status | No | No* | Yes |
| Create category | No | Yes | No |
| Manage Admin role | Yes | No | No |
| Transfer ownership | Yes | No | No |
| Archive household | Yes | No | No |
| Remove another member | No | Yes | No |
| Leave household | Yes** | Yes | Yes |

\* Admin can manage the chore itself, including reopening/editing it, but the normal status transition is performed by the assignee.

\*\* Owner may leave only when an Admin exists.

## 13. Design principles

1. Simple role boundaries: Owner manages the household, Admin manages chores, Members perform chores.
2. Every execution is a separate chore record.
3. Household-wide visibility keeps responsibilities transparent.
4. Assignment is explicit rather than automatic.
5. Soft deletion protects retained records.
6. Keep the MVP small enough to validate the core workflow before adding automation.
