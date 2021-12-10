import json
from datetime import datetime

from django.core import serializers
from django.db import models, transaction
from django.utils import timezone
from rest_framework.exceptions import APIException

from core.models import User
from core.models.audit_trail import AuditTrail
from investhubapi.permissions.current_user import get_current_user, get_current_ip
from investhubapi.utils.manager import EntireManager, ValidManager


class ReadOnlyModel(models.Model):
    pass

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return


class CRUSDModel(models.Model):
    # Create, Retrieve, Update, Soft Delete
    created_by = models.ForeignKey(User, default=None, on_delete=models.DO_NOTHING, db_constraint=False,
                                   related_name="%(class)s_create_related",
                                   db_column='created_by')
    updated_by = models.ForeignKey(User, default=None, null=True, on_delete=models.DO_NOTHING, db_constraint=False,
                                   related_name="%(class)s_update_related",
                                   db_column='updated_by')
    deleted_by = models.ForeignKey(User, default=None, null=True, on_delete=models.DO_NOTHING, db_constraint=False,
                                   related_name="%(class)s_delete_related",
                                   db_column='deleted_by')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = ValidManager()
    o = EntireManager()

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        self.pure_save = False
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_user():
        if get_current_user().is_anonymous:
            raise APIException("User information is required for this operation")
        return get_current_user()

    @transaction.atomic
    def delete(self, *args, **kwargs):
        self.deleted_by = self.get_user()
        self.deleted_at = timezone.now()
        create_audit_trail(self, "DELETE")
        return super().save(update_fields=['deleted_by', 'deleted_at'])

    @transaction.atomic
    def save(self, *args, **kwargs):
        """
        if primary key is set, set update_user id
        if not set, set create user id
        """
        is_create = True
        if not self.pure_save:
            if self.id:
                is_create = False
                self.update_user = self.get_user()
                self.update_date = datetime.now()
            else:
                self.create_user = self.get_user()
                self.create_date = datetime.now()
        super().save(*args, **kwargs)
        if not self.pure_save:
            if is_create:
                create_audit_trail(self, "CREATE")
            else:
                create_audit_trail(self, "UPDATE")

    def create(self, **data):
        for attr, value in data.items():
            setattr(self, attr, value)
        self.save()

    def update(self, **data):
        if self.id:
            for attr, value in data.items():
                setattr(self, attr, value)
            self.save()
        else:
            raise APIException("Cannot update in update() with no primary key.")

    def update_child_list(self, child_data=None, child_class=None, fk_field=None, nest=None):
        exist_child_list = child_class.objects.filter(**{fk_field: self})
        exist_child_dicts = {row.id: row for row in exist_child_list}

        nest_data = None
        for data in child_data:
            if nest:
                nest_data = data.pop(nest['list_field'], None)
            _id = data.get('id')
            if _id is None:
                # create
                c = child_class.objects.create(**{fk_field: self}, **data)
            else:
                # check exist in child list or not
                e_c = exist_child_dicts.get(_id)
                if e_c is None:
                    # create (seldom will reach here)
                    # remove id is too prevent repeat pk
                    data.pop('id')
                    c = child_class.objects.create(**{fk_field: self}, **data)
                else:
                    # update
                    c = child_class.objects.get(pk=_id)
                    c.update(**data)

            if nest_data is not None:
                c.update_child_list(child_data=nest_data,
                                    child_class=nest['child_class'],
                                    fk_field=nest['fk_field'],
                                    nest=nest.get('nest'))

        data_id_list = [data['id'] for data in child_data if data.get('id') is not None]
        for c_id, c in exist_child_dicts.items():
            if c_id not in data_id_list:
                c.delete()

    def create_child_list(self, child_data=None, child_class=None, fk_field=None, nest=None):
        nest_data = None
        for row in child_data:
            if nest:
                nest_data = row.pop(nest['list_field'], None)

            # remove id is too prevent repeat pk
            row.pop('id', None)
            c = child_class.objects.create(**{fk_field: self}, **row)

            if nest_data:
                c.create_child_list(child_data=nest_data,
                                    child_class=nest['child_class'],
                                    fk_field=nest['fk_field'],
                                    nest=nest.get('nest'))


def create_audit_trail(instance, action):
    ins = json.loads(serializers.serialize('json', [instance]))[0]

    model = ins.get("model")
    model_id = ins.get("pk")
    log = json.dumps(ins.get("fields"))
    ip_address = get_current_ip()

    AuditTrail(model=model,
               model_id=model_id,
               action=action,
               log=log,
               user=get_current_user(),
               ip_address=ip_address).save()
