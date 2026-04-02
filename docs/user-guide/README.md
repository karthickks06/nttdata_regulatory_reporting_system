# User Guide

## Getting Started

Welcome to the NTT Data Regulatory Reporting System. This guide will help you get started with the platform.

## Logging In

1. Navigate to the application URL
2. Enter your email and password
3. Click "Login"

Default admin credentials:
- Email: `admin@example.com`
- Password: `admin123`

**Important**: Change your password after first login.

## Dashboard Overview

After logging in, you'll see the main dashboard with:

- **Regulatory Updates**: Recent regulatory documents
- **Active Workflows**: Ongoing processes
- **Reports**: Generated reports
- **Notifications**: System alerts

## User Roles

The system has six predefined roles:

1. **Admin**: Full system access
2. **Business Analyst**: Requirements and gap analysis
3. **Developer**: Code generation and data pipelines
4. **Analyst**: Report generation and validation
5. **Approver**: Workflow approvals
6. **Viewer**: Read-only access

## Features by Role

### Business Analyst

#### Uploading Regulatory Documents

1. Navigate to "Regulatory Updates"
2. Click "Upload Document"
3. Select file (PDF, Word, Excel)
4. Fill in metadata:
   - Title
   - Source (FCA, PRA, BOE)
   - Reference Number
   - Effective Date
5. Click "Upload"

The system will automatically:
- Parse the document
- Extract requirements
- Build knowledge graph
- Notify relevant stakeholders

#### Managing Requirements

1. Navigate to "Requirements"
2. View extracted requirements
3. Click on a requirement to:
   - Edit details
   - Perform gap analysis
   - Create data mappings
   - Set priority
   - Request approval

#### Gap Analysis

1. Select a requirement
2. Click "Gap Analysis"
3. Review identified gaps:
   - Missing data fields
   - System limitations
   - Process gaps
4. Document remediation plans
5. Assign to appropriate team

### Developer

#### Viewing Generated Code

1. Navigate to "Development"
2. Select "Generated Code"
3. View SQL and Python code
4. Click "Edit" to modify
5. Click "Validate" to check syntax

#### Data Lineage

1. Navigate to "Development" > "Lineage"
2. Select entity type and ID
3. View lineage diagram showing:
   - Data sources
   - Transformations
   - Target systems
   - Dependencies

#### Pipeline Monitoring

1. Navigate to "Development" > "Pipelines"
2. View active pipelines
3. Monitor progress
4. Check for errors
5. View execution history

### Analyst

#### Generating Reports

1. Navigate to "Reports"
2. Click "Generate Report"
3. Select report type
4. Choose period (start/end dates)
5. Configure parameters
6. Click "Generate"

#### Validating Reports

1. Select a generated report
2. Click "Validate"
3. Review validation results:
   - Data quality checks
   - Business rule validation
   - Anomaly detection
4. Address any issues
5. Revalidate if needed

#### Submitting Reports

1. Validate report first
2. Click "Submit"
3. Review submission checklist
4. Add comments if needed
5. Click "Confirm Submission"

### Approver

#### Approval Queue

1. Navigate to "Workflows" > "Approvals"
2. View pending approvals
3. Click on item to review
4. Check details and validation
5. Approve or Reject with comments

## Workflows

### Understanding Workflow Stages

All regulatory updates go through:

1. **Document Upload**: BA uploads regulatory document
2. **Requirement Extraction**: Interpreter Agent extracts requirements
3. **BA Review**: BA Supervisor reviews and approves
4. **Code Generation**: Architect Agent generates code
5. **Dev Review**: Dev Supervisor reviews and approves
6. **Validation**: Auditor Agent validates outputs
7. **QA Review**: QA Supervisor reviews and approves
8. **Completion**: Compliance Agent marks complete

### Tracking Workflow Progress

1. Navigate to "Workflows"
2. Select a workflow
3. View:
   - Current stage
   - Progress percentage
   - Agent activities
   - Approval history
   - Timeline

## Agent Monitoring

### Viewing Agent Activity

1. Navigate to "Agents"
2. Select agent type:
   - Compliance Agent (Level 0)
   - Supervisors (Level 1)
   - Workers (Level 2)
3. View:
   - Current tasks
   - Execution logs
   - Performance metrics
   - Error reports

## Notifications

### Email Notifications

You'll receive emails for:
- New regulatory updates
- Approval requests
- Workflow completions
- Report validations
- System errors (admins only)

### In-App Notifications

Check the notification bell icon for:
- Real-time updates
- Task assignments
- Workflow changes
- System announcements

## Search and Filtering

### Global Search

Use the search bar at the top to find:
- Documents
- Requirements
- Reports
- Workflows

### Advanced Filtering

Most list views support filtering:
- Date ranges
- Status
- Source
- Assigned user
- Priority

## Best Practices

### Document Uploads

- Use clear, descriptive titles
- Include all relevant metadata
- Upload complete documents
- Verify effective dates

### Requirements Management

- Review extracted requirements carefully
- Add business context
- Set appropriate priorities
- Link related requirements

### Code Review

- Always validate generated code
- Test in non-production first
- Document any modifications
- Keep lineage updated

### Report Generation

- Validate before submission
- Address all anomalies
- Include explanatory notes
- Archive supporting documents

## Troubleshooting

### Login Issues

- Check email/password
- Clear browser cache
- Contact admin if locked out

### Upload Failures

- Check file size limit (50MB)
- Verify file format
- Ensure stable connection

### Validation Errors

- Review error messages
- Check data completeness
- Verify business rules
- Contact support if needed

## Getting Help

- In-app help: Click "?" icon
- Documentation: `/docs` folder
- Admin support: admin@example.com
- Technical support: support@example.com

## Keyboard Shortcuts

- `Ctrl + K`: Global search
- `Ctrl + N`: New item (context-dependent)
- `Ctrl + S`: Save
- `Esc`: Close dialog

## Mobile Access

The system is responsive and works on:
- Tablets (recommended)
- Mobile phones (limited features)
- Desktop browsers (full features)

## Security

- Always logout when done
- Don't share credentials
- Use strong passwords
- Report suspicious activity
- Enable 2FA (if available)

## Updates and Maintenance

- System updates: Weekly (Sundays 2-4 AM)
- Planned maintenance: Announced 48 hours in advance
- Emergency maintenance: As needed with notification
