# Talend Job: Plan_Success_Alert

## Purpose

Send email when entire plan completes successfully

- **Project**: LATITUDE
- **Version**: 0.1
- **Job Type**: Standard

- **Author**: jmach@harriscollect.com
- **Created**: 2025-10-16T09:02:46.821-0700
- **Last Modified**: 2025-10-16T09:31:04.919-0700

## Components

| # | Component | Type | Key Parameters |
|---|-----------|------|----------------|
| 1 | tSendMail_1 | `tSendMail` | `TO`=context.emailRecipients, `FROM`="svc_analytics@harriscollect.com", `NEED_PERSONAL_NAME`=false, `PERSONAL_NAME`="sender", `SUBJECT`="Latitude load to Snowflake complete" |
