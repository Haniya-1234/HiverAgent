import pandas as pd
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    candidates = pd.read_csv('data/processed/apple_support_candidates.csv')
    print(f"Total candidates: {len(candidates)}")
    
    intents = {
        'iOS Update/Installation': r'(update|install|download).*(won\'t|stuck|error|fail|can\'t)',
        'Device Freezing/Unresponsive': r'(freeze|freezing|unresponsive|frozen|lagging|slow)',
        'Battery Drain/Health': r'(battery|drain|draining|battery life|battery health)',
        'iOS Autocorrect Bug': r'(question mark|squares|letter i |typing i |A\?|box)',
        'Device Activation': r'(activate|activation server|could not activate)',
        'Apple Music Playback/Library': r'apple music.*(play|library|missing|song|download|sync)',
        'Apple ID / iCloud Account': r'\b(apple id|icloud|locked|password|verification code|disabled)\b',
        'Wi-Fi / Bluetooth Connectivity': r'\b(wifi|wi-fi|bluetooth|disconnect|connection)\b',
        'App Crashing/Closing': r'\b(crash|crashing|closes unexpectedly|quits unexpectedly)\b',
        'Hardware / Physical Damage': r'\b(cracked|shattered|broken screen|water damage)\b'
    }
    
    for intent_name, pattern in intents.items():
        matched = candidates[candidates['customer_text'].str.contains(pattern, flags=re.IGNORECASE, na=False)]
        print(f"{intent_name}: {len(matched)}")
        print(f"\nExamples for {intent_name}:")
        for i, row in matched.head(5).iterrows():
            print(f"- {row['customer_text'].replace('\n', ' ')}")
        print("="*50)

if __name__ == '__main__':
    main()
