# This class will generate a few method calls so that you can have a slightly
# deeper stack trace
class RipVanWinkle
  def call
    sleepy
  end

  def sleepy
    you_are_getting_sleepy
  end

  def you_are_getting_sleepy
    actual_hang
  end

  def actual_hang
    some_variable = "the value"
    sleep 1_000_000
  end
end

puts "PID is #{Process.pid}"
