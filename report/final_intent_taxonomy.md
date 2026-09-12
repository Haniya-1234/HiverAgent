# Final AppleSupport Intent Taxonomy

## Intent 1
**Name**: iOS Update/Installation Issue
**Definition**: Customer is experiencing problems downloading, installing, or starting an iOS update on their device.
**Include**: Messages about updates failing, stuck downloads, installation errors, or insufficient storage for an update.
**Exclude**: Messages about bugs/issues that occurred *after* an update was successfully installed (e.g., battery drain after update).
**Approximate candidate volume**: 1,206
**Why this is useful**: Allows an AI agent to immediately provide troubleshooting steps for network issues, storage management, or iTunes update methods instead of generic device troubleshooting.
**5 real examples**:
1. `Can't update iPhone software, restarted phone and reconnected internet still not working @AppleSupport https://t.co/FpCg3Qr5i2`
2. `I have a 16gb iPhone 6s. I need to do an update (1.33gb). @115858 explain why I can't update my phone? https://t.co/IsPsf5nqq8`
3. `Wth @115858, I've been clicking "download &amp; install" for almost a week now but the update doesn't want to start download. 🤔`
4. `@AppleSupport I was able to download &amp; install the system update via iTunes just after I sent the tweet.`
5. `@AppleSupport Apps weren't a problem, System update was.`

## Intent 2
**Name**: Device Freezing/Unresponsive
**Definition**: Customer's iPhone, iPad, or Mac is lagging, freezing, or becoming completely unresponsive to touch or buttons.
**Include**: Complaints about random freezing, buttons not working, lagging screens, or slow device performance.
**Exclude**: Apps crashing (closing unexpectedly) without freezing the entire device.
**Approximate candidate volume**: 6,774
**Why this is useful**: Freezing issues usually require hard reset instructions or storage management tips, which an AI agent can quickly provide based on the device model.
**5 real examples**:
1. `@AppleSupport updated my phone the other day and it keeps freezing so I have to restart it. Then it’s really slow. Sort it out.`
2. `@AppleSupport after updating to iOS 11.0.3, my iPhone 7 will randomly freeze on any app/screen. The buttons won’t even work`
3. `@AppleSupport IOS update is a total disaster / phone freezing constantly .... battery draining faster than before.`
4. `@115858 this new phone software is making my phone slow and glitchy!  Not impressed!`
5. `@AppleSupport I have already send my diagnosis reports in past but nothing seems to working with this iOS 11.0.3 update. Each day 7Plus getting slower`

## Intent 3
**Name**: Battery Drain/Health
**Definition**: Customer is experiencing poor battery life, fast battery drain, or wants to check their battery health.
**Include**: Messages about the battery dying quickly, phones shutting off with battery remaining, or questions about battery health status.
**Exclude**: Issues where the phone will not turn on at all or won't charge (hardware issue).
**Approximate candidate volume**: 7,695
**Why this is useful**: Highly common issue; an AI agent can provide battery-saving tips or instructions on how to check battery health and usage in settings.
**5 real examples**:
1. `@AppleSupport any way to check overall battery health of my iPhone 7?`
2. `@AppleSupport Please. Let the people in charge of the updates to fix the battery issue. Last two iOS updates worsen the battery life.`
3. `Well ios11 is a swarm of bugs. I literally was stranded in a foreign country because my battery suddenly died. @AppleSupport`
4. `@AppleSupport The battery dies in seconds. I’ve contacted my company IT department and they stated it is a known 11.3 issue.`
5. `@AppleSupport ios 11.0.3 tons of bugs on my iphone 5s, battery drains while charging, no clock or date on lock screen, visual artifacts`

## Intent 4
**Name**: iOS Autocorrect Bug
**Definition**: Customer is complaining about the specific iOS 11 bug where typing the letter "I" autocorrects to an "A" with a question mark symbol/box.
**Include**: References to "question mark boxes", "damn squares", typing "I", or the "A?" symbol.
**Exclude**: General keyboard issues or screen display artifacts unrelated to typing.
**Approximate candidate volume**: 4,284
**Why this is useful**: A known software defect where an AI agent can provide the specific temporary workaround (text replacement) or direct them to update to iOS 11.1.
**5 real examples**:
1. `CANT STAND THOSE DAMN SQUARES, @115858 . Y’all need to fix that shit.`
2. `I’m so tired of these question mark boxes on my TL. Get your shit together  @115858 @AppleSupport`
3. `Why is shit popping up as questions marks on my phone?? What’s going on @AppleSupport`
4. `FUCK YOU @115858 &amp; @123765! NOW I️ CAN’T TWEET THE LETTER I️?!`
5. `@AppleSupport how come the app icons on my Apple Watch come up as blank white squares instead of the actual app icon?` (Note: similar artifact bug on watch)

