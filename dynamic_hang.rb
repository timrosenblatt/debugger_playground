class RipVanWinkle
  def call
    sleepy
  end

  def sleepy
    while true
      step1
      step2
      step3
      step4
      step5
    end
  end

  def step1
    puts "step 1"
    sleep 1
  end

  def step2
    puts "step 2"
    sleep 1
  end

  def step3
    puts "step 3"
    sleep 1
  end

  def step4
    puts "step 4"
    sleep 1
  end

  def step5
    puts "step 5"
    sleep 1
  end
end

puts "PID is #{Process.pid}"
