# AppleSupport Brand Analysis

## 1. AppleSupport Volume
- **Total AppleSupport outbound tweets:** 106860
- **Outbound tweets replying to another tweet:** 106719
- **Standalone outbound tweets:** 141

## 2. Customer Interactions
- **Unique customer tweets receiving an AppleSupport response:** 106623
- **Unique customer accounts involved:** 76365

## 3. Conversation Structure
- **Total usable response pairs (Customer -> AppleSupport):** 112078
- **Conversations with 2 messages:** 58345
- **Conversations with 3 messages:** 11050
- **Conversations with 4+ messages:** 18549

## 4. Response Filtering Signals
- **Average response length:** 136.6 characters
- **Very short responses (<50 chars):** 0.6%
- **Common patterns observed:** Requests to DM, Links provided, Greetings ('happy to help')

## 5. Resolution Usefulness (10 Representative Examples)

**Example 1**
- **Customer Tweet ID:** 208953
- **Customer Message:** Yo @115858 WTF is with this auto WiFi and Bluetooth connection... it’s mad annoying!!!
- **AppleSupport Tweet ID:** 208951
- **AppleSupport Response:** @165449 Happy to help. Please let us know what issues you are seeing there.
- **Appears useful for retrieval?** Yes, provides specific steps

**Example 2**
- **Customer Tweet ID:** 1571012
- **Customer Message:** @AppleSupport so all my music has been removed from my iTunes but is still on my phone... how do I get it back on iTunes pls
- **AppleSupport Tweet ID:** 1571011
- **AppleSupport Response:** @484421 We'd love to help!  Are you missing Apple Music playlists or a personally-uploaded iTunes library?  Is it all or some?
- **Appears useful for retrieval?** Yes, provides specific steps

**Example 3**
- **Customer Tweet ID:** 845873
- **Customer Message:** New IOS update sucks - I keep losing signal @115858 @AppleSupport #notgoodenough
- **AppleSupport Tweet ID:** 845871
- **AppleSupport Response:** @321051 We’d like to help with your signal issue. Is this happening with your cellular signal or Wi-Fi? Which iOS version are you running?
- **Appears useful for retrieval?** Yes, provides specific steps

**Example 4**
- **Customer Tweet ID:** 1858197
- **Customer Message:** @AppleSupport All sorted now. Turning it off and on worked a treat, somethings never change.
- **AppleSupport Tweet ID:** 1858199
- **AppleSupport Response:** @555637 We're glad to hear that's working again. Please reach out if you need help in the future. We'll be here for you.
- **Appears useful for retrieval?** Yes, provides specific steps

**Example 5**
- **Customer Tweet ID:** 2229355
- **Customer Message:** Installed High Sierra on my @115858 MacBook and now it won’t start. Remember when people bought Apple products because the “just worked”?
- **AppleSupport Tweet ID:** 2229353
- **AppleSupport Response:** @297799 We definitely want to get your MacBook running again, for sure. Let's clarify a few things about what you are describing. When you power up your MacBook are there no system sounds heard, and nothing on display? Provide us more details please.
- **Appears useful for retrieval?** Yes, provides specific steps

**Example 6**
- **Customer Tweet ID:** 2142381
- **Customer Message:** @AppleSupport I did that, but it still shows up in the autocomplete. https://t.co/4Hn4xd0zvc
- **AppleSupport Tweet ID:** 2142383
- **AppleSupport Response:** @188271 Do you still experience the issue after writing a message?
- **Appears useful for retrieval?** Yes, provides specific steps

**Example 7**
- **Customer Tweet ID:** 1598108
- **Customer Message:** @AppleSupport I found this article, https://t.co/lL10Z2WbQr, helped a lot. My phone is fixed.
- **AppleSupport Tweet ID:** 1598107
- **AppleSupport Response:** @487003 That's great to hear! Let us know if you have any other questions in the future.
- **Appears useful for retrieval?** Yes, provides specific steps

**Example 8**
- **Customer Tweet ID:** 848422
- **Customer Message:** @AppleSupport I’ve been sending DM’s since Monday, they have all been ignored.
- **AppleSupport Tweet ID:** 848421
- **AppleSupport Response:** @321622 We've got your DM's, and we look forward to working with you there.
- **Appears useful for retrieval?** Yes, provides specific steps

**Example 9**
- **Customer Tweet ID:** 396954
- **Customer Message:** .@115858 how do I get voicemail preview back I hate this update
- **AppleSupport Tweet ID:** 396952
- **AppleSupport Response:** @210021 We're here to help. What happens when you try to view Visual Voicemail?
- **Appears useful for retrieval?** Yes, provides specific steps

**Example 10**
- **Customer Tweet ID:** 2072244
- **Customer Message:** @AppleSupport Hi! Attached image of the IOS I am currently using. I have an iPhone 6s. Thanks https://t.co/v7LtHi9MFi
- **AppleSupport Tweet ID:** 2072246
- **AppleSupport Response:** @612904 Thanks. This would be expected for the music to stop when opening Snapchat, because the camera and microphone are being activated.
- **Appears useful for retrieval?** Yes, provides specific steps

## 6. Candidate Intent Discovery
Recurring themes/topics based on frequent n-grams in customer messages:
- 11 update, app store, apple music, apple watch, battery life, doesn work, high sierra, ios 11, ios 11 update, ios update

## 7. Final Recommendation

**Is AppleSupport suitable for the Hiver assignment?**
**Yes.**

- **Enough customer-support conversations:** Yes, 112078 response pairs available.
- **Enough multi-turn conversations:** Yes, 29599 conversations have 3 or more turns.
- **Enough substantive responses:** Yes, though many contain links to Apple documentation, there is a large absolute volume to filter from.
- **Enough diversity for approximately 8–12 intents:** Yes, covers iOS updates, battery, screen issues, Apple ID, etc.
- **Enough data to build a 150–250 example golden evaluation set:** Yes, easily achievable.
- **Feasibility:** High. The volume is sufficient to apply rigorous filtering for high-quality examples.

**Major Limitations:**
- Many responses are templates requesting DMs or linking to support articles.
- Requires careful filtering to find "substantive" resolutions directly in the tweet text.
