from django.utils import timezone
from django.views.generic.edit import ModelFormMixin

from .models import DataCollectTerminal, DataCollectTerminalRemark


class ChangedStatusAccum(ModelFormMixin):
    """
    Extension when creating and updating a terminal to change the battery status.
    """
    def form_valid(self, form):
        """
        Redefined method for enabling business logic when
        creating and modifying data collect terminals.
        """
        self.change_status_accum(form)
        self.data_collect_terminal_remark(form)
        return super().form_valid(form)

    def change_status_accum(self, form):
        """
        Called to change the state of the battery.
        Possible states:
        1. Installed
        2. Uninstalled
        """
        accum_in_form = form.cleaned_data['accumulator']
        # If this terminal already exists
        if DataCollectTerminal.objects.filter(name=form.cleaned_data['name']):
            accum_in_db = DataCollectTerminal.objects.get(id=self.object.id).accumulator
            if accum_in_db != accum_in_form:
                if accum_in_db and accum_in_form:
                    accum_in_db.changed_status(2)
                    accum_in_form.changed_status(1)
                elif accum_in_db:
                    accum_in_db.changed_status(2)
                else:
                    accum_in_form.changed_status(1)
        # If a new terminal is being created
        else:
            if accum_in_form:
                accum_in_form.changed_status(1)

    def data_collect_terminal_remark(self, form):
        """
        Remark for data collect terminal.
        """
        remark_in_form = form.cleaned_data['remark']
        # If this terminal already exists
        if DataCollectTerminal.objects.filter(name=form.cleaned_data['name']):
            obj_dct = DataCollectTerminal.objects.get(name=form.cleaned_data['name'])
            remark_in_db = obj_dct.remark
            # If there are remarks in the remarks database
            if DataCollectTerminalRemark.objects.filter(data_collect_terminal=obj_dct.id):
                if remark_in_form != remark_in_db:
                    DataCollectTerminalRemark.objects.create(data_collect_terminal=obj_dct,
                                                             remark=remark_in_form,
                                                             date=timezone.now())
            else:
                if remark_in_db != remark_in_form:
                    if remark_in_db:
                        DataCollectTerminalRemark.objects.create(data_collect_terminal=obj_dct,
                                                                 remark=remark_in_db,
                                                                 date=obj_dct.date)
                    DataCollectTerminalRemark.objects.create(data_collect_terminal=obj_dct,
                                                             remark=remark_in_form,
                                                             date=timezone.now())
