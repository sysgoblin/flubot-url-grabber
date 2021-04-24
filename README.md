## flubot-url-grabber

<p align="center">
  <img width="446" height="558" src="https://i.imgur.com/VILZhRN.png">
</p>

This script will continually hit the provided flubot lure URL to enumerate and collect unique download URLs or domains, based on the provided arguments.

## Setup
**Step 1**: Clone the repo
```
git clone https://github.com/sysgoblin/flubot-url-grabber.git
```
**Step 2**: cd in to the repo folder
```
cd flubot-url-grabber/
```
**Step 3**: Install the requirements (python 3.6+)
```
pip3 install requirements.txt
```

## Usage
Required arguments:
```
-u --url        URL to collect from

OR

-i --input      List of newline delimited URLs to collect from
```

Optional arguments:
```
-p --path       Path of output file to save collected URLs/domains

--domain-only   Return domains only, not full URLs
```

## Examples
Output unique full URLs collected from the provided URL.
```
$ python3 grabber.py --url http://exmaple.com/pkg/?2gfv5gfdbavg

https://www.domain1.com/xyz/?zwd3v4vu32v4rivvt3fz75eyysb7baxxut677n74wkl5hhnxrlki...
https://kf.domain2.com/xyz/?el4fldk3ufclotokog2hbc3xxnwia34ijobbbsatzv4ky4wimwvw3...
https://domain3.ir/xyz/?fiwv2wctorggeri7pfqxqxt7nzsfkzyyinlrqhi3dbyhs6q5nv7gkfdbp...
```

Output unique domains collected from the provided URL, and also save to the file `out.txt`
```
$ python3 grabber.py -u http://exmaple.com/pkg/?2gfv5gfdbavg -p ./out.txt --domain-only

https://domain1.net
https://www.domain2.com
https://domain3.com.vn
```

Iterate over provided URLs within input.txt (newline delimited) and print all unique domains collected
```
$ python3 grabber.py -i input.txt --domain-only

https://domain1.net
https://www.domain2.com
https://domain3.com.vn
```