## Intent 5
**Name**: Device Activation Issue
**Definition**: Customer is unable to activate a newly purchased or restored device.
**Include**: Error messages stating "Could Not Activate iPhone" or issues connecting to the activation server.
**Exclude**: Issues logging into Apple ID if the phone is already activated (which falls under Apple ID Account).
**Approximate candidate volume**: 360
**Why this is useful**: Activation is a critical first-step blocker. An AI agent can quickly verify if activation servers are down or guide the user to activate via iTunes.
**5 real examples**:
1. `@AppleSupport my iPhone X keeps getting a "Could Not Activate iPhone" error. Is the activation server down?`
2. `@AppleSupport I’m continually getting the “Could Not Activate iPhone” message … any updates on when this will be working?`
3. `@AppleSupport I want to activate it via itunes, but when I connect to itunes its error 💆`
4. `@AppleSupport Latest version of iOS. It says a error occurred during activation. Turned phone off and on. Nothing. New phone just set it this evening`
5. `Hey @VerizonSupport @115858 your activation server is still broken, been trying for an hour. https://t.co/TgSbhaMkW6`

## Intent 6
**Name**: Apple Music Playback/Library
**Definition**: Customer is having trouble streaming music, syncing their Apple Music library, or downloading songs.
**Include**: Missing songs, albums splitting, "Add to Library" feature issues, or Apple Music app behavior.
**Exclude**: General iTunes Store billing or purchase issues.
**Approximate candidate volume**: 360
**Why this is useful**: Apple Music requires specific app-level troubleshooting (checking sync library settings, redownloading) rather than device-level fixes.
**5 real examples**:
1. `@AppleSupport Having an issue where Apple Music divides up the albums I have, days after adding them to my library`
2. `@AppleSupport Trying to figure out: I checked off the preference for downloading all music into iTunes but not all music is being downloaded`
3. `@AppleSupport how do I clear songs from the Up Next queue in the Apple Music app on iOS 11?`
4. `Hello why is Snapchat and my Apple Music app messing up? Is this bc the new iPhone is coming out? I’m broke pls help thx @115858`
5. `@AppleSupport Is their any way to pin playlists in Apple Music to the top for easy access? Specifically with CarPlay`

## Intent 7
**Name**: Apple ID / iCloud Account Issue
**Definition**: Customer cannot access their Apple ID or iCloud account due to forgotten passwords, locked accounts, or verification issues.
**Include**: Accounts disabled, forgotten passwords, verification code errors, iCloud storage issues, or Activation Lock.
**Exclude**: Issues simply signing into a specific app if the Apple ID itself is working perfectly.
**Approximate candidate volume**: 3,094
**Why this is useful**: Account issues require security verification. An AI agent can direct users to the iForgot portal or Apple Support account recovery workflows safely.
**5 real examples**:
1. `@AppleSupport Dear iphone. I would like to help my old friend. She lost her phone but when she found it. The phone was locked. Any help?`
2. `locked out of my apple ID bcuz my old phone broke &amp; i had 2 factor authentication on , no one should ever use tht shit @115858`
3. `@AppleSupport hello, I just got an email saying that my apple ID has been disabled. Can you confirm that email? I'm afraid it might be fake.`
4. `@AppleSupport I’m getting the following error when trying to access my Apple ID - iPhone 6s plus (11.0.3).  HELP!!`
5. `@AppleSupport help I logged out of my Apple ID account and the verification code is sent to a broken phone????`

## Intent 8
**Name**: Wi-Fi / Bluetooth Connectivity
**Definition**: Customer is unable to maintain a stable Wi-Fi or Bluetooth connection with their device.
**Include**: Wi-Fi dropping, Bluetooth disconnecting, unable to pair accessories, or control center toggles not working.
**Exclude**: Cellular data or carrier signal issues (No Service).
**Approximate candidate volume**: 3,226
**Why this is useful**: Connectivity troubleshooting has standard steps (forget network, reset network settings) that an AI agent can perfectly handle.
**5 real examples**:
1. `@115858 if my screen say poor connection does that mean my wifi is messed up or theres? cause i tired of having this argument erry night 😭💯`
2. `@AppleSupport enfia no cu essa atualização maldita que fica ligando o Wi-Fi sozinho`
3. `@AppleSupport Bluetooth suddenly turns off automatically while streaming on wireless speaker on iPhone 8 plus. Happens several time.`
4. `@AppleSupport On iPhone Bluetooth turns off and immediately turns on automatically and try’s to reconnect with speaker.`
5. `@115858 @AppleSupport Sigo sin ver los beneficios del nuevo IOS... batería se descarga el doble, apps se cuelgan y wifi no funciona bien`

