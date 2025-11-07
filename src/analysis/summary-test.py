import cv2
import requests

ARTICLE = """night was awful. Alright. What the fuck is this? Oh, we're doing the car. Yeah. Yeah.
I want to I want to search cars. I'm gonna say I don't like this map at all either. Yeah.
It's it's it's the map is really fun when you're 15 minutes in but when you're 30 minutes
in at the start, I don't like it. Yeah, there's also no cover. I'm gonna just hit these cars
and pray I don't get shot in the fucking dome ski. Definitely the best looking map though.
Oh, it's so you do it's yeah. So so fucking just like the the alleys and shit that you
can go through as well is really cool. Yeah, yeah, it's well designed. It looks like Italy or
something. I need to get into the garage, which is kind of far. We're gonna have to go through hell.
The garage. What the hell is that? Oh, like not the garage, not like the the tunnels, you know,
what's in the trash can? Yeah, dude, I can't fight down there. There's too much shit going on. I
don't know where I'm going. I know it's awesome. Right? I think I've kind of I've kind of learned
a little bit. So now I know how to get around, which is nice. We made some insane like a lot. Yeah,
we played it a lot yesterday. Made some like really good flank plays. Okay. I got a hairpin. Speak of
the devil. My child was telling me to use it. Or that's a stitcher. Never mind.
Let's go up this hill a little bit. Words extracts.
Industrial batteries are from the cars too, or is that just the motor? I think I think you could
find both. Well, yeah, right? Yeah, maybe I think it's both. I don't know chat shadow.
Rocketeer. God damn it.
The new map comes soon. I wonder what that's gonna be about. November, right? Just the yeah, oh,
right here. Oh, I live. Oh my God. He's right here. He's literally in there.
Running. Nice shots. Nice shots. We don't need to over push. I kind of got fucked up.
They're gonna go get their boy anyways. Oh, you doubt him? Yeah, I don't know. We could go wide left
then. I guess he's somewhere up here. I forgot. D fibs is really bad. Oh, fuck me too. Yeah, I was
not ready. Fine. We'll play. Ready? Rat game. Yeah. Oh, wait, is that? No, no, that's not him.
"""

# URL of the OCR endpoint
OCR_URL = "http://arc_raiders_summary:8000/summarize"

# Send it to the OCR API
response = requests.post(OCR_URL, data=ARTICLE)

# Parse the JSON response
if response.status_code == 200:
    data = response.json()
    print("✅ Summary Results:")
    print(data)
else:
    print("❌ Error:", response.text)
