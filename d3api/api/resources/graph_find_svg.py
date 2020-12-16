def get_svg_url(arg_type):
    if arg_type == 'D3/POS_µSrv':
        return '/static/dist/SVGs/cube.svg'
    if arg_type == 'D3/POS_K8S':
        return '/static/dist/SVGs/cube2.svg'
    if arg_type == 'D3/POS_POS':
        return '/static/dist/SVGs/cash-register2.svg'
    if arg_type == 'D3/Store':
        return '/static/dist/SVGs/warehouse.svg'
    if arg_type == 'D3/ESX-Server':
        return '/static/dist/SVGs/uni-erlangen/devices/server.svg'
    if arg_type == 'D3/VMware-VM':
        return '/static/dist/SVGs/016-screen.svg'
    # if arg_type == 'D3/Country':
    #     return '/static/dist/SVGs/warehouse.svg'
    if arg_type == 'D3/IOT_Device':
        return '/static/dist/SVGs/uni-erlangen/devices/server-access.svg'
    if arg_type == 'D3/IOT_Functions':
        return '/static/dist/SVGs/uni-erlangen/logos/otb.svg'
    if arg_type == 'D3/Country':
        return '/static/dist/SVGs/uni-erlangen/status/binational.svg'
    if arg_type == 'D3/CC-Server':
        return '/static/dist/SVGs/uni-erlangen/devices/server-multiple.svg'
    if arg_type == 'D3/CC-VM':
        return '/static/dist/SVGs/016-screen.svg'
    if arg_type == 'D3/DC-Room':
        return '/static/dist/SVGs/room01.svg'
    if arg_type == 'D3/DC-Datacenter':
        return '/static/dist/SVGs/dc-computer.svg'
    if arg_type == 'D3/DC-Location':
        return '/static/dist/SVGs/global.svg'

    # print("unknown arg_type: '{}'".format(arg_type))
    return '/static/dist/SVGs/uni-erlangen/status/important.svg'
