"""
A script to modify and publish a private article based on Mouselight.
Uploads json and swc files. 
Articles are private before being made public. Run this script with -t and your production token.
Currently the stage URL is hard-coded into the script, so doesn't work for stage.
"""

import pip._vendor.requests as requests
import argparse
import json
import sys
import hashlib
import os

CHUNK_SIZE = 10 * (1024 ** 2) # e.g. 10 * (1024 ** 2) = 10 Mb.
base_url = "https://api.figshare.com/v2/account/articles" #TODO: use --stage flag instead of hard-coding; Also, "https://api.figsh.com/v2/account/articles" = stage
data_dict = {'AA1614': ['28087673', '10.25378/janelia.28087673', '30853bdc-e3f3-4f5b-a3c8-351b530b1dd2']}

#root = r'U:\Documents\MouseLight\database_copy' #Where the swc and json files from the MNB are located
root = r'Z:\neuron-database\export\CCFv3'
swcs = "swc30"
jsons = "json30"


def checkOK(response_to_check):
    if not response_to_check.ok:
        print(f"Request failed with error code {response_to_check.status_code}")
        print(response_to_check.text) 
        sys.exit()

def initiate_new_upload(url, headers, article_id, file_name, neuron_name):
    endpoint = '{}/{}/files'.format(url, article_id)
    md5, size = get_file_check_data(file_name)
    file_data = {'name': neuron_name,'md5': md5, 'size': size}
    upload_response = requests.post(endpoint, headers=headers, data=json.dumps(file_data))
    checkOK(upload_response)
    return json.loads(upload_response.content) 

def get_file_check_data(file_name):
    with open(file_name, 'rb') as fin:
        md5 = hashlib.md5()
        size = 0
        data = fin.read(CHUNK_SIZE)
        while data:
            size += len(data)
            md5.update(data)
            data = fin.read(CHUNK_SIZE)
        return md5.hexdigest(), size

def upload_parts(headers, file_info, file_name):
    res = requests.get(file_info['location'], headers=headers)
    checkOK(res)
    up_url, up_token = json.loads(res.content)['upload_url'], json.loads(res.content)['upload_token']
    uploader_service_response = requests.get(up_url, headers = {'Authorization': 'token {}'.format(up_token)} )
    checkOK(uploader_service_response)
    with open(file_name, 'rb') as fin:
        for part in json.loads(uploader_service_response.content)['parts']:
            upload_part(file_info, fin, part, up_url)

def upload_part(file_info, stream, part, up_url):
    udata = file_info.copy()
    udata.update(part)
    udata['upload_url'] = up_url 
    part_url = '{upload_url}/{partNo}'.format(**udata)
    stream.seek(part['startOffset'])
    part_data = stream.read(part['endOffset'] - part['startOffset'] + 1)
    part_res = requests.put(part_url, data=part_data)
    checkOK(part_res)

def returnTitle(n):
    #n = string or neuron_list[index number]
    return f'MouseLight Neuron {n}'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-t', 
                        '--token', 
                        required = True, 
                        help = 'Personal token, most easily obtained through the figshare website.'
                        )
    parser.add_argument('-s', 
                    '--stage', 
                    help = 'If -s is included, script will grab info from the stage environment, not the production environment.',
                    action='store_true' # The store_true option automatically creates a default value of False.
                    )
    parser.add_argument('-id',
                    '--article_id',
                    required = False,
                    help = 'Article ID, which was printed to the terminal at the time of creation.'
                    )
    args = parser.parse_args()


    for neuron, info in data_dict.items():
        pathy = os.path.join(root, swcs, neuron+".swc")
        #print(pathy)
        article_id = info[0]
        doi = info[1]
        
        if os.path.isfile(pathy):
            swc_path = pathy
            json_path = os.path.join(root, jsons, neuron+".json")
            print("files exist!")
        #TODO: what if file does not exist?
        else:
            print("files do not exist!")
            sys.exit()

        headers = {'Authorization': 'token {}'.format(args.token)}
 
        proceed = "y"
        while True:
            #proceed = input(f"Would you like to upload a file to the article you just created? (y/n): ")
            
            if proceed.lower() == "y":
                #upload swc file
                file_info = initiate_new_upload(base_url, headers, article_id, swc_path, neuron+'.swc')
                print("Uploading file ", swc_path, f"in {CHUNK_SIZE/(1024 ** 2)}Mb chunks")
                # Until here we used the figshare API; the following lines use the figshare upload service API.
                upload_parts(headers, file_info, swc_path) # looks like e.g. {'location': 'https://api.figsh.com/v2/account/articles/8417838/files/830411224'}
                # complete the upload
                up_res = requests.post(file_info['location'], headers=headers)
                checkOK(up_res)
                print("Upload successful.")
                
                #upload json file
                file_info = initiate_new_upload(base_url, headers, article_id, json_path, neuron+'.json')
                print("Uploading file ", json_path, f"in {CHUNK_SIZE/(1024 ** 2)}Mb chunks")
                # Until here we used the figshare API; the following lines use the figshare upload service API.
                upload_parts(headers, file_info, json_path) # looks like e.g. {'location': 'https://api.figsh.com/v2/account/articles/8417838/files/830411224'}
                # complete the upload
                up_res = requests.post(file_info['location'], headers=headers)
                checkOK(up_res)
                print("Upload successful.")
                proceed = "n"
            elif proceed.lower() == "n":
                break  # break out of the while loop
            else:
                print("Invalid input. Please enter 'y' to upload a file, or 'n' to cancel.")

        #publish = input(f"Would you like to publish this article now? (y/n): ")
        publish = "y" #new
        if publish.lower() == 'y':
            pub_res = requests.post(f"{base_url}/{article_id}/publish", headers=headers)
            checkOK(pub_res)
            print("Article published successfully.")
        else:
            print("Not publishing at this time.")
print("Done")