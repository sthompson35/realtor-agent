-- Realtor Agent Database Schema
-- PostgreSQL compatible

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Properties table
CREATE TABLE properties (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    address TEXT NOT NULL,
    city VARCHAR(100),
    state VARCHAR(2),
    zip VARCHAR(10),
    county VARCHAR(100),
    parcel_apn VARCHAR(50),
    property_type VARCHAR(20) CHECK (property_type IN ('land', 'single_family', 'duplex', 'fourplex', 'apartment', 'commercial')),
    beds INTEGER,
    baths DECIMAL(3,1),
    sqft INTEGER,
    lot_size DECIMAL(10,2),
    year_built INTEGER,
    utilities TEXT,
    zoning VARCHAR(50),
    flood_zone VARCHAR(10),
    asking_price DECIMAL(12,2),
    source_url TEXT,
    source_site VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Owners table
CREATE TABLE owners (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    property_id UUID REFERENCES properties(id),
    owner_name TEXT,
    mailing_address TEXT,
    ownership_type VARCHAR(20) CHECK (ownership_type IN ('individual', 'llc', 'trust')),
    phone VARCHAR(20),
    email VARCHAR(255),
    contact_source VARCHAR(50),
    contact_permissions JSONB, -- consent flags, DNC status
    verified_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Underwriting table
CREATE TABLE underwriting (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    property_id UUID REFERENCES properties(id),
    arv DECIMAL(12,2), -- After Repair Value
    rent_monthly DECIMAL(10,2),
    rehab_estimate DECIMAL(10,2),
    holding_costs DECIMAL(10,2),
    closing_costs DECIMAL(10,2),
    offer_type VARCHAR(20) CHECK (offer_type IN ('cash', 'owner_finance', 'subject_to', 'lease_option')),
    mao DECIMAL(12,2), -- Maximum Allowable Offer
    exit_strategy VARCHAR(20) CHECK (exit_strategy IN ('flip', 'brrrr', 'wholesale', 'land_note')),
    risk_flags JSONB, -- Array of risk flags
    underwriter_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Leads table
CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    property_id UUID REFERENCES properties(id),
    owner_id UUID REFERENCES owners(id),
    status VARCHAR(20) DEFAULT 'new' CHECK (status IN ('new', 'contacted', 'qualified', 'negotiating', 'under_contract', 'closed', 'lost')),
    priority VARCHAR(10) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    source VARCHAR(50),
    assigned_to VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Outreach campaigns table
CREATE TABLE outreach_campaigns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id),
    campaign_type VARCHAR(20) CHECK (campaign_type IN ('initial', 'follow_up', 'negotiation')),
    channel VARCHAR(10) CHECK (channel IN ('sms', 'email', 'call', 'mail')),
    message TEXT,
    sent_at TIMESTAMP WITH TIME ZONE,
    response TEXT,
    response_at TIMESTAMP WITH TIME ZONE,
    compliance_checked BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Offers table
CREATE TABLE offers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id),
    offer_amount DECIMAL(12,2),
    offer_type VARCHAR(20) CHECK (offer_type IN ('cash', 'owner_finance', 'subject_to', 'lease_option')),
    terms JSONB, -- Detailed terms
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'countered', 'rejected')),
    expires_at TIMESTAMP WITH TIME ZONE,
    attorney_reviewed BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id),
    task_type VARCHAR(50),
    description TEXT,
    assigned_to VARCHAR(100),
    priority VARCHAR(10) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high')),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed', 'cancelled')),
    due_date TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Documents table
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id),
    document_type VARCHAR(50),
    file_name VARCHAR(255),
    file_path TEXT,
    file_size INTEGER,
    mime_type VARCHAR(100),
    uploaded_by VARCHAR(100),
    attorney_reviewed BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Audit log table
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_name VARCHAR(50),
    record_id UUID,
    action VARCHAR(10) CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_values JSONB,
    new_values JSONB,
    user_id VARCHAR(100),
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_properties_address ON properties(address);
CREATE INDEX idx_properties_type ON properties(property_type);
CREATE INDEX idx_properties_price ON properties(asking_price);
CREATE INDEX idx_owners_property ON owners(property_id);
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_property ON leads(property_id);
CREATE INDEX idx_underwriting_property ON underwriting(property_id);
CREATE INDEX idx_offers_lead ON offers(lead_id);
CREATE INDEX idx_tasks_lead ON tasks(lead_id);
CREATE INDEX idx_documents_lead ON documents(lead_id);
CREATE INDEX idx_audit_table_record ON audit_log(table_name, record_id);

-- Updated at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add updated_at triggers to relevant tables
CREATE TRIGGER update_properties_updated_at BEFORE UPDATE ON properties FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_owners_updated_at BEFORE UPDATE ON owners FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_underwriting_updated_at BEFORE UPDATE ON underwriting FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_leads_updated_at BEFORE UPDATE ON leads FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_offers_updated_at BEFORE UPDATE ON offers FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Audit trigger function
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
DECLARE
    old_row JSONB;
    new_row JSONB;
BEGIN
    IF TG_OP = 'DELETE' THEN
        old_row = row_to_json(OLD)::JSONB;
        INSERT INTO audit_log (table_name, record_id, action, old_values, user_id)
        VALUES (TG_TABLE_NAME, OLD.id, TG_OP, old_row, current_user);
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        old_row = row_to_json(OLD)::JSONB;
        new_row = row_to_json(NEW)::JSONB;
        INSERT INTO audit_log (table_name, record_id, action, old_values, new_values, user_id)
        VALUES (TG_TABLE_NAME, NEW.id, TG_OP, old_row, new_row, current_user);
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        new_row = row_to_json(NEW)::JSONB;
        INSERT INTO audit_log (table_name, record_id, action, new_values, user_id)
        VALUES (TG_TABLE_NAME, NEW.id, TG_OP, new_row, current_user);
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Add audit triggers (optional - enable for compliance)
-- CREATE TRIGGER audit_properties AFTER INSERT OR UPDATE OR DELETE ON properties FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();
-- CREATE TRIGGER audit_leads AFTER INSERT OR UPDATE OR DELETE ON leads FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();
-- CREATE TRIGGER audit_offers AFTER INSERT OR UPDATE OR DELETE ON offers FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();