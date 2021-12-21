# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AdditionalCharge(models.Model):
    id = models.BigAutoField(primary_key=True)
    rentid = models.ForeignKey('Rent', models.DO_NOTHING, db_column='rentid', blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    type = models.CharField(max_length=128, blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.CharField(max_length=128, blank=True, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True)
    modifiedby = models.CharField(max_length=128, blank=True, null=True)
    activeflag = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'additional_charge'


class FileMapper(models.Model):
    id = models.AutoField()
    original_fileid = models.BigIntegerField(blank=True, null=True)
    duplicate_fileid = models.BigIntegerField(blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.CharField(max_length=128, blank=True, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True)
    modifiedby = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'file_mapper'
        unique_together = (('original_fileid', 'duplicate_fileid'),)


class Fileanalytics(models.Model):
    id = models.BigAutoField()
    fileid = models.BigIntegerField(blank=True, null=True)
    file_name = models.CharField(max_length=-1, blank=True, null=True)
    title = models.CharField(max_length=-1, blank=True, null=True)
    tags = models.JSONField(blank=True, null=True)
    party = models.JSONField(blank=True, null=True)
    address = models.JSONField(blank=True, null=True)
    address_text = models.JSONField(blank=True, null=True)
    renewal = models.TextField(blank=True, null=True)
    renewal_text = models.JSONField(blank=True, null=True)
    locked_in_period = models.JSONField(blank=True, null=True)
    locked_in_period_text = models.JSONField(blank=True, null=True)
    termination = models.TextField(blank=True, null=True)
    termination_text = models.JSONField(blank=True, null=True)
    termination_event = models.JSONField(blank=True, null=True)
    termination_event_text = models.JSONField(blank=True, null=True)
    termination_at_convenience = models.TextField(blank=True, null=True)
    termination_at_convenience_text = models.JSONField(blank=True, null=True)
    force_majeure = models.TextField(blank=True, null=True)
    force_majeure_text = models.JSONField(blank=True, null=True)
    force_majeure_event = models.JSONField(blank=True, null=True)
    force_majeure_event_text = models.JSONField(blank=True, null=True)
    governing_law = models.TextField(blank=True, null=True)
    governing_law_text = models.JSONField(blank=True, null=True)
    jurisdiction = models.JSONField(blank=True, null=True)
    jurisdiction_text = models.JSONField(blank=True, null=True)
    assignment = models.TextField(blank=True, null=True)
    assignment_text = models.JSONField(blank=True, null=True)
    assignment_notice = models.TextField(blank=True, null=True)
    assignment_notice_text = models.JSONField(blank=True, null=True)
    assignment_consent = models.TextField(blank=True, null=True)
    assignment_consent_text = models.JSONField(blank=True, null=True)
    term_start = models.JSONField(blank=True, null=True)
    term = models.TextField(blank=True, null=True)
    term_text = models.JSONField(blank=True, null=True)
    term_start_text = models.JSONField(blank=True, null=True)
    term_start_map = models.JSONField(blank=True, null=True)
    term_end = models.JSONField(blank=True, null=True)
    term_end_text = models.JSONField(blank=True, null=True)
    term_end_map = models.JSONField(blank=True, null=True)
    term_duration = models.JSONField(blank=True, null=True)
    term_duration_text = models.JSONField(blank=True, null=True)
    payment_present = models.TextField(blank=True, null=True)
    payment_text = models.JSONField(blank=True, null=True)
    payment_amount = models.JSONField(blank=True, null=True)
    payment_amount_text = models.JSONField(blank=True, null=True)
    payment_duration = models.JSONField(blank=True, null=True)
    payment_duration_text = models.JSONField(blank=True, null=True)
    indemnity = models.TextField(blank=True, null=True)
    indemnity_text = models.JSONField(blank=True, null=True)
    indemnity_amounts = models.JSONField(blank=True, null=True)
    indemnity_amounts_text = models.JSONField(blank=True, null=True)
    indemnity_extent_of_costs = models.JSONField(blank=True, null=True)
    indemnity_extent_of_costs_text = models.JSONField(blank=True, null=True)
    indemnity_triggering_event = models.JSONField(blank=True, null=True)
    indemnity_triggering_event_text = models.JSONField(blank=True, null=True)
    indemnity_payer = models.JSONField(blank=True, null=True)
    indemnity_payer_text = models.JSONField(blank=True, null=True)
    indemnity_payee = models.JSONField(blank=True, null=True)
    indemnity_payee_text = models.JSONField(blank=True, null=True)
    confidentiality = models.TextField(blank=True, null=True)
    confidentiality_text = models.JSONField(blank=True, null=True)
    confidentiality_nature = models.JSONField(blank=True, null=True)
    confidentiality_nature_text = models.JSONField(blank=True, null=True)
    confidentiality_duration = models.JSONField(blank=True, null=True)
    confidentiality_duration_text = models.JSONField(blank=True, null=True)
    change_of_control = models.TextField(blank=True, null=True)
    change_of_control_text = models.JSONField(blank=True, null=True)
    change_of_control_definition = models.TextField(blank=True, null=True)
    change_of_control_definition_text = models.JSONField(blank=True, null=True)
    change_of_control_termination = models.TextField(blank=True, null=True)
    change_of_control_termination_text = models.JSONField(blank=True, null=True)
    change_of_control_payment = models.TextField(blank=True, null=True)
    change_of_control_payment_text = models.JSONField(blank=True, null=True)
    change_of_control_assignment = models.TextField(blank=True, null=True)
    change_of_control_assignment_text = models.JSONField(blank=True, null=True)
    change_of_control_consent = models.TextField(blank=True, null=True)
    change_of_control_consent_text = models.JSONField(blank=True, null=True)
    change_of_control_notice = models.TextField(blank=True, null=True)
    change_of_control_notice_text = models.JSONField(blank=True, null=True)
    change_of_control_events_of_default = models.TextField(blank=True, null=True)
    change_of_control_events_of_default_text = models.JSONField(blank=True, null=True)
    insurance = models.TextField(blank=True, null=True)
    insurance_text = models.JSONField(blank=True, null=True)
    notice = models.TextField(blank=True, null=True)
    notice_text = models.JSONField(blank=True, null=True)
    non_compete = models.TextField(blank=True, null=True)
    non_compete_text = models.JSONField(blank=True, null=True)
    non_compete_duration = models.JSONField(blank=True, null=True)
    non_compete_duration_text = models.JSONField(blank=True, null=True)
    non_compete_jurisdiction = models.JSONField(blank=True, null=True)
    non_compete_jurisdiction_text = models.JSONField(blank=True, null=True)
    non_solicitation = models.TextField(blank=True, null=True)
    non_solicitation_text = models.JSONField(blank=True, null=True)
    non_solicitation_duration = models.JSONField(blank=True, null=True)
    non_solicitation_duration_text = models.JSONField(blank=True, null=True)
    liability = models.TextField(blank=True, null=True)
    liability_text = models.JSONField(blank=True, null=True)
    liability_amount = models.JSONField(blank=True, null=True)
    liability_amount_text = models.JSONField(blank=True, null=True)
    consent = models.TextField(blank=True, null=True)
    consent_type = models.TextField(blank=True, null=True)
    consent_text = models.JSONField(blank=True, null=True)
    consent_authority = models.JSONField(blank=True, null=True)
    consent_authority_text = models.JSONField(blank=True, null=True)
    dispute_resolution = models.TextField(blank=True, null=True)
    dispute_resolution_text = models.JSONField(blank=True, null=True)
    dispute_resolution_panel = models.JSONField(blank=True, null=True)
    dispute_resolution_panel_text = models.JSONField(blank=True, null=True)
    dispute_resolution_venue = models.JSONField(blank=True, null=True)
    dispute_resolution_venue_text = models.JSONField(blank=True, null=True)
    dispute_resolution_act = models.JSONField(blank=True, null=True)
    dispute_resolution_act_text = models.JSONField(blank=True, null=True)
    dispute_resolution_arbitration = models.TextField(blank=True, null=True)
    dispute_resolution_arbitration_text = models.JSONField(blank=True, null=True)
    dispute_resolution_conciliation = models.TextField(blank=True, null=True)
    dispute_resolution_conciliation_text = models.JSONField(blank=True, null=True)
    dispute_resolution_mediation = models.TextField(blank=True, null=True)
    dispute_resolution_mediation_text = models.JSONField(blank=True, null=True)
    dispute_resolution_negotiation = models.TextField(blank=True, null=True)
    dispute_resolution_negotiation_text = models.JSONField(blank=True, null=True)
    dispute_resolution_others = models.TextField(blank=True, null=True)
    dispute_resolution_others_text = models.JSONField(blank=True, null=True)
    events_of_default_present = models.TextField(blank=True, null=True)
    events_of_default_present_text = models.JSONField(blank=True, null=True)
    events_of_default = models.JSONField(blank=True, null=True)
    events_of_default_text = models.JSONField(blank=True, null=True)
    other_obligations = models.TextField(blank=True, null=True)
    other_obligations_text = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fileanalytics'


class Hierarchy(models.Model):
    id = models.BigAutoField(primary_key=True)
    fileid = models.BigIntegerField(blank=True, null=True)
    parentid = models.BigIntegerField(blank=True, null=True)
    activeflag = models.BooleanField(blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.CharField(max_length=128, blank=True, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True)
    modifiedby = models.CharField(max_length=128, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hierarchy'
        unique_together = (('fileid', 'parentid'),)


class Lease(models.Model):
    id = models.BigAutoField(primary_key=True)
    file_name = models.CharField(max_length=512, blank=True, null=True)
    pdf = models.BinaryField(blank=True, null=True)
    txt = models.TextField(blank=True, null=True)
    extracted = models.JSONField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.CharField(max_length=128, blank=True, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True)
    modifiedby = models.CharField(max_length=128, blank=True, null=True)
    activeflag = models.BooleanField(blank=True, null=True)
    contract_type = models.CharField(max_length=32, blank=True, null=True)
    textract = models.JSONField(blank=True, null=True)
    analyticsdata = models.JSONField(blank=True, null=True)
    pdf_hash = models.TextField(blank=True, null=True)
    file_size = models.BigIntegerField(blank=True, null=True)
    modified_file_name = models.CharField(max_length=256, blank=True, null=True)
    analytics2 = models.JSONField(blank=True, null=True)
    doc_type = models.CharField(max_length=258, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lease'


class LeaseParty(models.Model):
    id = models.BigAutoField(primary_key=True)
    leaseid = models.ForeignKey(Lease, models.DO_NOTHING, db_column='leaseid', blank=True, null=True)
    partyid = models.ForeignKey('Party', models.DO_NOTHING, db_column='partyid', blank=True, null=True)
    type = models.CharField(max_length=128, blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.CharField(max_length=128, blank=True, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True)
    modifiedby = models.CharField(max_length=128, blank=True, null=True)
    activeflag = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lease_party'


class LeaseStageAws(models.Model):
    id = models.BigIntegerField(blank=True, null=True)
    file_name = models.CharField(max_length=512, blank=True, null=True)
    pdf = models.BinaryField(blank=True, null=True)
    txt = models.TextField(blank=True, null=True)
    extracted = models.JSONField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.CharField(max_length=128, blank=True, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True)
    modifiedby = models.CharField(max_length=128, blank=True, null=True)
    activeflag = models.BooleanField(blank=True, null=True)
    contract_type = models.CharField(max_length=32, blank=True, null=True)
    textract = models.JSONField(blank=True, null=True)
    analyticsdata = models.JSONField(blank=True, null=True)
    pdf_hash = models.TextField(blank=True, null=True)
    file_size = models.BigIntegerField(blank=True, null=True)
    modified_file_name = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lease_stage_aws'


class LeaseTerminate(models.Model):
    id = models.BigAutoField(primary_key=True)
    charge = models.IntegerField(blank=True, null=True)
    terminate_condition = models.TextField(blank=True, null=True)
    notice_period = models.IntegerField(blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.CharField(max_length=128, blank=True, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True)
    modifiedby = models.CharField(max_length=128, blank=True, null=True)
    activeflag = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lease_terminate'


class Party(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.CharField(max_length=128, blank=True, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True)
    modifiedby = models.CharField(max_length=128, blank=True, null=True)
    activeflag = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'party'


class Rent(models.Model):
    id = models.BigAutoField(primary_key=True)
    leaseid = models.ForeignKey(Lease, models.DO_NOTHING, db_column='leaseid', blank=True, null=True)
    base_rent = models.FloatField(blank=True, null=True)
    security_deposit = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=32, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    renewable = models.BooleanField(blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.CharField(max_length=128, blank=True, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True)
    modifiedby = models.CharField(max_length=128, blank=True, null=True)
    activeflag = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rent'


class SimpleFilter(models.Model):
    fileid = models.IntegerField(primary_key=True)
    process = models.CharField(max_length=20, blank=True, null=True)
    active = models.CharField(max_length=20, blank=True, null=True)
    expiry = models.BooleanField(blank=True, null=True)
    flagged = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'simple_filter'


class Status(models.Model):
    id = models.AutoField()
    fileid = models.BigIntegerField(unique=True, blank=True, null=True)
    textract = models.BooleanField(blank=True, null=True)
    analytics = models.BooleanField(blank=True, null=True)
    normalization = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'status'


class TerminateMap(models.Model):
    id = models.BigAutoField(primary_key=True)
    leaseid = models.ForeignKey(Lease, models.DO_NOTHING, db_column='leaseid', blank=True, null=True)
    terminateid = models.ForeignKey(LeaseTerminate, models.DO_NOTHING, db_column='terminateid', blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.CharField(max_length=128, blank=True, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True)
    modifiedby = models.CharField(max_length=128, blank=True, null=True)
    activeflag = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'terminate_map'
