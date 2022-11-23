import hashlib
import base64
import sys

DEFAULT_PHRASE = 'jaguar over before resist settle combine language man mammal call slush split rescue theme donate poverty chicken oblige inhale gallery cable daring home abandon hotel'
def main():
    print('Number of arguments: {}'.format(len(sys.argv)))
    print('Argument(s) passed: {}'.format(str(sys.argv)))
    if len(sys.argv) < 2:
        phrase = DEFAULT_PHRASE
    else:
        phrase = sys.argv[1]
    print(
        base64.b64encode(
            hashlib.sha256(
                str(phrase).
                encode('utf-8')
            ).
            digest()
        ).
        decode('utf-8')
    )
if __name__ == "__main__":
    main()
