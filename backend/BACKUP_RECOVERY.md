# Backup and Recovery Procedures

## Overview

This document outlines the backup and recovery procedures for the TaskMaster API backend system. These procedures ensure data integrity and system availability in case of failures.

## Data Backup Procedures

### 1. Database Backups

#### Daily Automated Backups
- PostgreSQL database is backed up daily at 2:00 AM UTC
- Backups are stored in encrypted format
- Retention: 30 days of daily backups, 12 months of monthly backups

#### Manual Backup Process
```bash
# Create a backup manually
pg_dump -h hostname -U postgres -W -F t database_name > backup_file.tar

# Or for Neon PostgreSQL:
pg_dump "postgresql://username:password@endpoint.region.aws.neon.tech/dbname" --format=custom --file=backup_file.dump
```

#### Backup Verification
- Verify backup integrity weekly
- Test restoration procedure monthly
- Check backup size and contents

### 2. Application Configuration Backups

#### Environment Variables
- Store environment files in secure, encrypted location
- Version control for non-sensitive configuration
- Regular sync with production configurations

#### Application Code
- All code is stored in version control system (Git)
- Tag releases for easy rollback
- Maintain release notes and changelogs

## Recovery Procedures

### 1. Database Recovery

#### Full Database Recovery
```bash
# From tar format backup
pg_restore -h hostname -U postgres -d database_name -v backup_file.tar

# From dump format backup
pg_restore -h endpoint.region.aws.neon.tech -U username -d database_name -v backup_file.dump
```

#### Point-in-Time Recovery (PITR)
For PostgreSQL with WAL archiving enabled:
```bash
# Restore to specific timestamp
pg_restore --to-include-timestamp="YYYY-MM-DD HH:MM:SS" backup_file.dump
```

### 2. Application Recovery

#### Rollback Procedure
1. Stop the current application
2. Switch to the previous stable version
3. Restart the application
4. Verify health checks pass
5. Monitor for issues

#### Container-Based Recovery
```bash
# Rollback to previous Docker image
docker-compose down
docker-compose pull --quiet
docker-compose up -d
```

## Disaster Recovery Plan

### RTO (Recovery Time Objective)
- Critical systems: 4 hours
- Non-critical systems: 24 hours

### RPO (Recovery Point Objective)
- Maximum data loss: 1 hour (hourly backups)
- Database transactions: Real-time replication

### Recovery Scenarios

#### Scenario 1: Database Failure
1. Activate database replica if available
2. Restore from latest backup
3. Replay transaction logs if needed
4. Verify data integrity
5. Resume services

#### Scenario 2: Application Server Failure
1. Launch new instance from latest image
2. Mount persistent storage
3. Connect to database
4. Run health checks
5. Route traffic to new instance

#### Scenario 3: Complete System Failure
1. Provision new infrastructure
2. Restore database from backup
3. Deploy application from latest release
4. Configure networking and security
5. Validate all services
6. Redirect traffic

## Backup Testing

### Monthly Tests
- Full restoration test from backup
- Data integrity verification
- Performance validation
- Update documentation if needed

### Quarterly Drills
- Complete disaster recovery simulation
- Team training exercise
- Process refinement
- RTO/RPO validation

## Security Measures

### Encryption
- All backups are encrypted using AES-256
- Keys are managed separately from backup data
- Regular key rotation

### Access Control
- Backup access limited to authorized personnel
- Audit trails for all backup operations
- Two-person rule for critical operations

### Storage Location
- Primary backups: Cloud storage with replication
- Secondary backups: Different geographic region
- Offline backups: Physical storage for long-term retention

## Monitoring and Alerts

### Backup Monitoring
- Automated verification of backup completion
- Size and integrity checks
- Alert on backup failures
- Storage capacity monitoring

### Recovery Readiness
- Regular testing schedule adherence
- Recovery time tracking
- Alert on testing failures
- Capacity planning for recovery systems

## Roles and Responsibilities

### Database Administrator
- Manage database backups and restores
- Monitor backup jobs
- Validate backup integrity
- Execute recovery procedures

### DevOps Engineer
- Maintain backup infrastructure
- Configure backup schedules
- Monitor backup systems
- Coordinate recovery efforts

### Security Officer
- Approve backup security measures
- Review access controls
- Validate encryption standards
- Audit backup operations

## Documentation Updates

This document should be updated when:
- Backup procedures change
- New systems are added
- Recovery procedures are modified
- Lessons learned from incidents
- Regulatory requirements change

## Contact Information

In case of backup/recovery emergencies:
- Primary: [System Admin Contact]
- Secondary: [DevOps Lead Contact]
- Escalation: [Management Contact]

## Appendices

### Appendix A: Backup Scripts
```bash
#!/bin/bash
# Daily backup script
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="todoapp"
BACKUP_DIR="/backups"

# Create backup
pg_dump $DB_NAME | gzip > $BACKUP_DIR/${DB_NAME}_${DATE}.sql.gz

# Verify backup
gunzip -t $BACKUP_DIR/${DB_NAME}_${DATE}.sql.gz

# Cleanup old backups (older than 30 days)
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

### Appendix B: Recovery Checklist
- [ ] Verify backup integrity
- [ ] Ensure sufficient storage space
- [ ] Validate access credentials
- [ ] Prepare target environment
- [ ] Execute recovery procedure
- [ ] Verify data integrity
- [ ] Test application functionality
- [ ] Update documentation
- [ ] Notify stakeholders