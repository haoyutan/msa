from rest_framework import serializers

from .models import MicroService


class MicroServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroService
        fields = ('name', 'url', 'created', 'is_external',
                  'token_for_read', 'token_for_write', 'token_for_admin',)

    def safe_data(self, client_micro_service=None):
        """
        TODO: Add models for permission control.
        """
        d = self.data
        client_ms_name = None
        if client_micro_service is not None:
            client_ms_name = client_micro_service.name
        
        p_read, p_write, p_admin = self._get_permissions(client_ms_name,
                                                         d.get('name'))
        safe_data = {
            'name'           : d.get('name'),
            'url'            : d.get('url'),
            'created'        : d.get('created'),
            'is_external'    : d.get('is_external'),
            'token_for_read' : d.get('token_for_read') if p_read else None,
            'token_for_write': d.get('token_for_write') if p_write else None,
            'token_for_admin': d.get('token_for_admin') if p_admin else None,
        }
        return safe_data

    def _get_permissions(self, client_ms_name, server_ms_name):
        if client_ms_name is None:
            return (False, False, False)
        elif client_ms_name == server_ms_name:
            return (True, True, True)
        else:
            return (True, True, False)
