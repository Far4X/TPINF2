import math

def main() :
    with open("poème.txt", 'r', encoding="UTF-8") as f :
        ct = f.read()

    for char in ".,!?" :
        ct = ct.replace(f" {char}", "")
        ct = ct.replace(char, "")

    ct = ct.replace("'", " ")
    ct = ct.replace("\n", " ")
    words = ct.split(" ")
    print(words)


    with open("output.txt", "w") as f :
        test_pi = 0
        pwr = 0
        for word in words :
            digit = len(word) % 10
            f.write(str(digit))
            test_pi += digit * 10**pwr
            pwr -= 1

        print(test_pi, "\n", math.pi - math.pi % 10**pwr, sep = "")
        print(test_pi == math.pi - math.pi % 10**pwr)
        

if __name__ == "__main__" :
    main()