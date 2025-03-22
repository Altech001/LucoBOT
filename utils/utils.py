#================== Video ID ==============
#
#===========================================
import hmac
import hashlib
from datetime import datetime
import re
import base64
import secrets
from typing import Optional

id = str(secrets.randbits(1000))
def video_id(url: str, id:Optional[str] = id) -> str:
    
    digest = hmac.new(
        id.encode("utf-8"),
        msg=url.encode("utf-8"),
        digestmod=hashlib.md5,
    ).digest()
    
    return base64.b64encode(digest).decode()

name = video_id(url="https")
print(name)

#================== Unique Name ==============
#
#===========================================


def generate_unique_name(url: str) -> str:
    """
    Generate a unique name for the file based on the URL.
    """
    timestamp = datetime.now().strftime('%Y_%m_%d__%H_%M_%S_%f')
    domain = re.sub(r'\W+', '*_*', url.split('//')[-1].split('/')[0])
    return f"{domain}_{timestamp}"

name = generate_unique_name(url="https://www.youtube.com/AJHJHbnb12")
print(name)

#================== Youtube Links & Video Links ==============
import re
#===========================================================

def url_link(url: str) -> str:
    yt_url = r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+'
    vd_url = r'(https?://)?(www\.)?(tiktok\.com|vm\.tiktok\.com)/.+'
    
    return re.match(yt_url, url) or re.match(vd_url, url)

#======================================================================
