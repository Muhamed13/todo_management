# Todo Management

A custom Odoo 17 module for task management, timesheet tracking, PDF reporting, and REST API integration.

## Overview

Todo Management is an Odoo 17 module that helps organizations manage tasks, assign users, track working hours, generate PDF reports, and expose task operations through REST API endpoints.

## Features

* Task Management

  * Create, update, archive, and manage tasks.

* Task Assignment Wizard

  * Assign one or multiple tasks to a selected user.

* Timesheet Tracking

  * Log working hours for each task.

* Automatic Total Hours Calculation

  * Calculates total logged hours from related timesheets.

* Task Workflow

  * New → In Progress → Completed → Closed.

* Chatter Integration

  * Track changes and activities using Odoo Chatter.

* PDF Reports

  * Generate printable task reports with timesheet details.

* REST API

  * Create, retrieve, update, and delete tasks through API endpoints.

* Security & Access Control

  * User and Manager roles with record rules and access rights.

* Scheduled Actions

  * Automatically identify overdue tasks.

## Module Structure

```text
todo_management/
│
├── controllers/
│   ├── __init__.py
│   └── todo_task_api.py
│
├── data/
│   └── sequence.xml
│
├── i18n/
│   ├── ar_001.po
│   └── todo_management.pot
│
├── models/
│   ├── __init__.py
│   ├── todo_task.py
│   └── time_sheet.py
│
├── reports/
│   └── todo_task_report.xml
│
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
│
├── views/
│   ├── base_menu.xml
│   ├── time_sheet_view.xml
│   └── todo_task_view.xml
│
├── wizard/
│   ├── __init__.py
│   ├── assignment_wizard.py
│   └── assignment_wizard_view.xml
│
├── __init__.py
├── __manifest__.py
└── README.md
```

## Business Flow

The following diagram illustrates the task lifecycle inside the system:

```text id="2a9xnr"
Create Task
      │
      ▼
Assign User
      │
      ▼
Track Timesheets
      │
      ▼
Calculate Total Hours
      │
      ▼
Update Task Status
      │
      ▼
Generate PDF Report
```

### Task Workflow

Each task follows a predefined workflow:

```text id="6sjq8y"
New
 │
 ▼
In Progress
 │
 ▼
Completed
 │
 ▼
Closed
```

### Timesheet Flow

```text id="7blg8z"
Task
 │
 ▼
Add Timesheet Entries
 │
 ▼
Calculate Total Hours
 │
 ▼
Validate Against Estimated Time
```

## Security & Access Control

The module implements role-based access control using Odoo Security Groups, Access Rights, and Record Rules.

### Users Group

Users have limited access to the system:

* Can view assigned tasks only.
* Can update their assigned tasks.
* Cannot create tasks.
* Cannot delete tasks.

### Managers Group

Managers have full access to the system:

* Create tasks.
* View all tasks.
* Update tasks.
* Delete tasks.
* Assign tasks to users.

### Record Rules

A record rule is applied to restrict users to their own assigned tasks:

```python
[('assigned_to', '=', user.id)]
```

This ensures that users can only access tasks assigned to them.

### Access Rights

| Model             | Users       | Managers                    |
| ----------------- | ----------- | --------------------------- |
| Todo Task         | Read, Write | Read, Write, Create, Delete |
| Time Sheet        | Full Access | Full Access                 |
| Assignment Wizard | Full Access | Full Access                 |

```
```

## REST API

The module exposes REST API endpoints for managing tasks.

### Base URL

```text
/api/v1/tasks
```

### Create Task

**Request**

```http
POST /api/v1/tasks
```

**Request Body**

```json
{
    "name": "Prepare Project Documentation",
    "description": "Write project documentation",
    "assigned_to": 2,
    "due_date": "2026-06-30",
    "estimated_time": 8
}
```

**Response**

```json
{
    "success": true,
    "message": "Task created successfully"
}
```

---

### Get All Tasks

**Request**

```http
GET /api/v1/tasks
```

Returns all available tasks.

---

### Get Task By ID

**Request**

```http
GET /api/v1/tasks/<task_id>
```

Example:

```http
GET /api/v1/tasks/1
```

Returns a single task.

---

### Update Task

**Request**

```http
PUT /api/v1/tasks/<task_id>
```

Example:

```json
{
    "name": "Updated Task",
    "estimated_time": 10
}
```

Supports partial updates.

---

### Delete Task

**Request**

```http
DELETE /api/v1/tasks/<task_id>
```

Deletes a task if it has no related timesheet records.

---

### Validation Rules

The API validates:

* Task name is required.
* Estimated time is required.
* Estimated time must be greater than zero.
* Tasks with timesheet entries cannot be deleted.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/todo_management.git
```

### 2. Copy the Module

Copy the module into your Odoo custom addons directory.

```text
custom_addons/
└── todo_management
```

### 3. Update Apps List

From Odoo:

```text
Apps → Update Apps List
```

### 4. Install the Module

Search for:

```text
Todo Management
```

Then click:

```text
Install
```

### Requirements

* Odoo 17
* Python 3.10+
* PostgreSQL
* mail module