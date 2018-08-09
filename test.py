import cdn_api_client

username   = 'YOUR_API_USERNAME';
password   = 'YOUR_API_PASSWORD';
cdn_id     = 'YOUR_CDN_SERVICE_ID';

if __name__ == '__main__':
    client = cdn_api_client.CDNsunCdnApiClient({ 'username': username,
                                                 'password': password })
                                                 
    response = client.get({ 'url': 'cdns' })
    print(response)

    response = client.get({ 'url': 'cdns/' + str(cdn_id) + '/reports',
                            'data': { 
                                'type':   'GB',
                                'period': '4h'
                            }
                          })
    print(response)

    response = client.post({ 'url': 'cdns/' + str(cdn_id) + '/purge',
                              'data': {
                                  'purge_paths': [
                                        '/path1.img',
                                        '/path2.img'
                                   ]
                              }
                            })
    print(response)
    
    response = client.get({ 'url': 'cdns/' + str(cdn_id) })
    print(response)    
