"""Data mapping schemas"""

from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class DataMappingBase(BaseModel):
    """Base data mapping schema"""
    source_system: str = Field(..., max_length=200, description="Source system name")
    source_schema: Optional[str] = Field(default=None, max_length=200, description="Source schema")
    source_table: str = Field(..., max_length=200, description="Source table name")
    source_column: str = Field(..., max_length=200, description="Source column name")
    source_data_type: Optional[str] = Field(default=None, max_length=100, description="Source data type")
    target_system: Optional[str] = Field(default=None, max_length=200, description="Target system name")
    target_schema: Optional[str] = Field(default=None, max_length=200, description="Target schema")
    target_table: Optional[str] = Field(default=None, max_length=200, description="Target table name")
    target_field: str = Field(..., max_length=200, description="Target field name")
    target_data_type: Optional[str] = Field(default=None, max_length=100, description="Target data type")
    transformation_rule: Optional[str] = Field(default=None, description="Transformation rule description")
    validation_rule: Optional[str] = Field(default=None, description="Validation rule description")
    is_active: bool = Field(default=True, description="Whether mapping is active")


class DataMappingCreate(DataMappingBase):
    """Schema for creating a data mapping"""
    requirement_id: UUID = Field(..., description="Related requirement ID")
    transformation_logic: Optional[Dict[str, Any]] = Field(default=None, description="Structured transformation steps")
    validation_logic: Optional[Dict[str, Any]] = Field(default=None, description="Structured validation rules")
    business_rule_description: Optional[str] = Field(default=None, description="Business rule description")
    calculation_formula: Optional[str] = Field(default=None, description="Calculation formula if applicable")
    data_quality_rules: Optional[List[str]] = Field(default=[], description="Data quality rules")
    mapping_notes: Optional[str] = Field(default=None, description="Additional notes")
    tags: Optional[List[str]] = Field(default=[], description="Tags for categorization")

    class Config:
        json_schema_extra = {
            "example": {
                "requirement_id": "uuid-here",
                "source_system": "TradingDB",
                "source_schema": "public",
                "source_table": "transactions",
                "source_column": "trade_date",
                "source_data_type": "timestamp",
                "target_system": "ReportingDB",
                "target_schema": "reporting",
                "target_table": "mifid_reports",
                "target_field": "transaction_date",
                "target_data_type": "date",
                "transformation_rule": "Convert timestamp to date (UTC)",
                "validation_rule": "Must not be null, must be <= current date",
                "business_rule_description": "Transaction date for regulatory reporting",
                "calculation_formula": "DATE(trade_date AT TIME ZONE 'UTC')",
                "data_quality_rules": ["not_null", "valid_date", "not_future"],
                "is_active": True,
                "tags": ["mifid", "transaction_reporting"]
            }
        }


class DataMappingUpdate(BaseModel):
    """Schema for updating a data mapping"""
    source_system: Optional[str] = Field(default=None, max_length=200)
    source_schema: Optional[str] = Field(default=None, max_length=200)
    source_table: Optional[str] = Field(default=None, max_length=200)
    source_column: Optional[str] = Field(default=None, max_length=200)
    source_data_type: Optional[str] = Field(default=None, max_length=100)
    target_system: Optional[str] = Field(default=None, max_length=200)
    target_schema: Optional[str] = Field(default=None, max_length=200)
    target_table: Optional[str] = Field(default=None, max_length=200)
    target_field: Optional[str] = Field(default=None, max_length=200)
    target_data_type: Optional[str] = Field(default=None, max_length=100)
    transformation_rule: Optional[str] = Field(default=None)
    transformation_logic: Optional[Dict[str, Any]] = Field(default=None)
    validation_rule: Optional[str] = Field(default=None)
    validation_logic: Optional[Dict[str, Any]] = Field(default=None)
    business_rule_description: Optional[str] = Field(default=None)
    calculation_formula: Optional[str] = Field(default=None)
    data_quality_rules: Optional[List[str]] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)
    is_validated: Optional[bool] = Field(default=None)
    is_approved: Optional[bool] = Field(default=None)
    mapping_notes: Optional[str] = Field(default=None)
    tags: Optional[List[str]] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "is_validated": True,
                "is_approved": True,
                "mapping_notes": "Validated and approved for production use"
            }
        }


class DataMappingResponse(DataMappingBase):
    """Schema for data mapping response"""
    id: UUID = Field(..., description="Data mapping ID")
    requirement_id: UUID = Field(..., description="Related requirement ID")
    transformation_logic: Optional[Dict[str, Any]] = Field(default=None, description="Transformation logic")
    validation_logic: Optional[Dict[str, Any]] = Field(default=None, description="Validation logic")
    business_rule_description: Optional[str] = Field(default=None, description="Business rule")
    calculation_formula: Optional[str] = Field(default=None, description="Calculation formula")
    data_quality_rules: List[str] = Field(default=[], description="Data quality rules")
    is_validated: bool = Field(default=False, description="Whether mapping is validated")
    is_approved: bool = Field(default=False, description="Whether mapping is approved")
    confidence_score: Optional[str] = Field(default=None, description="AI confidence score")
    mapping_notes: Optional[str] = Field(default=None, description="Notes")
    tags: List[str] = Field(default=[], description="Tags")
    created_by: Optional[UUID] = Field(default=None, description="Creator user ID")
    approved_by: Optional[UUID] = Field(default=None, description="Approver user ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    approved_at: Optional[datetime] = Field(default=None, description="Approval timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "uuid-here",
                "requirement_id": "uuid-here",
                "source_system": "TradingDB",
                "source_table": "transactions",
                "source_column": "trade_date",
                "source_data_type": "timestamp",
                "target_field": "transaction_date",
                "target_data_type": "date",
                "transformation_rule": "Convert timestamp to date",
                "validation_rule": "Must not be null",
                "business_rule_description": "Transaction date for reporting",
                "data_quality_rules": ["not_null", "valid_date"],
                "is_active": True,
                "is_validated": True,
                "is_approved": True,
                "confidence_score": "0.95",
                "tags": ["mifid"],
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-01-20T14:00:00Z"
            }
        }
