# AppleSupport Intent Discovery Report

## 1. Data Extraction
Conversations were extracted by finding AppleSupport tweets and identifying the root tweet in the `in_response_to_tweet_id` chain. A total of 81481 conversations were formed.

## 2. Filtering Signals
Flags were added for short messages, closures, DM requests, and generic templates. Data was not deleted.

## 3. Candidate Selection
Using length and non-generic patterns, 80470 candidate conversations were selected.

## 4. Theme Discovery
TF-IDF and NMF (Non-negative Matrix Factorization) were used to discover candidate themes.

## 5. Candidate Theme Frequencies
- **115858 | 115858 applesupport | shit | applesupport 115858 | wtf**: 8528 candidates
- **iphone | applesupport iphone | plus | 6s | iphone 6s**: 8296 candidates
- **ios | 11 | ios 11 | applesupport ios | applesupport ios 11**: 8157 candidates
- **applesupport | just | thanks | applesupport applesupport | thank**: 7799 candidates
- **phone | updated | applesupport phone | updated phone | freezing**: 7531 candidates
- **update | new | new update | ios update | new ios**: 7043 candidates
- **fix | 115858 fix | applesupport fix | glitch | shit**: 7040 candidates
- **https | applesupport https | applesupport | 115858 https | 115858 applesupport https**: 6773 candidates
- **apple | music | apple music | watch | store**: 6082 candidates
- **help | applesupport help | need | help applesupport | help https**: 5077 candidates
- **battery | life | battery life | ios11 | draining**: 5034 candidates
- **question | mark | question mark | box | letter**: 3110 candidates

## 6. Representative Examples
### applesupport | just | thanks | applesupport applesupport | thank
**Customer**: @AppleSupport your c/s sucks, I was just disconnected after waiting on hold for 45+ minutes

**Support**: @356770 That's not the experience we want you to have. Tell us in DM what's going on so we can determine the best support for you today. https://t.co/GDrqU22YpT

### fix | 115858 fix | applesupport fix | glitch | shit
**Customer**: CANT STAND THOSE DAMN SQUARES, @115858 . Y’all need to fix that shit.

**Support**: @356753 Let us know via DM the device you are experiencing this on and with which version of the iOS, then we can advise from there. https://t.co/GDrqU22YpT

### https | applesupport https | applesupport | 115858 https | 115858 applesupport https
**Customer**: @AppleSupport explain yourself. https://t.co/356zUHKRCF

**Support**: @356751 Thanks for reaching out to us for support. We would love to help you. Please DM us so that we can look into this together. https://t.co/GDrqU22YpT

### ios | 11 | ios 11 | applesupport ios | applesupport ios 11
**Customer**: @357005 @AppleSupport Had that problem too, lemme know the remedy | @AppleSupport after updating to iOS 11.0.3, my iPhone 7 will randomly freeze on any app/screen. The buttons won’t even work

**Support**: @566132 We'd be happy to take a look!  Let us know in DM what model iPhone and what country you're in and we'll go from there: https://t.co/GDrqU22YpT | @357005 We'd like to look into appropriate options for your region. DM your current location. https://t.co/GDrqU22YpT

### update | new | new update | ios update | new ios
**Customer**: Wth @115858, I've been clicking "download &amp; install" for almost a week now but the update doesn't want to start download. 🤔 | @AppleSupport Apps weren't a problem, System update was. I was able to download &amp; install the system update via iTunes just after I sent the tweet.

**Support**: @356800 We'd be happy to help you get your apps updated. Have you tried another Wi-Fi network? Please DM us your device and version of OS: https://t.co/GDrqU22YpT | @356800 Got it. Thanks for clarifying! We're glad that it's all worked out. If you need anything else, just let us know. Have a great day.

### phone | updated | applesupport phone | updated phone | freezing
**Customer**: Why is shit popping up as questions marks on my phone?? What’s going on @AppleSupport

**Support**: @356766 We're here to help. DM us which model of iPhone and version of the operating system you're using and we'll get started. https://t.co/GDrqU22YpT

### 115858 | 115858 applesupport | shit | applesupport 115858 | wtf
**Customer**: FUCK YOU @115858 &amp; @123765! NOW I️ CAN’T TWEET THE LETTER I️?!

**Support**: @356764 Hello, thanks for reaching out about this. DM us with which device and iOS version you’re using and we’ll continue there. https://t.co/GDrqU22YpT

### question | mark | question mark | box | letter
**Customer**: I’m so tired of these question mark boxes on my TL. Get your shit together  @115858 @AppleSupport

**Support**: @356755 We'd be happy to look this over with you. Please meet us in DM so we may gather information, and better assist. https://t.co/GDrqU22YpT

### iphone | applesupport iphone | plus | 6s | iphone 6s
**Customer**: @AppleSupport my iPhone X keeps getting a "Could Not Activate iPhone" error. Is the activation server down? | @AppleSupport That was hectic, but I’m all set. Thanks guys!

**Support**: @356773 Congrats on the new iPhone X! These steps can help with Activation issues: https://t.co/cJ57VP3gxT
DM us if still an issue. https://t.co/GDrqU22YpT

### battery | life | battery life | ios11 | draining
**Customer**: @AppleSupport any way to check overall battery health of my iPhone 7?

**Support**: @356799 We appreciate you reaching out!  We've received your DM and will continue with you there.

### apple | music | apple music | watch | store
**Customer**: I have the same question Kristi for AT&amp;T. It sounds like it might be an Apple issue. @117735 @AppleSupport https://t.co/UHM3RWZvFK | @AppleSupport @AppleSupport, link not helpful - Issue was getting the Zip, SS# AT&amp;T verification- Is that Apple's Servers or AT&amp;T? #transparency #iphoneX

**Support**: @356787 Hi Martin! Plry activating your device again. If the issue persist, try these steps and DM the result: https://t.co/ywHIZGN4Ac https://t.co/GDrqU22YpT

### help | applesupport help | need | help applesupport | help https
**Customer**: @AppleSupport Can you help with this? | @AppleSupport 11.0.3

**Support**: @356797 Yes, we can. Can you tell us which iOS version you are currently using please? | @356797 Okay. Have you been having this issue since updating to iOS 11.0.3? DM us your response here: https://t.co/GDrqU22YpT

## 7. Limitations
These are automated candidate themes. Some themes may overlap or capture formatting rather than intent. Manual review is required to define the final golden intents.
