from gbxremote import DedicatedRemote
import os

HOST = 'localhost'
PORT = 5000
USERNAME = 'SuperAdmin'
PASSWORD = 'SuperAdmin'

#############################

remote = DedicatedRemote(HOST, PORT, USERNAME, PASSWORD)

if not remote.connect(1):
    print('Connection failed.')
else:
    print('Connected!')

# get method info
methods = remote.call('system.listMethods')
methodSignCalls = [['system.methodSignature', method] for method in methods]
methodHelpCalls = [['system.methodHelp', method] for method in methods]

methodSignatures = remote.multicall(*methodSignCalls)
methodHelps = remote.multicall(*methodHelpCalls)

def renderSignature(method, args):
    result = ''

    result += '<em>%s</em> ' % args[0]
    result += '<b>%s</b>' % method
    result += '('
    result += '%s' % ', '.join(args[1:])
    result += ')'

    return result

output = ''

# render reference table
output += '<figure class="table">'
output += '<table>'
output += '<thead>'
output += '<tr>'
output += '<th><strong>Signature<br><small style="font-family:Consolas">%s</small></strong></th>' % renderSignature('methodName', ['returnType', 'arg1', 'arg2', '...'])
output += '<th><strong>Description</th>'
output += '</tr>'
output += '</thead>'
output += '<tbody>'

for i in range(len(methods)):
    method = methods[i]
    methodSignature = methodSignatures[i][0][0]
    methodHelp = methodHelps[i][0]

    output += '<tr>'
    output += '<td style="font-family:Consolas">%s</td>' % renderSignature(method, methodSignature)
    output += '<td>%s</td>' % methodHelp
    output += '</tr>'

output += '</tbody>'
output += '</table>'
output += '</figure>'

# generate & render version info
version = remote.call('GetVersion')
output += '<br><div style="text-align:center;font-family:Consolas;font-size:12px;color:#7a7a7a;">'
output += '<em>This reference is auto-generated, version information:</em>'
output += '<br>'
output += 'Game: <b>%s</b>' % version['Name']
output += ' | Titlepack: <b>%s</b>' % version['TitleId']
output += ' | Version: <b>%s</b>' % version['Version']
output += ' | Build: <b>%s</b>' % version['Build']
output += ' | API Version: <b>%s</b>' % version['ApiVersion']
output += ' | No. Methods: <b>%d</b>' % len(methods)
output += '</div>'

# save the generated html to file
with open('xmlrpc_methods.html', 'w') as f:
    f.write(output)

print('Output to: %s' % os.path.realpath('xmlrpc_methods.html'))

# close connection & cleanup
remote.stop()
