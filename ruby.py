# Blatantly stolen from https://christoph.luppri.ch/articles/ruby/debugging-ruby-programs-on-osx-with-lldb/

import lldb

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f ruby.rb_backtrace rb_backtrace')
    debugger.HandleCommand('command script add -f ruby.rb_eval rb_eval')
    debugger.HandleCommand('command script add -f ruby.redirect_stdout redirect_stdout')

# This calls the internal ruby backtrace methods which output to stderr
# TODO redirect stderr as well. For now I just use `rb_eval "caller"`
def rb_backtrace(debugger, command, result, internal_dict):
    debugger.HandleCommand('expr (void)rb_backtrace()')

# Call as `rb_eval "puts 'hello world'"`
def rb_eval(debugger, command, result, internal_dict):
    debugger.HandleCommand('expr (void *)rb_p((void *)rb_eval_string_protect(%s, (int *) 0))' % command)

def redirect_stdout(debugger, command, result, internal_dict):
    debugger.HandleCommand("""call (void)rb_eval_string("$_old_stdout, $stdout = $stdout, File.open('/tmp/ruby-debug.' + Process.pid.to_s, 'a'); $stdout.sync = true")""")
