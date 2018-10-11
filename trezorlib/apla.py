from . import messages as proto
from .tools import CallException, expect, normalize_nfc, session


# ====== Client functions ====== #


@expect(proto.AplaWallet, field="address")
def get_wallet(client, n, show_display=True):
    return client.call(proto.AplaGetWallet(address_n=n, show_display=show_display))

@expect(proto.AplaPublicKey, field="public_key")
def get_public_key(client, n, show_display=True):
    return client.call(proto.AplaGetPublicKey(address_n=n, show_display=show_display))

@expect(proto.AplaMessageSignature)
def sign_message(client, n, message, note, ask_for_confirmation):
    message = normalize_nfc(message)
    note = normalize_nfc(note)
    return client.call(proto.AplaSignMessage(address_n=n, message=message, note=note, ask_for_confirmation=ask_for_confirmation))
