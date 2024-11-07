'''
Runs converted curl request as Python

#Uses requests to run converted curl request in Python

--- upload doi for multiple neurons ---
Requires:
1. Reserved (but not published) DOIs from create_and_publish.py
2. List of Neurons by AA-id (eg, AA1234)
    -should be copied over from create_and_publish.py  
    TODO: this should be one private variable that applies to the whole package... fix this!


'''

import pip._vendor.requests as requests

#same as sampleIds
brain_id = '' # alphanumeric uuid of brain
neuron_list = [] #TODO: delete this later
url = '' #url to MNB backend

def missingDOIs(brain_id_num):
    print("Looking for missing dois")
    query = 'query {neurons(input:{sampleIds:"' + brain_id_num + '"}){items {id idString doi}}}'

    headers = {
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': url, #MNBDB url here
    }


    json_data = {
        'query' : query
    }


    response = requests.post(url+'/graphql', headers=headers, json=json_data)
    #data = response.text


    #parse data to get dictionary of neurons in the brain
    data_json = response.json()
    data_list = data_json['data']['neurons']['items']

    print(response)
    #neurons
    #for x in range(0, len(data_list)):
    #    print(data_list[x]['idString'])


    #find neurons missing a doi
    missing_doi_dict = {}
    for x in range(0, len(data_list)):
        if data_list[x]['doi'] is None:
            #print(data_list[x]['idString'] + " is missing a doi.")
            missing_doi_dict[data_list[x]['idString']] = data_list[x]['id']

    #print(missing_doi_dict)
    return missing_doi_dict

#This one (below) no longer needed          
def process_neurons_dict(missing_dois_dict):
    for k, v in missing_dois_dict.items():
        neuron_list.append(k)
    return neuron_list
    #print(neurons_list)

def upload_dois(data_dict):
    #accepts a dict / list of neuron ids (long alpha-num things)
    #submits Database mutation to update each neuron

    # assume format =  data_dict[neuron] = [new_article_id, doi_res, neuron_id]

    for k, v in data_dict.items():
        doi = v[1]
        neuron_id = v[2]
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Connection': 'keep-alive', 'DNT': '1', 'Origin': url}
        query = 'mutation {\n  updateNeuron(neuron: {id: "' + neuron_id + '", doi: "' + doi + '" }) {\n    source {\n      doi\n    }\n    error\n  }\n}\n  \n'
        json_data = {'query' : query}
        response = requests.post(url+'/graphql', headers=headers, json=json_data)
        print(response)  



#def get_neuron_ids():
    


#dicty = missingDOIs("brain id alpha-num")
#print(neuron_list)
#process_neurons_dict(dicty)
#print(neuron_list)
#TODO: have an "overall process" file that...
# 1. move "if name == main" over to it
# 2. calls this doi stuff by doing: mnb_graphQL_queries.missingDOIs("doi_number"), which will return the missing doi dictionary
#TODO: run this again with url and make sure it works
#TODO: function to reset dois to null (for testing only)

