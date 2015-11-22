-- nodeMCU Lua Code for esp8266
-- Config:
IP     = "192.168.0.53"
PORT   = 80
REQUEST= "/cgi-bin/state.py"
TIME   = 20*1000   -- every 20s a request is made

RED = 4
GREEN = 3
-- END Config

gpio.mode(RED,gpio.OUTPUT)
gpio.mode(GREEN,gpio.OUTPUT)

function doRequest()
    if (conn ~= nil) then
        conn:close()
        conn = nil
    end
    conn=net.createConnection(net.TCP, 0) 
    conn:on("receive", function(conn, payload)
        --tmr.wdclr() 
        if string.find(payload, "build:__green__") ~= nil then
                an(GREEN)
                aus(RED)
        elseif string.find(payload, "build:__red__") ~= nil then
                an(RED)
                aus(GREEN)
        else
                an(RED)
                an(GREEN)
        end
        conn:close() 
    end)
    conn:connect(PORT,IP) 
    conn:send("GET http://"..IP..REQUEST.." HTTP/1.1\r\n") 
    conn:send("Host: logger\r\n") 
    conn:send("Accept: */*\r\n") 
    conn:send("User-Agent: Mozilla/4.0 (compatible; esp8266 Lua; Windows NT 5.1)\r\n")
    conn:send("\r\n")
    conn:on("disconnection", function(conn)
          --print("Got disconnection...")
         conn=nil
    end)
end

function an(led) gpio.write(led, gpio.LOW) end
function aus(led) gpio.write(led, gpio.HIGH) end

an(RED)
an(GREEN)
print("tmr.alarm(0, TIME, 1, doRequest)")
tmr.alarm(0, TIME, 1, doRequest)
