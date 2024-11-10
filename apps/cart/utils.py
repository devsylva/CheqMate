from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def update_cart_sync_status(cart_id, is_synced):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'cart_{cart_id}',
        {
            'type': 'send_cart_sync_update',
            'is_synced': is_synced
        }
    )
