from Colors import bcolors
import Global

def Banner():
	print ' _______ '
	print '< HatKey >'
	print ' ------- '
	print '        \   ^__^'
	print '         \  (xx)\_______'
	print '            (__)\\       )\\/\\'
	print '             U  ||----w |' 
	print '                ||     ||'
	print ' '*10 + '--=' + bcolors.OKBLUE + '[' + bcolors.ENDC + bcolors.BOLD + 'KeyLogger' + bcolors.ENDC
	print ' '*7 + '--+--=' + bcolors.OKBLUE + '[' + bcolors.ENDC + 'Version : ' + bcolors.OKGREEN + bcolors.BOLD + Global.VERSION + bcolors.ENDC + bcolors.ENDC	
	print ' '*7 + '--+--=' + bcolors.OKBLUE + '[' + bcolors.ENDC + 'Coder   : ' + bcolors.OKGREEN + bcolors.BOLD + Global.CODER + bcolors.ENDC + bcolors.ENDC	
	print ' '*10 + '--=' + bcolors.OKBLUE + '[' + bcolors.ENDC + 'github  : ' + bcolors.OKGREEN + bcolors.BOLD + Global.GITHUB + bcolors.ENDC + bcolors.ENDC	
	print ' \n'