
### STRATEC ROCKET CHALLENGE

<b>ok, this was amazing<b/> , so cosidering I didn't make it 'till Monday I wanted to go a little extra (astronomical) mile, feeling I had to

<iframe width="1398" height="521" src="https://www.youtube.com/embed/dKbWgRBDZV4" title="🚀Planet Animations gif🚀 🧑‍🚀🧑‍🚀 😎😎🤓" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

#### running it:
```bash
#yes, twice
cd soft_challange/soft_challange
```

so `pwd` returns somehting like `/path/to/soft_challange/soft_challange`
then

```bash
pip install -r requirements.txt
flask --app . run
```
and now you can access the app through your localhost or 127.000 or whatever


<br>
<br>



In the homepage you can drag and drop files for each stage of the problem (don't judge okay, I know it looks goofy)

![screenshot](pics/homepage.png)

<br>

##### The simplest way to use it is to just upload planetary data (computes stage 1)
![screenshot](pics/just-planetary-data.png)

#### Then you can also upload rocket data (computes stage 2)
![screenshot](pics/rocket-data.png)

#### Now the fun, does indeed begin. This is the output for uploading all three, planetary, rocket *and* solar system data
![screenshot](pics/solar-system-data.png)
<br>

##### And just below are the options for all other stages:
![screenshot](pics/results-options.png)

#### I'll start with the last one: the angular positions of the planets after 365 days passing from them being aligned
![screenshot](pics/angle-positions.png)

obviously, earth is aligned again