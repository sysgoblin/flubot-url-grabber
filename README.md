## flubot-url-grabber

<p align="center">
  <img width="446" height="558" src="https://i.imgur.com/VILZhRN.png">
</p>

This script will continually hit the provided flubot lure URL to enumerate and collect unique download URLs or domains, based on the provided arguments.

## Examples
```bash
$ python3 grabber.py -u http://exmaple.com/pkg/?2gfv5gfdbavg

https://www.domain1.com/xyz/?zwd3v4vu32v4rivvt3fz75eyysb7baxxut677n74wkl5hhnxrlki...
https://kf.domain2.com/xyz/?el4fldk3ufclotokog2hbc3xxnwia34ijobbbsatzv4ky4wimwvw3...
https://domain3.ir/xyz/?fiwv2wctorggeri7pfqxqxt7nzsfkzyyinlrqhi3dbyhs6q5nv7gkfdbp...
```
Output unique full URLs collected from the provided URL.

```bash
$ python3 grabber.py -u http://exmaple.com/pkg/?2gfv5gfdbavg -p ./out.txt --domain-only

https://domain1.net
https://www.domain2.com
https://domain3.com.vn
```
Output unique domains collected from the provided URL, and also save to the file `out.txt`