## Intent 9
**Name**: App Crashing/Closing
**Definition**: Specific applications are quitting unexpectedly, returning to the home screen, or failing to open.
**Include**: 3rd party apps or native apps crashing.
**Exclude**: The entire phone rebooting or freezing completely (Device Freezing).
**Approximate candidate volume**: 1,561
**Why this is useful**: Usually resolved by updating the specific app, reinstalling the app, or contacting the app developer. An AI agent can quickly guide users through these steps.
**5 real examples**:
1. `@188 app is constantly crashing on #iOS11 @AppleSupport @115858 Haptic feedback is still not working even in 11.0.3 on my 7Plus #apple`
2. `@AppleSupport Here is a screen capture. If the note is lengthy then refresh isn’t happening properly. And the note app was crashing yesterday.`
3. `@115858 why does my 8+ crash and freeze multiple time per day? ITS TWO WEEKS OLD YA DUMB FUCKS`
4. `Seriously getting fed up with @AppleSupport now. Had to hard reset my phone 5 times in the last day as it keeps crashing 😒`
5. `@36518 hello. Is there problem with @6716 and new @115858 update? Mine kept crashing this morning on watch and didn’t register run.`

## Intent 10
**Name**: Hardware / Physical Damage
**Definition**: Customer's device has sustained physical hardware damage such as a broken screen or water damage.
**Include**: Cracked screens, shattered glass, bent phones, physical buttons broken off.
**Exclude**: Software glitches displaying visual artifacts on a physically intact screen.
**Approximate candidate volume**: 180
**Why this is useful**: Hardware damage cannot be fixed via chat. An AI agent can immediately transition to helping the user book a Genius Bar repair appointment.
**5 real examples**:
1. `@115858 My iPad is broken screen is broken on and glass broken`
2. `I just cracked my phone in the stupidest way possible!!!!!! Why do you make these things so easy to crack!!!!!! @115858`
3. `@AppleSupport My iPhone 7 screen has accidentally cracked :( What should I do? Plz help.`
4. `@AppleSupport phone fell from 0.5 metres and front screen shattered - how is it the strongest ever ? Replace it free ?? Where in Gurgaon?`
5. `@115858 yall cracked tf out of my phone w ios 11. it just doesnt work right anymore` (Note: users sometimes use "cracked" metaphorically, but true physical damage queries exist).

## OTHER_UNCLEAR
**Name**: Other / Unclear
**Definition**: Use when the customer's problem cannot be confidently mapped to any of the 10 intents from the available context. This should NOT be treated as a technical support intent. It is an evaluation fallback class.

---

## Taxonomy Design Decisions

When moving from Phase 2 (Automated Theme Discovery) to Phase 3 (Final Taxonomy), significant manual review and refinement occurred. The automated NMF and TF-IDF themes identified structural clusters, but many were noisy or overlapping.

**Rejected Themes**:
- **"115858 | 115858 applesupport | shit | wtf"**: This theme was highly prevalent but entirely noisy. "115858" is an anonymized user mention (likely @Apple). "Shit/wtf" are expressions of frustration. These are not actionable intents.
- **"https | applesupport https | applesupport"**: This simply captured conversations where the user or agent included a URL, which spans across all possible intents.
- **"help | applesupport help | need"**: An overly broad category ("General Help"). Customers saying "I need help" do not provide enough context to formulate a specific troubleshooting path.

**Merged Themes**:
- The themes for **"ios | 11 | ios 11"**, **"iphone | plus | 6s"**, and **"phone | updated | freezing"** heavily overlapped. Many complaints were about the exact same issue: device lagging or freezing after the iOS 11 update. These were merged and refined into the single intent **"Device Freezing/Unresponsive"**.
- The themes for **"115858 | shit | wtf"** and **"question | mark | box | letter"** were both heavily populated by the exact same viral iOS 11 autocorrect bug ("I" changing to "A?"). We created a specific, highly actionable intent: **"iOS Autocorrect Bug"**.

**Split Themes**:
- The broad concept of "Apple problems" or "Apple Music/Store" was split into more actionable sub-components. For example, **"Apple Music Playback/Library"** was separated from general Apple ID login issues, because the troubleshooting steps are vastly different (sync settings vs. account security recovery).

---

## Labeling Guidelines

These guidelines are meant for human annotators when reviewing the golden set. Please adhere strictly to these rules to ensure high inter-rater reliability.

1. **Read the entire context**: Review the customer's text carefully. The intent should represent the *root cause* of why the customer is reaching out.
2. **Prioritize specific software/hardware bugs**: If a customer mentions battery drain *and* an app crashing, prioritize the one that seems to be the primary complaint or the blocker. 
3. **Hardware over Software**: If the user has a cracked screen but also mentions the touch isn't working, classify as **Hardware / Physical Damage** because physical repair is required first.
4. **Identify the iOS Autocorrect Bug**: Look for mentions of "question mark", "squares", "letter I", or symbols like "A?". This is a very specific, known defect (**iOS Autocorrect Bug**).
5. **Differentiate Freezing vs. Crashing**:
   - If the *entire phone* stops responding to touch/buttons or reboots: **Device Freezing/Unresponsive**.
   - If a *specific application* closes unexpectedly but the phone is otherwise fine: **App Crashing/Closing**.
6. **Unknown or Unclear**: If a message does not contain enough information to confidently assign one of the 10 technical intents, label it OTHER_UNCLEAR rather than guessing.
7. **Do not use sentiment as an intent**: A customer being angry or using profanity does not change the technical intent of their issue. Focus purely on the technical problem.
