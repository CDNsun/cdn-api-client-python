import cdn_api_client

username   = 'u1727107848480985';
password   = 'TtkgDqXmjJd4';
cdn_id         = 29567;

if __name__ == '__main__':
    client = cdn_api_client.CDNsunCdnApiClient({ 'username': username,
                                                         'password': password })
    response = client.get({ 'url': 'cdns' })
    print('test1')    
    print(response)

    response = client.get({ 'url': 'cdns/' + str(cdn_id) + '/reports',
                            'data': { 
                                'type': 'GB',
                                'period': '4h'
                            }
                          })
    print('test2')   
    print(response)

    response = client.post({ 'url': 'cdns/' + str(cdn_id) + '/purge',
                              'data': {
                                  'purge_paths': [
                                        '/path1.img',
                                        '/path2.img'
                                   ]
                              }
                            })
    print('test3')      
    print(response)
    

    response = client.get({ 'url': 'cdns/' + str(cdn_id) })
    print('test4')       
    print(response)

    response = client.put({ 'url': 'cdns/29567', 
                            'data': { 
                                'cdn': {
                                    'service_domain': 'oidoi32joid23x.mycompany.com', 
                                    'location_ids': [4, 7, 8, 10, 11, 13, 14, 16, 19, 23, 26, 31, 34, 39, 41, 42, 44, 45, 46, 48, 50, 55, 58, 59, 63, 65, 69, 74, 77, 87, 88, 99, 104, 129, 130, 260, 344, 351, 358, 365, 372, 386, 400, 414, 421, 477, 500, 501, 502] 
                                }
                            } 
                          })
    print('test5')       
    print(response)
