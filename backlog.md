# MVP Implementation Backlog

Tasks are ordered by dependency. Each task is one small, reviewable change.

## 1. Register the chores Django app

**Description**
Register the existing `chores` app and add its stable project URL include.

**Acceptance criteria**
- Django loads the app without errors.
- The app has a reachable URL entry point.
- `manage.py check` passes.

**Dependencies**
- None.

## 2. Configure authentication test helpers

**Description**
Add test helpers for creating users and making authenticated requests.

**Acceptance criteria**
- Tests can create users with unique credentials.
- Tests can authenticate and unauthenticate a client.
- At least one authentication test uses the helper.

**Dependencies**
- Task 1.

## 3. Create the Household model

**Description**
Add household name, archived state, and creation/update timestamps.

**Acceptance criteria**
- Households can be created and persisted.
- Archived households remain stored and identifiable as inactive.
- The migration applies cleanly.

**Dependencies**
- Task 1.

## 4. Create Membership and role values

**Description**
Add the user-to-household membership model with Owner, Admin, and Member roles.

**Acceptance criteria**
- A user can belong to multiple households.
- A user-household pair cannot be duplicated.
- Only the three specified role values are accepted.
- Membership tests pass.

**Dependencies**
- Tasks 2 and 3.

## 5. Enforce household role constraints

**Description**
Enforce one Owner and at most one Admin per active household.

**Acceptance criteria**
- Two active Owners cannot be saved.
- Two active Admins cannot be saved.
- Constraint violations produce validation or request errors.
- Constraint tests pass on the supported database.

**Dependencies**
- Task 4.

## 6. Add household creation and listing

**Description**
Implement authenticated views for creating households and listing the current user's households.

**Acceptance criteria**
- An authenticated user can create multiple households.
- Each creator receives an Owner membership.
- Users see only households where they are members.
- Anonymous requests are rejected.

**Dependencies**
- Tasks 2 and 4.

## 7. Add invitation-link or join-code entry

**Description**
Implement the specified invitation-link or join-code flow for active households.

**Acceptance criteria**
- A valid code or link adds an authenticated user as a Member.
- Rejoining does not duplicate membership.
- Invalid and archived-household attempts are rejected.
- Join-flow tests pass.

**Dependencies**
- Tasks 4 and 6.

## 8. Add household authorization helpers

**Description**
Create reusable server-side membership, Owner, Admin, Member, and household-scoped lookup checks.

**Acceptance criteria**
- Anonymous users are rejected from protected actions.
- Non-members cannot access a household by URL or object ID.
- Owner-only and Admin-only checks are reusable.
- Role-boundary tests pass.

**Dependencies**
- Tasks 4 and 6.

## 9. Create the Category model

**Description**
Add a household-scoped category with a name unique within that household.

**Acceptance criteria**
- A category belongs to exactly one household.
- Duplicate names are rejected within one household.
- The same name is allowed in different households.
- Model and migration tests pass.

**Dependencies**
- Task 3.

## 10. Create the Chore model

**Description**
Add the specified chore fields, relationships, statuses, priorities, timestamps, and completion metadata.

**Acceptance criteria**
- Required title, due date/time, priority, status, creator, and one assignee are represented.
- Description and category are optional.
- Status values are Pending, In Progress, and Completed.
- Priority values are Low, Medium, High, and Urgent.
- The migration applies cleanly.

**Dependencies**
- Tasks 4 and 9.

## 11. Validate chore household relationships

**Description**
Validate that a chore's assignee, creator, and category belong to its household.

**Acceptance criteria**
- Cross-household assignees are rejected.
- Cross-household categories are rejected.
- Invalid relationships fail before persistence.
- Validation tests pass.

**Dependencies**
- Tasks 8 and 10.

## 12. Add chore soft deletion and active queries

**Description**
Add the soft-deleted flag/timestamp and default query behavior for active chores and history.

**Acceptance criteria**
- Deletion retains the chore record.
- Normal active queries exclude deleted chores.
- Deleted chores are excluded from normal completed history.
- No restore operation is exposed.
- Soft-deletion tests pass.

**Dependencies**
- Task 10.

## 13. Add Admin category management

**Description**
Implement Admin-only category create, update, and delete operations.

**Acceptance criteria**
- Admins manage categories only in their household.
- Owners and Members are denied.
- Validation errors are returned clearly.
- Archived households reject category mutations.

