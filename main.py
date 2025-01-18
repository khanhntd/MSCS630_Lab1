import threading
from collections import Counter

# calculateWordFrequencyForEachSegment will caculate word frequency for each segment
def calculateWordFrequencyForEachSegment(segment: str, frequencyFromEachSegment: list[Counter], index: int):
    words = segment.split()
    freq = Counter(words)
    frequencyFromEachSegment[index] = freq
    print(f"Thread {index}: Intermediate Frequency Count: {freq}")

# partitionText will divide the text into the corresponding segments
# and if there are any remaining text, it will append those text into the last segment
def partitionText(text: str, numberOfSegments: int) -> list[str]:
    segmentLength = len(text) // numberOfSegments
    segments = [text[i * segmentLength:(i + 1) * segmentLength] for i in range(numberOfSegments)]

    # Append any remaining text to the last segment
    if len(text) % numberOfSegments:
        segments[-1] += text[numberOfSegments * segmentLength:]

    return segments

def main():
    # Input file and number of segments
    filePath = input("Enter the path to the text file: ")
    numberOfSegments = int(input("Enter the number of segments: "))

    # Read the input file
    with open(filePath, 'r') as file:
        text = file.read()

    # Partition the text into segments
    segments = partitionText(text, numberOfSegments)

    # Prepare a shared data structure for results
    frequencyFromEachSegment = [None] * numberOfSegments
    threads = []

    # Create and start threads
    for i in range(numberOfSegments):
        thread = threading.Thread(target=calculateWordFrequencyForEachSegment, args=(segments[i], frequencyFromEachSegment, i))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Consolidate results
    finalFrequency = Counter()
    for frequency in frequencyFromEachSegment:
        finalFrequency.update(frequency)

    # Output the final consolidated word-frequency count
    print("\nFinal Consolidated Word Frequency:")
    for word, count in finalFrequency.items():
        print(f"{word}: {count}")

if __name__ == "__main__":
    main()
