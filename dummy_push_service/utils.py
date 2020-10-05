import base64
import ecdsa


def generate_vapid_key_pair():
    """ Generate vapid key pair. Original source: https://gist.github.com/cjies/cc014d55976db80f610cd94ccb2ab21e """
    pk = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
    vk = pk.get_verifying_key()

    private_key = base64.urlsafe_b64encode(pk.to_string()).strip(b"=").decode('ascii')
    public_key = base64.urlsafe_b64encode(b"\x04" + vk.to_string()).strip(b"=").decode('ascii')

    return private_key, public_key