**Dependencies**
- Tasks 8 and 9.

## 14. Add Admin chore creation and editing

**Description**
Implement Admin-only chore creation and editing, including assignment.

**Acceptance criteria**
- Admins can create and edit household chores.
- Assignment requires one current household member.
- Owners and Members are denied.
- Archived households reject chore mutations.
- Request tests cover valid and invalid data.

**Dependencies**
- Tasks 8, 10, and 11.

## 15. Add Admin chore deletion and duplication

**Description**
Implement Admin-only soft deletion and reuse-by-duplication.

**Acceptance criteria**
- Delete marks a chore deleted without removing it.
- A duplicate has a new identity and Pending status.
- A duplicate can receive a new assignee and due date.
- Title, description, priority, and category can be copied.
- Owners and Members are denied.

**Dependencies**
- Tasks 12 and 14.

## 16. Implement assigned-member status transitions

**Description**
Implement the assigned member's Pending to In Progress to Completed workflow.

**Acceptance criteria**
- Only the assigned member performs normal status updates.
- Invalid backward or skipped transitions are rejected.
- Completion records the completing user and time.
- Deleted chores cannot be updated.
- Status tests pass.

**Dependencies**
- Tasks 8 and 10.

## 17. Implement Admin reopening

**Description**
Allow an Admin to reopen a completed chore through editing.

**Acceptance criteria**
- An Admin can reopen a completed chore.
- Reopening sets a non-completed status and consistent completion metadata.
- Owners and Members cannot reopen chores.
- Reopening tests pass.

**Dependencies**
- Tasks 14 and 16.

## 18. Add chore filters and sorting

**Description**
Implement the household chore list with the specified filters and sorting.

**Acceptance criteria**
- Members can view all active chores in their household.
- Filters support status, assignee, and priority.
- Sorting supports due date, priority, and assignee.
- Deleted and cross-household chores are excluded.
- Query tests pass.

**Dependencies**
- Tasks 8, 12, and 14.

## 19. Add completed history and statistics

**Description**
Add completed chore history and completed-chores-per-member statistics.

**Acceptance criteria**
- Completed chores appear in household history.
- Deleted chores are excluded from normal history.
- Statistics are scoped to the current household.
- Dashboard tests pass.

**Dependencies**
- Tasks 12, 16, and 18.

## 20. Implement member departure and removal

**Description**
Implement voluntary leave and Admin removal with the specified chore effects.

**Acceptance criteria**
- Members can leave their household.
- Admins can remove another member but not the Owner.
- Pending and In Progress chores become unassigned.
- Completed chores retain completion history.
- Invalid attempts are rejected.

**Dependencies**
- Tasks 5, 8, and 10.

## 21. Implement Admin assignment and ownership transfer

**Description**
Implement Owner-only Admin assignment, replacement, removal, and ownership transfer.

**Acceptance criteria**
- Only the Owner can manage the Admin role.
- At most one Admin remains after each operation.
- Ownership transfer changes roles atomically.
- Admins and Members are denied.
- Role-transition tests pass.

**Dependencies**
- Tasks 5, 8, and 20.

## 22. Implement owner departure and archiving

**Description**
Implement the Owner departure exception and Owner-only household archiving.

**Acceptance criteria**
- The Owner cannot leave without an Admin.
- When the Owner leaves, the Admin becomes Owner.
- Only the Owner can archive the household.
- Archived households retain history but reject joining and mutations.
- Lifecycle tests pass.

**Dependencies**
- Tasks 7, 20, and 21.

## 23. Add end-to-end MVP workflow tests

**Description**
Test the core workflow from household creation through joining, chore completion, duplication, and history viewing.

**Acceptance criteria**
- The workflow passes against a clean test database.
- Expected roles are verified at each step.
- The duplicate has an independent identity and Pending status.

**Dependencies**
- Tasks 7 and 13 through 19.

## 24. Add isolation and permission regression tests

**Description**
Add regression coverage for tenant isolation, permissions, soft deletion, and lifecycle edge cases.

**Acceptance criteria**
- Cross-household reads and mutations fail through IDs and query parameters.
- Permission-matrix actions have allow and deny coverage.
- Transfer, departure/removal, archive, and soft deletion are covered.
- The full Django test suite passes from a clean test database.

**Dependencies**
- Tasks 8, 12, 20, 21, and 22.