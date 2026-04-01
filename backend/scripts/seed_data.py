#!/usr/bin/env python3
"""Seed initial data into the database"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.postgres import engine
from app.models import User, Role, Permission
from passlib.context import CryptContext
from sqlalchemy import text

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed_data():
    """Seed initial roles, permissions, and admin user"""

    with engine.connect() as conn:
        # Start a transaction
        trans = conn.begin()

        try:
            # Create permissions
            permissions_data = [
                # User management
                ("users.read", "users", "read", "View users"),
                ("users.create", "users", "create", "Create new users"),
                ("users.update", "users", "update", "Update user information"),
                ("users.delete", "users", "delete", "Delete users"),

                # Regulatory updates
                ("regulatory_updates.read", "regulatory_updates", "read", "View regulatory updates"),
                ("regulatory_updates.create", "regulatory_updates", "create", "Create regulatory updates"),
                ("regulatory_updates.update", "regulatory_updates", "update", "Update regulatory updates"),
                ("regulatory_updates.delete", "regulatory_updates", "delete", "Delete regulatory updates"),

                # Requirements
                ("requirements.read", "requirements", "read", "View requirements"),
                ("requirements.create", "requirements", "create", "Create requirements"),
                ("requirements.update", "requirements", "update", "Update requirements"),
                ("requirements.delete", "requirements", "delete", "Delete requirements"),

                # Data mappings
                ("data_mappings.read", "data_mappings", "read", "View data mappings"),
                ("data_mappings.create", "data_mappings", "create", "Create data mappings"),
                ("data_mappings.update", "data_mappings", "update", "Update data mappings"),
                ("data_mappings.delete", "data_mappings", "delete", "Delete data mappings"),

                # Generated code
                ("generated_code.read", "generated_code", "read", "View generated code"),
                ("generated_code.create", "generated_code", "create", "Create generated code"),
                ("generated_code.update", "generated_code", "update", "Update generated code"),
                ("generated_code.delete", "generated_code", "delete", "Delete generated code"),

                # Reports
                ("reports.read", "reports", "read", "View reports"),
                ("reports.create", "reports", "create", "Create reports"),
                ("reports.update", "reports", "update", "Update reports"),
                ("reports.delete", "reports", "delete", "Delete reports"),
                ("reports.submit", "reports", "submit", "Submit reports"),
                ("reports.approve", "reports", "approve", "Approve reports"),

                # Workflows
                ("workflows.read", "workflows", "read", "View workflows"),
                ("workflows.create", "workflows", "create", "Create workflows"),
                ("workflows.update", "workflows", "update", "Update workflows"),
                ("workflows.delete", "workflows", "delete", "Delete workflows"),
                ("workflows.execute", "workflows", "execute", "Execute workflows"),

                # Audit logs
                ("audit_logs.read", "audit_logs", "read", "View audit logs"),

                # Admin
                ("admin.full_access", "admin", "*", "Full administrative access"),
            ]

            for perm_name, resource, action, description in permissions_data:
                conn.execute(
                    text("""
                        INSERT INTO permissions (name, resource, action, description, created_at)
                        VALUES (:name, :resource, :action, :description, :created_at)
                        ON CONFLICT (name) DO NOTHING
                    """),
                    {
                        "name": perm_name,
                        "resource": resource,
                        "action": action,
                        "description": description,
                        "created_at": datetime.utcnow(),
                    }
                )

            print(f"✅ Created {len(permissions_data)} permissions")

            # Create roles
            roles_data = [
                ("admin", "Administrator", "Full system access"),
                ("compliance_manager", "Compliance Manager", "Manage regulatory compliance"),
                ("business_analyst", "Business Analyst", "Analyze requirements and create mappings"),
                ("developer", "Developer", "Develop and test code"),
                ("qa_tester", "QA Tester", "Test and validate code"),
                ("viewer", "Viewer", "Read-only access"),
            ]

            for role_name, display_name, description in roles_data:
                conn.execute(
                    text("""
                        INSERT INTO roles (name, display_name, description, created_at, updated_at)
                        VALUES (:name, :display_name, :description, :created_at, :updated_at)
                        ON CONFLICT (name) DO NOTHING
                    """),
                    {
                        "name": role_name,
                        "display_name": display_name,
                        "description": description,
                        "created_at": datetime.utcnow(),
                        "updated_at": datetime.utcnow(),
                    }
                )

            print(f"✅ Created {len(roles_data)} roles")

            # Assign all permissions to admin role
            result = conn.execute(text("SELECT id FROM roles WHERE name = 'admin'"))
            admin_role_id = result.scalar()

            result = conn.execute(text("SELECT id FROM permissions"))
            permission_ids = [row[0] for row in result.fetchall()]

            for perm_id in permission_ids:
                conn.execute(
                    text("""
                        INSERT INTO role_permissions (role_id, permission_id)
                        VALUES (:role_id, :permission_id)
                        ON CONFLICT DO NOTHING
                    """),
                    {"role_id": admin_role_id, "permission_id": perm_id}
                )

            print(f"✅ Assigned {len(permission_ids)} permissions to admin role")

            # Create default admin user
            hashed_password = pwd_context.hash("admin123")

            conn.execute(
                text("""
                    INSERT INTO users (username, email, hashed_password, full_name, department,
                                     is_active, is_superuser, created_at, updated_at)
                    VALUES (:username, :email, :hashed_password, :full_name, :department,
                           :is_active, :is_superuser, :created_at, :updated_at)
                    ON CONFLICT (username) DO NOTHING
                """),
                {
                    "username": "admin",
                    "email": "admin@nttdata.com",
                    "hashed_password": hashed_password,
                    "full_name": "System Administrator",
                    "department": "IT",
                    "is_active": True,
                    "is_superuser": True,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                }
            )

            # Assign admin role to admin user
            result = conn.execute(text("SELECT id FROM users WHERE username = 'admin'"))
            admin_user_id = result.scalar()

            if admin_user_id:
                conn.execute(
                    text("""
                        INSERT INTO user_roles (user_id, role_id)
                        VALUES (:user_id, :role_id)
                        ON CONFLICT DO NOTHING
                    """),
                    {"user_id": admin_user_id, "role_id": admin_role_id}
                )

                print("✅ Created admin user (username: admin, password: admin123)")

            # Commit transaction
            trans.commit()
            print("✅ Database seeding completed successfully")

        except Exception as e:
            trans.rollback()
            print(f"❌ Error seeding data: {e}")
            raise


if __name__ == "__main__":
    seed_data()
