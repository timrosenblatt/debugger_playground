# Ruby Debugging Playground!

## Background

On Linux, `gdb` is the best option for debugging a running process.

At the moment, there's a [fairly widespread issue with gdb on OSX](https://github.com/Homebrew/homebrew-core/issues/20047) where [gdb is tied to dyld v14 but newer versions of OSX are on dyld v15](https://sourceware.org/bugzilla/show_bug.cgi?id=20981). So, `lldb` (which comes with OSX) is the alternative.

There is a `static_hang.rb` file in this repo. You can invoke it with `ruby -e "require './static_hang'; RipVanWinkle.new.call"`

There is also `dynamic_hang.rb` which can be similarly invoked.

# General process information

On Linux, `top -p THE_PID`, and on OSX `top -pid THE_PID`, will let you check on a specific process. If it's using 100% CPU, that tells you something different than if it is using 0% CPU. If it's at 0%, it might be waiting on some kind of network call/DB call/etc.

# General GDB notes

You need the PID and your Ruby path to connect GDB to this process with `gdb /your/ruby/path PID`. I'm using rbenv so I run `rbenv which ruby`. YMMV.

Thanks to [Jon Yurek (and Rasmus before him)](https://robots.thoughtbot.com/using-gdb-to-inspect-a-running-ruby-process) we have some simple GDB functions that are helpful. When you are in the GDB prompt, just paste them in to define them (they can also be put in ~/.gdbinit). Then, run `redirect_stdout` to start, then you can use `ruby_eval('Kernel.caller')` to run arbitrary Ruby code.

```
define redirect_stdout
  call rb_eval_string("$_old_stdout, $stdout = $stdout, File.open('/tmp/ruby-debug.' + Process.pid.to_s, 'a'); $stdout.sync = true")
end

define ruby_eval
  call(rb_p(rb_eval_string_protect($arg0,(int*)0)))
end
```

One note: the `Process.pid.to_s` will be the GDB process's PID, and not your Ruby process's PID.

(BTW thanks to [this](https://github.com/Homebrew/homebrew-core/issues/2730) I realized I had to run `pip install six` inititally. YMMV)

# Debugging with LLDB

Run `lldb` and attach it to the process with `attach THE_PID_GOES_HERE`

I have [a few LLDB macros methods](https://christoph.luppri.ch/articles/ruby/debugging-ruby-programs-on-osx-with-lldb/) in `ruby.py`. Load it with `command script import ruby.py`

By default, these all output to stdout, and if you're debugging a process on a running server, you won't have access to that, so you should redirect stdout to a file and tail it with `redirect_stdout`

You can start and stop the process:
- `process continue`
- `process interrupt`

When you're done you can run `kill` to terminate the process. `quit` will get you out of lldb.

# Resources

- https://blog.newrelic.com/2013/04/29/debugging-stuck-ruby-processes-what-to-do-before-you-kill-9/
- https://lldb.llvm.org/lldb-gdb.html
- https://lldb.llvm.org/tutorial.html
- https://github.com/altkatz/hijack-lldb
