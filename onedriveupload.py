import onedrivesdk
from onedrivesdk.helpers import GetAuthCodeServer
import sys

filename = sys.argv[1]
location =sys.argv[2]
uploadname = sys.argv[3]

print("saving "+filename)
print("at location: " + location)
print("with the name: " + uploadname)

redirect_uri = 'http://localhost:8080/'
client_secret = 'Rh2@Z/]Lrr1[UxHNwucxEr7yIz69.x88'
scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']

client = onedrivesdk.get_default_client(
    client_id='d81be3b3-f95d-4aec-b929-0b4f9c056c32', scopes=scopes)

auth_url = client.auth_provider.get_auth_url(redirect_uri)

#this will block until we have the code
code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)

client.auth_provider.authenticate(code, redirect_uri, client_secret)
#returned_item = client.item(drive='me', id='root').children['hi2.txt'].upload('./test3.txt')

'''
haid = 'B2FE1C9399604511!14953'
rr = 'root'
root_folder = client.item(drive='me', id=rr).children.get()
id_of_file = root_folder[4].name
rr = root_folder[4].id
print(id_of_file)

root_folder = client.item(drive='me', id=rr).children.get()
id_of_file = root_folder[1].name
rr = root_folder[1].id
print(id_of_file)

root_folder = client.item(drive='me', id=rr).children.get()
id_of_file = root_folder[1].name
BN = root_folder[1].id
print(id_of_file)

id_of_file = root_folder[0].name
Alda = root_folder[0].id
print(id_of_file)
print(Alda)
'''

def Find_ID(str):
    str_array = str.split("/")
    root = "root"
    root_folder_array = client.item(drive='me', id=root).children.get()
    for folder in str_array:
        for root_folder in root_folder_array:
            if (root_folder.name == folder):
                root = root_folder.id
                if (folder == str_array[-1]):
                    return root_folder.id
                root_folder_array = client.item(drive='me', id=root).children.get()
                break

#print(Find_ID("Uni/Info/Alda"))
        
try:
    id_OneDrive = Find_ID(location)
    print("found location: id = " + id_OneDrive)
except:
    print("did not find location")

try:
    returned_item = client.item(drive='me', id=id_OneDrive).children[uploadname].upload_async(filename)
    print("upload done")
except Exception as e:
    print("upload failed:")
    print(e)
