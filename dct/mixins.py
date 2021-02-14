from django.views.generic.edit import ModelFormMixin

from .models import DataCollectTerminal


class ChangedStatusAccum(ModelFormMixin):
    """
    Extension when creating and updating a terminal to change the battery status.
    """
    def form_valid(self, form):
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
        return super().form_valid(form)